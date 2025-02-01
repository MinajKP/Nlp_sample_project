import boto3
from boto3.dynamodb.conditions import Key
from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering
from django.conf import settings


class AskDatabase:
    def __init__(self, qa_model, summarizer_model):
        # Initialize with the provided models for question answering and summarization
        self.qa_model = AutoModelForQuestionAnswering.from_pretrained(qa_model)
        self.tokenizer = AutoTokenizer.from_pretrained(qa_model)
        self.nlp_pipeline = pipeline("question-answering", model=self.qa_model, tokenizer=self.tokenizer)
        self.summarizer = pipeline("summarization", model=summarizer_model)
        self.dynamodb = boto3.resource('dynamodb', region_name=settings.AWS_REGION)
        self.table = self.dynamodb.Table(settings.DYNAMODB_TABLE_NAME)


    def summarize_with_bart(self, context, max_length=50, min_length=25):
        try:
            summaries = self.summarizer(context, max_length=max_length, min_length=min_length)
            print(f'Summary: {summaries}')
            return summaries[0]['summary_text']
        except Exception as e:
            return f'Error during summarization: {str(e)}'

    def answer_question(self,question, file_id):
        # Query DynamoDB for the specific file_id
        response = self.table.query(
            IndexName='file_id-index',  # Use the correct index name
            KeyConditionExpression=Key('file_id').eq(file_id)
        )
        print(f'\nresponse value is : {response}')

        # Check if response contains 'Items' and ensure it's not empty
        if 'Items' not in response or not response['Items']:
            return "No file found!"

        # Get the first item in the response (DynamoDB returns an array of items)
        file_item = response['Items'][0]  # Access the first item in the list
        print(f'\nfile_item: {file_item}\n')

        # Ensure 'content' is present in the file item
        if 'content' not in file_item:
            return "No content found in the file!"

        # Get the content from the file item
        full_content = file_item.get('content', None)  # Access content from the item
        print(f'\nFull content in answer question: {full_content}\n')

        # If no content is found, return an error
        if not full_content:
            return "Error: Content not found in the file!"

        # Use Hugging Face's pipeline for question answering
        answer = self.nlp_pipeline(question=question, context=full_content)
        print(f'\nAnswer is {answer}')
        # Consider confidence score when selecting the answer
        if answer['score'] > 0.005:  # Adjust threshold as needed
            span = answer['answer']
            print(f'\nSpan : {span}')
        else:
            span = "I'm not confident in the answer."

        # Get a 'wanted_context' from span(answer)
        start = full_content.rfind('.', 0, full_content.find(span)) + 1  # Get the last period before answer
        print(f'START: {start}')
        if start == 0:  # If no period is found before the answer, start from the beginning
            start = 0

        second_period = full_content.find('.', start + 1)
        print(f'\nsecond period: {second_period}')
        if second_period != -1:
            end = full_content.find('.', second_period + 1)
            end = end + 1 if end != -1 else len(full_content)
            print(f'END: {end}')

        else:
            end = len(full_content)
            print(f'END: {end}')

        wanted_context = full_content[start:end].strip()
        print(f'\nWanted context: {wanted_context}')  # This will now include the name
        summarized_answer = self.summarize_with_bart(wanted_context)
        return summarized_answer
