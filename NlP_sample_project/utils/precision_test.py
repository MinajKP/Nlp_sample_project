gold_set = [
    {
        "text": "Barack Obama was born in Hawaii. Michelle Obama is his wife.",
        "expected": ["Barack Obama", "Michelle Obama"]
    },
    {
        "text": "Elon Musk founded Tesla. His brother Kimbal Musk is a restaurateur.",
        "expected": ["Elon Musk", "Kimbal Musk"]
    },
    {
        "text": "Sundar Pichai leads Google, while Satya Nadella runs Microsoft.",
        "expected": ["Sundar Pichai", "Satya Nadella"]
    },
    {
        "text": "Marie Curie discovered radium. Her daughter Irène Joliot-Curie also won a Nobel Prize.",
        "expected": ["Marie Curie", "Irène Joliot-Curie"]
    },
    {
        "text": "Jeff Bezos founded Amazon. His ex-wife MacKenzie Scott is a philanthropist.",
        "expected": ["Jeff Bezos", "MacKenzie Scott"]
    }
]
#
# from name_extractor import NLTKNameExtractor
#
# def test_precision():
#
#     extractor = NLTKNameExtractor()
#     TP_total = 0
#     PF_total = 0
#
#     my_names = []
#     for item in gold_set:
#         actual_names = set(extractor.extract_names(item['text'])) #Returned by the name extractor
#         expected_names = set(item['expected']) #Expected items by extractor
#
#         TP = actual_names & expected_names #Correct names - intersection
#         FP = actual_names - expected_names #Wrong names - difference
#
#         TP_total += len(TP)
#         PF_total += len(FP)
#
#     total_predicted = TP_total+PF_total
#     precision = TP_total/total_predicted
#     print(precision)
#
# test_precision()

from name_extractor import NLTKNameExtractor


def evaluate_precision_on_text(gold_examples):\

    extractor = NLTKNameExtractor()
    total_tp = 0
    total_fp = 0

    for example in gold_examples:
        text = example["text"]
        expected = set(example["expected"])
        predicted = set(extractor.extract_names(text))

        tp = predicted.intersection(expected)
        fp = predicted.difference(expected)

        total_tp += len(tp)
        total_fp += len(fp)

        precision = len(tp) / len(predicted) if predicted else 0

        print(f"\n📝 Text: {text}")
        print(f"✅ Expected: {expected}")
        print(f"🔍 Predicted: {predicted}")
        print(f"🎯 True Positives: {tp}")
        print(f"❌ False Positives: {fp}")
        print(f"📊 Precision: {precision:.2f}")

    total_pred = total_tp + total_fp
    overall_precision = total_tp / total_pred if total_pred else 0

    print(f"\n========================")
    print(f"🎯 Overall Precision: {overall_precision:.2f}")
    print(f"========================")

evaluate_precision_on_text(gold_set)
