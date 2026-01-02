from transformers import pipeline


class SentimentsClassifier:

    def __init__(self):

        self.classifier = pipeline(
            task="sentiment-analysis",
            model="cardiffnlp/twitter-xlm-roberta-base-sentiment",
        )

    def classify(self, text: str) -> dict:
        text = text[:514]

        result = self.classifier(text)[0]

        return {
            "text": text,
            "sentiment": result["label"],
            "confidence": round(result["score"], 4)
        }


if __name__ == "__main__":
    c = SentimentsClassifier()

    for i in [
        "Сервіс жахливий",
        "я знайшов те що шукав",
        "як так можна",
        "могло бути краще",
        "в цілому норм",
        "дійсно добре зроблене"
    ]:
        res = c.classify(i)
        print(res)
