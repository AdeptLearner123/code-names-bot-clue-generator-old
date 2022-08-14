from abc import ABC, abstractmethod
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer 
from tqdm import tqdm

from code_names_bot_clue_generator.clues.clues_database import CluesDatabase
from config import HYPERNYM, GET_SCORES_PATH, TERMS_PATH


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
    hypernym_synsets = get_all_hypernyms(term)
    hypernym_synsets = filter_hypernyms(hypernym_synsets)
    return get_synset_words(hypernym_synsets)


def get_all_hypernyms(term):
    queue = []
    result_synsets = dict()

    synsets = wordnet.synsets(term)
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


def filter_hypernyms(hypernym_synsets):
    filtered_synsets = dict()

    obj_synset = wordnet.synsets("object")[0]
    if obj_synset in hypernym_synsets:
        _, path = hypernym_synsets[obj_synset]
        for i in range(len(path) - 1):
            synset = path[i]
            filtered_synsets[synset] = (i + 1, path[:i + 1])

    return filtered_synsets


def get_synset_words(hypernym_synsets):
    result_words = dict()
    for hypernym in hypernym_synsets:
        depth, path = hypernym_synsets[hypernym]

        words = map(lambda lemma: lemma.name(), hypernym.lemmas())
        for lemma in words:
            if lemma not in result_words or result_words[lemma][0] > depth:
                result_words[lemma] = (depth, path)
    return result_words


if __name__ == "__main__":
    main()
