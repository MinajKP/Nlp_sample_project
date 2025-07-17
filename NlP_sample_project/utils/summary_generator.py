import sys

from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from django.conf import settings
import django
import os

# Step 1: Fix the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# CHANGE: Django setup for standalone script
# This allows the script to run independently and access Django models
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'NlP_sample_project.settings')
django.setup()

from nlp_app.models import UploadedFile


class SummaryGenerator:

    def __init__(self,model_name = "facebook/bart-large-cnn"):
        print("Loading summarization model...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.summarizer = pipeline("summarization",model=self.model, tokenizer=self.tokenizer)

    def generate_summary(self,content, max_length=128, min_length=20, do_sample=False):

        if not content or not content.strip():
            return "Empty file !!"

        summary = self.summarizer(content,max_length=max_length,min_length=min_length, do_sample=do_sample)
        return summary[0]['summary_text']

if __name__ == "__main__":
    try:
        file_id = int(input("Enter a file ID: "))
    except ValueError:
        print("Please enter a valid ID number !!")

    try:
        file = UploadedFile.objects.get(id=file_id)
    except UploadedFile.DoesNotExist:
        print("File doesnt exist !!")

    summarizer = SummaryGenerator()
    summary = summarizer.generate_summary(file.content)

    print("\n" + "=="*20)
    print(f"SUMMARY FOR FILE_ID: {file_id}")
    print("\n" + "=="*20)
    print(f"SUMMARY: {summary}")
    print("\n" + "=="*20)