from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.preprocessing import MultiLabelBinarizer

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

def scikit_f1():

    extractor = NLTKNameExtractor()

    Y_true_total = []
    Y_pred_total = []

    for item in gold_set:
        expected = list(set(item['expected']))
        predicted = list(set(extractor.extract_names(item['text'])))

        Y_true_total.append(expected)
        Y_pred_total.append(predicted)


    mlb = MultiLabelBinarizer()

    mlb.fit(Y_true_total)

    Y_true_bin = mlb.transform(Y_true_total)
    Y_pred_bin = mlb.transform(Y_pred_total)

    precision = precision_score(Y_true_bin,Y_pred_bin,average='micro')
    recall = recall_score(Y_true_bin,Y_pred_bin,average='micro')
    f1 = f1_score(Y_true_bin,Y_pred_bin,average='micro')

    print(f"PRECISION: {precision}\n")
    print(f"RECALL: {recall}\n")
    print(f"F1: {f1}\n")


scikit_f1()