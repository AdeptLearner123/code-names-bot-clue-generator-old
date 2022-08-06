import sys

from code_names_bot_clue_generator.clues.clues_database import CluesDatabase
from config import HYPERNYM_SCORES_PATH


def main():
    scores_database = CluesDatabase(HYPERNYM_SCORES_PATH)

    clues = scores_database.get_top_clues(sys.argv[1], 20)

    for clue, score, type, reason in clues:
        print(clue, score, type, reason)


if __name__ == "__main__":
    main()
