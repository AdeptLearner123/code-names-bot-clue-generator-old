from nltk.corpus import wordnet
from tqdm import tqdm
import yaml

from code_names_bot_clue_generator.clues.clues_database import CluesDatabase
from config import HYPERNYM, GET_SCORES_PATH, TERMS_PATH, TERM_PRIMARY_SYNSETS_PATH


def main():
    scores_database = CluesDatabase(GET_SCORES_PATH(HYPERNYM))
    scores_database.clear()
    scores_database.setup()

    terms = list(open(TERMS_PATH, "r").read().splitlines())
    for term in tqdm(terms):
        hypernym_words = get_hypernym_clues(term)
        for clue in hypernym_words:
            depth, path = hypernym_words[clue]

            if "_" not in clue:  # Only single-word clues are valid
                clue = clue.upper()
                scores_database.insert_term_clue(term, clue, 1.0, "HYPERNYM", "->".join([synset.name() for synset in path]))
    scores_database.commit()


def get_hypernym_clues(term):
    hypernym_synsets = get_primary_hypernyms(term)
    return get_synset_words(hypernym_synsets)


def get_all_hypernyms(term):
    synsets = wordnet.synsets(term)
    return get_synset_hypernyms(synsets)


def get_primary_hypernyms(term):
    with open(TERM_PRIMARY_SYNSETS_PATH, 'r') as f:
        term_synsets = yaml.safe_load(f)
    if term not in term_synsets:
        return dict()
    primary_synset = wordnet.synset(term_synsets[term])
    return get_synset_hypernyms([primary_synset])


def get_synset_hypernyms(synsets):
    queue = []
    result_synsets = dict()
    
    for synset in synsets:
        for hypernym in synset.hypernyms():
            queue.append((hypernym, 1, [synset, hypernym]))

    while len(queue) > 0:
        hypernym, depth, path = queue.pop(0)

        if hypernym in result_synsets:
            continue

        result_synsets[hypernym] = (depth, path)

        for parent_hypernym in hypernym.hypernyms():
            queue.append((parent_hypernym, depth + 1, path + [parent_hypernym]))

    return result_synsets


def get_synset_words(hypernym_synsets):
    result_words = dict()
    for hypernym in hypernym_synsets:
        depth, path = hypernym_synsets[hypernym]
        word = hypernym.name().split(".")[0]
        result_words[word] = (depth, path)
    return result_words


if __name__ == "__main__":
    main()
