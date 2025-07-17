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


def test_f1():

    extractor = NLTKNameExtractor()

    total_tp = 0
    total_fp = 0
    total_fn = 0

    for item in gold_set:
        expected = set(item['expected'])
        actual = set(extractor.extract_names(item['text']))

        tp = expected.intersection(actual)
        fp = actual.difference(expected)
        fn = expected.difference(actual)

        total_tp += len(tp)
        total_fp += len(fp)
        total_fn += len(fn)

    precision = total_tp/(total_tp+total_fp) if (total_tp+total_fp) else 0
    print(f"PRECISION: {precision:.2f}")
    recall = total_tp/(total_tp+total_fn) if (total_tp+total_fn) else 0
    print(f"RECALL: {recall:.2f}")
    f1_score = 2*(precision*recall)/(precision+recall) if (precision + recall) else 0
    print(f"F1 SCORE: {f1_score:.2f}")

test_f1()