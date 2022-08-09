import sys

from nltk.corpus import wordnet

from code_names_bot_clue_generator.hypernym_clues.generate_hypernym_clues import \
    get_all_hypernyms, filter_hypernyms, get_synset_words


def print_path_map(map):
    for key in map:
        depth, path = map[key]
        print(key, depth, path)


def main():
    term = sys.argv[1]

    print("--- All ---")
    hypernym_synsets = get_all_hypernyms(term)
    print_path_map(hypernym_synsets)
    print()

    print("--- Filtered ---")
    hypernym_synsets = filter_hypernyms(term, hypernym_synsets)
    print_path_map(hypernym_synsets)
    print()

    print("--- Words ---")
    hypernym_words = get_synset_words(hypernym_synsets)
    print_path_map(hypernym_words)
    print()


if __name__ == "__main__":
    main()
