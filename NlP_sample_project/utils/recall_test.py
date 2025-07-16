from name_extractor import NLTKNameExtractor

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

def recall_test():

    extractor = NLTKNameExtractor()
    total_tp = 0
    total_fn = 0

    for item in gold_set:
        expected = set(item['expected'])
        actual = set(extractor.extract_names(item['text']))

        TP = expected.intersection(actual)
        FN = expected.difference(actual)

        total_tp += len(TP)
        total_fn += len(FN)

        print(f"\n\nTEXT: {item['text']}")
        print(f"ACTUAL: {actual}")
        print(f"EXPECTED: {expected}")
        print(f"TRUE POSITIVE: {TP}")
        print(f"FALSE NEGATIVE (MISSED ITEMS): {FN}")
        recall = len(TP)/len(expected) if expected else 0
        print("RECALL: ", recall)

    total_pred = total_tp+total_fn
    overall_recall = total_tp/total_pred if total_pred else 0
    print(f"\n\nOVERALL RECALL: {overall_recall}")

recall_test()