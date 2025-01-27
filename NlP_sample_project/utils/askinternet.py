import sys

import requests

class AskInternet:
    def __init__(self, google_api_key, cse_id):
        self.GOOGLE_API_KEY = google_api_key
        self.CSE_ID = cse_id

    def search_internet(self,question):
        url = f"https://www.googleapis.com/customsearch/v1?q={question}&key={self.GOOGLE_API_KEY}&cx={self.CSE_ID}"
        response = requests.get(url)
        print(response.status_code)  # Check the status code
        print(response.text)  # Print raw response to see the data returned by the API

        if response.status_code == 200:
            search_results = response.json().get('items', [])
            if search_results:
                first_result = search_results[0]
                return first_result.get('snippet', "No relevant answer found.")
        return "No relevant answer found."

    def answer_question_from_internet(self,question):
        """Answer a question by searching the internet."""
        print("\nSearching the internet...\n")
        return self.search_internet(question)


def main():
    # Ask the user for their question interactively
    question = input("Please enter your question: ").strip()

    # Check if the question is provided
    if not question:
        print("You must provide a question!")
        return

    # Google API Key and Custom Search Engine ID (replace with actual values)
    GOOGLE_API_KEY = 'AIzaSyC2uZBrkokicMltHIeyl5ywYXUM01Jz4Sk'
    CSE_ID = '010805fb737b14f43'

    # Initialize the AskInternet class
    ask_internet = AskInternet(GOOGLE_API_KEY, CSE_ID)

    # Get the answer to the question
    answer = ask_internet.answer_question_from_internet(question)

    # Print the result
    print(f"\nAnswer: {answer}")

if __name__ == "__main__":
    main()