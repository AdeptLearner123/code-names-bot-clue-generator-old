import sys
from nltk.corpus import wordnet


def main():
    synsets = wordnet.synsets(sys.argv[1])
    result_synsets = set()
    for synset in synsets:
        get_hyponyms(synset, result_synsets)
    print("\nAll Synsets: ", result_synsets)

    hyponym_words = set()
    for hyponym_synset in result_synsets:
        hyponym_words.update(result_synsets.lemmas())
    print("All words: ", hyponym_words)


def get_hyponyms(synset, result):
    for hyponym in synset.hyponyms():
        print(f"{synset} -> {hyponym}")
        result.add(hyponym)


if __name__ == "__main__":
    main()
