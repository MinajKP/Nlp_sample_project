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

from name_extractor import NLTKNameExtractor

def test_precision():

    extractor = NLTKNameExtractor()

    my_names = []
    for item in gold_set:
        actual_names = extractor.extract_names(item['text']) #Returned by the name extractor
        expected_names = item['expected'] #Expected items by extractor


    TP = actual_names & expected_names #Correct names - intersection
    FP = actual_names - expected_names #Wrong names - difference

    precision = TP/TP+FP

test_precision()