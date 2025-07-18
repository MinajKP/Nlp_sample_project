from bert_score import score
from summary_generator import SummaryGenerator

def test_BERTScore():

    summarizer = SummaryGenerator()

    with open(r"C:\Users\USER\Downloads\reference_summary.txt",'r',encoding='utf-8') as file:
        reference_summary = file.read()

    with open(r'C:\Users\USER\Downloads\text.txt','r',encoding='utf-8') as my_file:
        generated_summary = summarizer.generate_summary(my_file.read())

    p,r,f1 = score([generated_summary],[reference_summary],lang='en',verbose=True)
    print(f"REFERENCE SUMMARY: {reference_summary}")
    print(f"GENERATED SUMMARY: {generated_summary}")
    print(f"PRECISION: {p}")
    print(f"RECALL: {r}")
    print(f"F1 SCORE: {f1}")


if __name__ == "__main__":
    test_BERTScore()


