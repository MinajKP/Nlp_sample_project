import nltk
import django
import os
import sys
from django.conf import settings

# Step 1: Fix the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# CHANGE: Django setup for standalone script
# This allows the script to run independently and access Django models
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'NlP_sample_project.settings')
django.setup()

from nlp_app.models import UploadedFile


def download_required_resources():

    required_resources = [
        'punkt_tab',  # Sentence tokenizer
        'maxent_ne_chunker_tab',  # Named Entity Recognition model
        'words',  # List of English words
        'averaged_perceptron_tagger_eng'  # POS tagger model
    ]

    for resource in required_resources:
        try:
            if resource == 'punkt_tab':
                nltk.data.find('tokenizers/punkt_tab')
            elif resource == 'maxent_ne_chunker_tab':
                nltk.data.find('chunkers/maxent_ne_chunker_tab')
            elif resource == 'words':
                nltk.data.find('corpora/words')
            elif resource == 'averaged_perceptron_tagger_eng':
                nltk.data.find('taggers/averaged_perceptron_tagger_eng')
            print(f'NLTK Resource {resource} already available!')
        except LookupError:
            print(f"Downloading NLTK resource {resource}")
            nltk.download(resource)
            print(f"Successfully downloaded the package: {resource}")

download_required_resources()


class NLTKNameExtractor:

    #why?
    def __init__(self):
        self.ensure_nltk_data()

    #why double check
    def ensure_nltk_data(self):
        required_data = [
            ('punkt_tab', 'tokenizers/punkt_tab'),
            ('maxent_ne_chunker_tab', 'chunkers/maxent_ne_chunker_tab'),
            ('words', 'corpora/words'),
            ('averaged_perceptron_tagger_eng', 'taggers/averaged_perceptron_tagger_eng')
        ]

        for name,path in required_data:
            try:
                nltk.data.find(path)
                print(f'NLTK data {name} already exists!!')
            except LookupError:
                print(f'Downloading NLTK data {name}')
                nltk.download(name)
                print(f'Successfully downloaded {name}')

    def extract_names(self,text):

        if not text or not isinstance(text,str):
            return []

        try:
            sentences = nltk.sent_tokenize(text)
            names = []

            for sentence in sentences:
                words = nltk.word_tokenize(sentence) #tokenise sentences to words
                # print(f"--------------WORDS--------------\n {words}")
                pos_tags = nltk.pos_tag(words)
                # print(f"--------------POS TAGS--------------\n {pos_tags}")
                named_entities = nltk.ne_chunk(pos_tags)
                # print(f"--------------NAMED ENTITIES--------------\n ")
                # named_entities.pprint()

                for chunk in named_entities:
                    if hasattr(chunk,'label') and chunk.label() =='PERSON':
                        name = ' '.join([token for token,pos in chunk.leaves()])
                        # print(f"--------------NAMES--------------\n {name}")
                        # print("Chunk label():", chunk.label())  # actual label like 'PERSON'
                        names.append(name)
            return sorted(list(set(names)))  # Remove duplicates and return


        except Exception as e:
            print(f"Error in name extraction{str(e)}")
            return []

    def get_file_from_mysql(self,file_id):

        try:
            uploaded_file = UploadedFile.objects.get(id=file_id)
            print(f'Successfully retrieved file: {uploaded_file.title}')
            return uploaded_file
        except UploadedFile.DoesNotExist:
            print(f'File ID: {file_id} not found in Mysql DB!!')
        except Exception as e:
            print(f'Error retrieving file from MySql: {str(e)}')
            return None

    def extract_name_from_file_id(self,file_id):
        print(f'Extracting names from File ID: {file_id}')
        uploaded_file = self.get_file_from_mysql(file_id)

        if not uploaded_file:
            return {'success':False, 'error': 'File not found in database','file_id':file_id}

        print(f"📝 Extracting names from content ({len(uploaded_file.content)} characters)...")
        names = self.extract_names(uploaded_file.content)

        result = {
            'success': True,
            'file_id': file_id,
            'file_title': uploaded_file.title,
            'uploaded_at': uploaded_file.uploaded_at,
            'content_length': len(uploaded_file.content),
            'extracted_names': names,
            'total_names_found': len(names)
        }

        print(f'Name extraction completed. Found {len(names)} unique names !')
        return result

def main():
    print("🚀 NLTK Name Extractor - MySQL Database Integration")
    print("=" * 60)

    try:
        extractor = NLTKNameExtractor()
    except Exception as e:
        print(f'Error initializing NLTK name extractor {str(e)}')
        return

    while True:
        print("\n📋 Choose an option:")
        print("1. Extract names from specific file (by ID)")
        print("2. List all files in database")
        print("3. Exit")

        choice = input(f'Enter a choice(1-3): ').strip()

        if choice =='1':
            try:
                file_id = int(input('Enter file ID: ').strip())
                result = extractor.extract_name_from_file_id(file_id)

                if result['success']:
                    print(f"\n📄 File: {result['file_title']}")
                    print(f"📅 Uploaded: {result['uploaded_at']}")
                    print(f"📊 Content length: {result['content_length']} characters")
                    print(f"👥 Names found ({result['total_names_found']}):")
                    for i,name in enumerate (result['extracted_names'],1):
                        print(f"{i}. {name}")
                else:
                    print(f"{result['error']}")
            except ValueError:
                print("Please enter a valid file ID(number)")
            except Exception as e:
                print(f'Error: {str(e)}')

        elif choice == '2':
            all_files = UploadedFile.objects.all()
            if all_files.exists():
                print(f"\n📁 All files in MySQL database ({all_files.count()}):")
                for uploaded_file in all_files:
                    print(f'ID: {uploaded_file.id}')
                    print(f'Title: {uploaded_file.title}')
                    print(f'Uploaded: {uploaded_file.uploaded_at}')
                    print(f"📊 Content length: {len(uploaded_file.content)} characters")
                    print("-" * 30)

            else:
                print('No files found in database')

        elif choice == '3':
            print("👋 Goodbye!")
            break

        else:
            print("Invalid choice. Please enter an option from 1-3.")

if __name__ =='__main__':
    main()
