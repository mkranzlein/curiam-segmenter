# curiam-segmenter
This is a [spaCy](https://spacy.io/)-based **sentence segmenter for legal texts**. It was developed and initially used for a corpus of U.S. Supreme Court opinions with metalanguage annotations called CuRIAM. The segmenter was trained on 41 U.S. Supreme Court opinions from the Court's 2019 term. The opinions are written in English.

We have not conducted any formal evaluation of the segmenter's performance. Anecdotally, it gets the vast majority of sentence boundaries on in-domain documents correct. When it does occasionally fail, it's often because of unfamiliar party names in legal citations, especially those complicated by numbers or abbreviations with periods.

The model is initialized from [en_core_web_lg](https://spacy.io/models/en#en_core_web_lg) and trained on 41 manually segmented opinions from the U.S. Supreme Court. This manual segmentation was an iterative process. First, we used spaCy to tokenize and segment a handful of opinions. We fixed the output on those opinions, retrained the model, and repeated the process, adding a few more opinions each time until we had gold sentence boundaries for all 41 opinions. We then retrained the model a final time on those 41 opinions, and this is the model that is released. You can train it from scratch using the intructions below or you can use the version provided in the [saved_model](saved_model) directory.

## Training the model

Install dependencies and activate the environment:

```
$ mamba env create -f environment.yml
$ mamba activate curiam-segmenter
```

Download spaCy's [en_core_web_lg](https://spacy.io/models/en#en_core_web_lg) model:

```
$ python -m spacy download en_core_web_lg
```

Serialize the [training text files](data/train) into a spaCy `DocBin` object for training and dev. The dev set is **not** an actual dev set here. The dev set is a full copy of the training set, used to show training progress.

```
$ python scripts/prep_training_data.py
```

Train and save the model in the [models](models) folder:

With GPU:

```
$ python -m spacy train training_config.cfg --paths.train train.spacy --paths.dev dev.spacy -o models --gpu-id 0
```

With CPU (this may take a very long time, training only tested with GPU):

```
$ python -m spacy train training_config.cfg --paths.train train.spacy --paths.dev dev.spacy -o models
```

## Download the trained model

Extract the [model-last](saved_model/model-last.tar.gz) directory from [saved_model](saved_model).

```
$ cd saved_model
$ tar -xf model-last.tar.gz
```

## Inference

The model (trained from scratch or downloaded) can be used like any off-the-shelf spaCy model:

```python
import spacy

paragraph = "This is a sentence. This is another sentence."

custom_nlp = spacy.load("saved_model/model-last")git
doc = custom_nlp(paragraph)
for sent in list(doc.sents):
    print(sent)
```

Output:
```
This is a sentence.

This is another sentence.
```
