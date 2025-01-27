from elasticsearch_dsl import Search
from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering

class AskDatabase:
    def __init__(self, qa_model, summarizer_model):
        # Initialize with the provided models for question answering and summarization
        self.qa_model = AutoModelForQuestionAnswering.from_pretrained(qa_model)
        self.tokenizer = AutoTokenizer.from_pretrained(qa_model)
        self.nlp_pipeline = pipeline("question-answering", model=self.qa_model, tokenizer=self.tokenizer)
        self.summarizer = pipeline("summarization", model=summarizer_model)

    def summarize_with_bart(self, context, max_length=50, min_length=20):
        try:
            summaries = self.summarizer(context, max_length=max_length, min_length=min_length)
            print(f'Summary: {summaries}')
            return summaries[0]['summary_text']
        except Exception as e:
            return f'Error during summarization: {str(e)}'

    def answer_question(self, file_id, question):
        # Query Elasticsearch for the specific file_id
        search = Search(index='file_index').query("match", file_id=file_id)
        search_results = search.execute()
        if search_results:
            full_context = search_results[0].content
            print(f'Full context in answer question: {full_context}')
        else:
            return "No relevant content found for the given file."

        # Use Hugging Face's pipeline for question answering with confidence score
        answer = self.nlp_pipeline(question=question, context=full_context)
        print(f'Answer: {answer}')

        # Consider confidence score when selecting the answer
        if answer['score'] > 0.6:  # Adjust threshold as needed
            concise_answer = answer['answer']
            print(f'Concise Answer : {concise_answer}')
        else:
            concise_answer = "I'm not confident in the answer."

        # Look for a more detailed context if the answer is a name (optional)
        if answer['answer'].lower() in full_context.lower():
            start = full_context.find(answer['answer'])
            print(f'START value: {start}')
            second_period = full_context.find('.', start + 1)
            end = full_context.find('.', second_period + 1) + 1  # Find the second period after the first
            print(f'END value: {end}')
            detailed_context = full_context[start:end].strip()
            print(f'detailed_context : {detailed_context}')
            summarized_answer = self.summarize_with_bart(detailed_context)
            concise_answer = summarized_answer
            print(f'Concise answer : {concise_answer}')
            return concise_answer
