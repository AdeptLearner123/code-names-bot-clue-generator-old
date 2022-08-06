import sys

from nltk.corpus import wordnet

from code_names_bot_clue_generator.hypernym_scores.generate_hypernym_clues import \
    get_term_hypernyms


def main():
    result_synsets, result_words = get_term_hypernyms(sys.argv[1])

    for synset in result_synsets:
        depth, path = result_synsets[synset]
        print(synset, depth, path)

    print()

    for word in result_words:
        depth, path = result_words[word]
        print(word, depth, path)


if __name__ == "__main__":
    main()
