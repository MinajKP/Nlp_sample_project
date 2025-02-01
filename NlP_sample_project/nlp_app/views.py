from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import UploadedFile
from django.conf import settings
import hashlib
from utils.askinternet import AskInternet
from utils.data_upload import DataUpload
from utils.askdatabase import AskDatabase

ask_internet = AskInternet(google_api_key= settings.GOOGLE_API_KEY, cse_id=settings.CSE_ID)
data_upload = DataUpload()
ask_database = AskDatabase("deepset/roberta-base-squad2", "facebook/bart-large-cnn")

# Function to generate a hash for the file content
def generate_file_hash(content):
    return hashlib.sha256(content.encode()).hexdigest()

# View for handling file uploads and answering queries
def handle_request(request):
    uploaded_file = None
    answer = None
    internet_answer = None

#Check for the request type
    if request.method == 'POST':  # Handle file upload
        file_data = request.FILES.get('file') #'file': name of the file input field from the HTML form that was submitted by the user.
        if file_data:
            content = file_data.read().decode('utf-8')
            file_hash = generate_file_hash(content) # Generate unique hash

            # Creates an instance of UploadedFile model to save in Django database
            uploaded_file = UploadedFile.objects.create(title=file_data.name, content=content)
            data_upload.index_uploaded_file(uploaded_file)  # Index the file in DynamoDB after upload

            return JsonResponse({'message': 'File uploaded successfully', 'file_name': uploaded_file.title})

    elif request.method == 'GET':  # Handle answering query and rendering page
        # Check for query parameters for file ID and question
        file_id = request.GET.get('file_id')
        question = request.GET.get('question')
        internet_question = request.GET.get('internet_question')

        if file_id and question:
            # Query DynamoDB to retrieve file using the file_hash
            file_content = data_upload.get_file_by_id(file_id)
            if not file_content:
                return JsonResponse({'message': 'File not found in DynamoDB'}, STATUS=404)

            # Use Hugging Face's pipeline for question answering
            answer = ask_database.answer_question(question,file_id)  # Query DynamoDB

        # Handle searching the internet if the question is an internet query
        if internet_question:
            internet_answer = ask_internet.search_internet(internet_question)  # Perform internet search and get results

        # If it's a normal page load (non-AJAX), render the main page
        if not request.is_ajax():
            return render(request, 'main_page.html', {
                'uploaded_file': uploaded_file,
                'answer': answer,
                'file': file_id,
                'internet_answer': internet_answer
            })

        # For AJAX requests, return the answers dynamically
        return JsonResponse({
            'answer': answer if answer else "No answer found",
            'internet_answer': internet_answer if internet_answer else "No internet results found"
        })
    return JsonResponse({'message': 'Invalid request method or parameters.'}, status=400)
