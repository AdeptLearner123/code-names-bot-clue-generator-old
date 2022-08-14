import sys

from nltk.corpus import wordnet


def main():
    synsets = wordnet.synsets(sys.argv[1])
    for synset in synsets:
        print(synset)
        print("Definition: ", synset.definition())
        print("Words", list(map(lambda lemma: lemma.name(), synset.lemmas())))
        print("Hypernyms:", synset.hypernyms())
        print("Hyponyms:", synset.hyponyms(), "\n")


if __name__ == "__main__":
    main()
