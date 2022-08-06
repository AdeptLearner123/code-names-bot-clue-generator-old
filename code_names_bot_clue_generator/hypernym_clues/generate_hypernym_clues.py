from nltk.corpus import wordnet
from tqdm import tqdm

from code_names_bot_clue_generator.clues.clues_database import CluesDatabase
from config import HYPERNYM_SCORES_PATH, TERMS_PATH


def main():
    scores_database = CluesDatabase(HYPERNYM_SCORES_PATH)
    scores_database.clear()
    scores_database.setup()

    terms = list(open(TERMS_PATH, "r").read().splitlines())
    for term in tqdm(terms):
        _, result_words = get_term_hypernyms(term)
        for clue in result_words:
            depth, path = result_words[clue]

            if "_" not in clue:  # Only single-word clues are valid
                clue = clue.upper()
                scores_database.insert_term_clue(term, clue, 1.0, "HYPERNYM", path)
    scores_database.commit()


def get_term_hypernyms(term):
    queue = []
    result_synsets = dict()

    synsets = wordnet.synsets(term)
    for synset in synsets:
        for hypernym in synset.hypernyms():
            queue.append((hypernym, 1, f"{synset}->{hypernym}"))

    while len(queue) > 0:
        hypernym, depth, path = queue.pop(0)

        if hypernym in result_synsets:
            continue

        result_synsets[hypernym] = (depth, path)

        for parent_hypernym in hypernym.hypernyms():
            queue.append((parent_hypernym, depth + 1, f"{path}->{parent_hypernym}"))

    result_words = dict()
    for hypernym in result_synsets:
        depth, path = result_synsets[hypernym]

        words = map(lambda lemma: lemma.name(), hypernym.lemmas())
        for lemma in words:
            if lemma not in result_words or result_words[lemma][0] > depth:
                result_words[lemma] = (depth, path)

    return result_synsets, result_words


if __name__ == "__main__":
    main()
