from config import TERM_PRIMARY_SYNSETS_PATH, TERMS_PATH

import yaml
import sys
from nltk.corpus import wordnet


def print_term_synsets(term, primary, options):
    print(f"TERM: {term}")

    print("Primary:")
    if primary is not None:
        print(f"\t {primary.name()}: {primary.definition()}")
    
    print("Options:")
    for i in range(len(options)):
        print(f"\t [{i}] {options[i].name()}: {options[i].definition()}")


def set_term_synsets(term, term_synsets):
    primary = None
    if term in term_synsets:
        primary = wordnet.synset(term_synsets[term])
    else:
        try:
            primary = wordnet.synset(f"{term.lower().replace(' ', '_')}.n.01")
        except:
            primary = None
    options = wordnet.synsets(term.replace(' ', '_'))
    print(options, primary)
    if primary is not None:
        options.remove(primary)
    options = list(sorted(filter(lambda s: s.name().split('.')[1] == 'n', options)))

    if len(options) == 0:
        print("Skipped")
        return

    print_term_synsets(term, primary, options)

    key = input()
    try:
        idx = int(key)
        term_synsets[term] = options[idx].name()
        print("Selected " + options[idx].name())
    except:
        term_synsets[term] = primary.name()
        print("Invalid input")


def main():
    with open(TERM_PRIMARY_SYNSETS_PATH, 'r') as f:
        term_synsets = yaml.safe_load(f)
    term_synsets = term_synsets if term_synsets is not None else dict()

    i = 1 if len(sys.argv) == 1 else int(sys.argv[1])
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
