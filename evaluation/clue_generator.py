from code_names_bot_clue_generator.scores.scores_database import ScoresDatabase
from code_names_bot_clue_generator.config import WIKI_SCORES_PATH

NEGATIVE_THRESHOLD = 2.0


scores_database = ScoresDatabase(WIKI_SCORES_PATH)

def best_clue(pos_terms, neg_terms, count, ignore=[]):
    term_scores = get_term_scores(pos_terms, neg_terms)
    neg_scores = get_neg_scores(neg_terms, term_scores)
    clue_scores, clue_counts, clue_terms = get_clue_scores(
        pos_terms, neg_scores, term_scores
    )
    return get_best_clues(clue_scores, clue_counts, clue_terms, count, ignore)


def get_best_clues(clue_scores, clue_counts, clue_terms, count, ignore=[]):
    clue_scores_list = []
    for clue in clue_scores:
        if clue not in ignore:
            clue_scores_list.append(
                (clue, clue_scores[clue], clue_counts[clue], clue_terms[clue])
            )
    clue_scores_list.sort(key=lambda tup: tup[1], reverse=True)

    return clue_scores_list[:count]


def get_term_scores(pos_terms, neg_terms):
    term_scores = {}
    for term in pos_terms + neg_terms:
        term_scores[term] = scores_database.get_scores(term)
    return term_scores


def get_clue_scores(pos_terms, neg_scores, term_scores):
    clue_scores = {}
    clue_counts = {}
    clue_terms = {}
    for term in pos_terms:
        scores = term_scores[term]
        for clue_option in scores:
            if clue_option in neg_scores and (
                neg_scores[clue_option] >= NEGATIVE_THRESHOLD
                or neg_scores[clue_option] >= scores[clue_option]
            ):
                continue
            if clue_option not in clue_scores:
                clue_scores[clue_option] = 0
                clue_counts[clue_option] = 0
                clue_terms[clue_option] = []
            clue_scores[clue_option] += scores[clue_option]
            clue_counts[clue_option] += 1
            clue_terms[clue_option].append(term)
    return clue_scores, clue_counts, clue_terms


def get_neg_scores(neg_terms, term_scores):
    neg_scores = {}
    for term in neg_terms:
        scores = term_scores[term]
        for clue_option in scores:
            if clue_option not in neg_scores:
                neg_scores[clue_option] = scores[clue_option]
            else:
                neg_scores[clue_option] = max(
                    neg_scores[clue_option], scores[clue_option]
                )
    return neg_scores


def explore_clue(clue, pos_terms, neg_terms):
    print("--- POSITIVE ---")
    for term in pos_terms:
        print_clue_term(term, clue)
    print()
    print("--- NEGATIVE ---")
    for term in neg_terms:
        print_clue_term(term, clue)


def print_clue_term(term, clue):
    score, type, reason = scores_database.get_term_clue(term, clue)
    if score is None:
        print("Term: {0} N/A".format(term))
    else:
        print(
            "Term: {0} Score: {1} Type: {2} Reason: {3}".format(
                term, score, type, reason
            )
        )
