import sys
from nltk.corpus import wordnet


def main():
    synsets = wordnet.synsets(sys.argv[1])
    result_synsets = set()
    for synset in synsets:
        get_hypernyms(synset, result_synsets)
    print("\nAll Synsets: ", result_synsets)

    hypernym_words = set()
    for hypernym_synset in result_synsets:
        hypernym_synset_words = map(lambda lemma: lemma.name(), hypernym_synset.lemmas())
        hypernym_words.update(hypernym_synset_words)
    print("All words: ", hypernym_words)


def get_hypernyms(synset, result):
    for hypernym in synset.hypernyms():
        print(f"{synset} -> {hypernym}")
        if hypernym not in result:
            result.add(hypernym)
            get_hypernyms(hypernym, result)


if __name__ == "__main__":
    main()
