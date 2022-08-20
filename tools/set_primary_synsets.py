from config import TERM_PRIMARY_SYNSETS_PATH, TERMS_PATH

import yaml
import sys
from nltk.corpus import wordnet


def print_term_synsets(term, added, options):
    print(f"TERM: {term}")

    print("Added:")
    for synset in added:
        print(f"\t {synset.name()}: {synset.definition()}")
    
    print("Options:")
    for i in range(len(options)):
        print(f"\t [{i}] {options[i].name()}: {options[i].definition()}")


def set_term_synsets(term, term_synsets):
    if term not in term_synsets:
        term_synsets[term] = []

    while True:
        all_synsets = wordnet.synsets(term)
        added = list(map(lambda synset_name: wordnet.synset(synset_name), term_synsets[term]))
        added.sort(key=lambda s: s.name())
        options = list(set(all_synsets) - set(added))
        options.sort(key=lambda s: s.name())

        if (len(options) == 0):
            print("Skipped")
            break
        if (len(added) == 0 and len(options) == 1):
            term_synsets[term].append(options[0].name())
            print("Only 1 option, skipped")
            break

        print_term_synsets(term, added, options)
        key = input()
        try:
            term_synsets[term].append(options[int(key)].name())
        except:
            print("Invalid input")
            break


def main():
    with open(TERM_PRIMARY_SYNSETS_PATH, 'r') as f:
        term_synsets = yaml.safe_load(f)
    term_synsets = term_synsets if term_synsets is not None else dict()

    print(sys.argv)
    i = 1 if len(sys.argv) == 1 else int(sys.argv[1])
    print(i)
    terms = list(open(TERMS_PATH, "r").read().splitlines())
    while i < len(terms):
        term = terms[i]
        print("\n\n")
        print(f" --- {i} / {len(terms)}  {term} --- ")
        i += 1
        set_term_synsets(term, term_synsets)
        with open(TERM_PRIMARY_SYNSETS_PATH, "w") as out_file:
            yaml.dump(term_synsets, out_file)


if __name__ == "__main__":
    main()
