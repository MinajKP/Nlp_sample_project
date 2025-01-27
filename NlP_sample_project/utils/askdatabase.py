from djoser.conf import settings
from elasticsearch_dsl import Search
from elasticsearch_dsl.async_connections import connections
from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering

# Load model for question answering
qa_model = "deepset/roberta-base-squad2"
model = AutoModelForQuestionAnswering.from_pretrained(qa_model)
tokenizer = AutoTokenizer.from_pretrained(qa_model)
nlp_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)

# Load summarization model for summarizing the span
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_with_bart(context, max_length=50, min_length=20):
    try:
        summaries = summarizer(context, max_length=max_length, min_length=min_length)
        print(f'Summary: {summaries}')
        return summaries[0]['summary_text']
    except Exception as e:
        return f'Error during summarization: {str(e)}'

def answer_question(file_id, question):
    # Query Elasticsearch for the specific file_id
    search = Search(index='file_index').query("match", file_id=file_id)
    search_results = search.execute()
    if search_results:
        full_context = search_results[0].content
        print(f'Full context in answer question: {full_context}')
    else:
        return "No relevant content found for the given file."

    # Use Hugging Face's pipeline for question answering with confidence score
    answer = nlp_pipeline(question=question, context=full_context)
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
        summarized_answer = summarize_with_bart(detailed_context)
        concise_answer = summarized_answer
        print(f'Concise answer : {concise_answer}')
        return concise_answer

def setup_elasticsearch_connection():
    """Configure the Elasticsearch connection."""
    try:
        from django.conf import settings  # Import settings from Django
        connections.configure(
            default={
                'hosts': [settings.ELASTICSEARCH_HOST],
                'http_auth': tuple(settings.ELASTICSEARCH_AUTH.split(',')),
            }
        )
        print("Connected to Elasticsearch successfully.")
    except Exception as e:
        print(f"Error configuring Elasticsearch connection: {e}")
        exit(1)

if __name__ == "__main__":

    setup_elasticsearch_connection()  # Configure the connection
    while True:
        print("\n--- Question Answering Terminal ---\n")
        file_id = input("Enter the File ID (or type 'exit' to quit): ")
        if file_id.lower() == "exit":
            print("Exiting...")
            break
        question = input("Enter your question: ")
        print("\nFetching answer...\n \n")
        print(answer_question(file_id, question))