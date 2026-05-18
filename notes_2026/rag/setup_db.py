from sentence_transformers import SentenceTransformer, util


model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')


sentences = [
    "я гуляю з собакою по вихідних",
    "люблю походити із псем по парку у неділю",
    "мій кіт охоче спить цілими днями"
]


embeddings = model.encode(sentences)


print("пес - пес", util.cos_sim(embeddings[0], embeddings[1]))
print("пес - кіт", util.cos_sim(embeddings[1], embeddings[2]))
print("кіт - пес", util.cos_sim(embeddings[2], embeddings[0]))
