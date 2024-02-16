import os

import spacy

from spacy.tokens import Doc
from spacy.tokens import DocBin

nlp = spacy.load('en_core_web_lg')


def get_spaces(tokens):
    spaces = [True] * (len(tokens) - 1)
    spaces.append(False)
    return spaces


opinions = []

for filename in os.listdir("data/train"):
    if filename.endswith(".txt"):
        with open(f"data/train/{filename}", "r", encoding="utf-8") as f:
            sentences = f.read().split("\n")
            opinions.append(sentences)

db = DocBin()

for opinion in opinions:
    docs = []
    # Each sent is a string of tokens separated by spaces
    for sent_string in opinion:
        tokens = sent_string.split(" ")
        tokens = [tok for tok in tokens if tok != ""]
        if tokens == []:
            continue
        spaces = get_spaces(tokens)
        doc = Doc(nlp.vocab, tokens, spaces)
        docs.append(doc)
    db.add(Doc.from_docs(docs, ensure_whitespace=True))

db.to_disk("train.spacy")
db.to_disk("dev.spacy")
