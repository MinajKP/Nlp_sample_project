from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import UploadedFile
from django.conf import settings
from utils.askinternet import AskInternet
from utils.data_upload import DataUpload
from utils.askdatabase import answer_question

ask_internet = AskInternet(google_api_key= settings.GOOGLE_API_KEY, cse_id=settings.CSE_ID)
data_upload = DataUpload()

# View for handling file uploads and answering queries
def handle_request(request):
    uploaded_file = None
    answer = None
    file = None
    internet_answer = None

    if request.method == 'POST':  # Handle file upload
        file_data = request.FILES.get('file')
        if file_data:
            content = file_data.read().decode('utf-8')
            uploaded_file = UploadedFile.objects.create(title=file_data.name, content=content)
            data_upload.index_uploaded_file(uploaded_file)  # Index the file in Elasticsearch after upload
            return JsonResponse({'message': 'File uploaded successfully', 'file_name': uploaded_file.title})

    elif request.method == 'GET':  # Handle answering query and rendering page
        # Check for query parameters for file ID and question
        file_id = request.GET.get('file_id')
        question = request.GET.get('question')
        internet_question = request.GET.get('internet_question')

        if file_id and question:
            file = get_object_or_404(UploadedFile, id=file_id)
            answer = answer_question(file_id, question)  # Answer the question based on file content

        # Handle searching the internet if the question is an internet query
        if internet_question:
            internet_answer = ask_internet.search_internet(internet_question)  # Perform internet search and get results

        # If it's a normal page load (non-AJAX), render the main page
        if not request.is_ajax():
            return render(request, 'main_page.html', {
                'uploaded_file': uploaded_file,
                'answer': answer,
                'file': file,
                'internet_answer': internet_answer
            })

        # For AJAX requests, return the answers dynamically
        return JsonResponse({
            'answer': answer if answer else "No answer found",
            'internet_answer': internet_answer if internet_answer else "No internet results found"
        })
    return JsonResponse({'message': 'Invalid request method or parameters.'}, status=400)
