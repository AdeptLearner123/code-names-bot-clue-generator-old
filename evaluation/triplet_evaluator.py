import random

import yaml

from code_names_bot_clue_generator.config import EVALUATION_TRIPLETS_PATH
from evaluation.clue_generator import (best_clue, explore_clue)

from .scenario import ScenarioSet


def get_guess(clue, triplet):
    words = triplet.positive + triplet.negative
    random.shuffle(words)
    for i in range(len(words)):
        print(f"[{i}] {words[i]}")
    print(f"Clue: {clue}")

    try:
        print("Guess 1")
        guess1 = int(input())
        print("Guess 2")
        guess2 = int(input())
    except ValueError:
        return False

    return words[guess1] in triplet.positive and words[guess2] in triplet.positive


def main():
    with open(EVALUATION_TRIPLETS_PATH, "r") as in_file:
        evaluation_triplets = ScenarioSet.from_yaml_obj(yaml.safe_load(in_file))

    score = 0
    total = len(evaluation_triplets.scenarios)
    i = 0
    for triplet in evaluation_triplets.scenarios:
        i += 1
        clue, clue_score, clue_count, clue_terms = best_clue(
            triplet.positive, triplet.negative, 1, triplet.positive + triplet.negative
        )[0]

        if clue in triplet.clues:
            score += 2
            continue
        elif (
            clue_count == 1
        ):  # If model only clues for 1, it will almost always be guessed correctly
            print("Clued for 1, skipping")
            score += 1
            continue
        elif clue in triplet.nonclues:
            continue

        print("\n\n")
        print(f"--- Scenario {i} / {total} ---")
        correct = get_guess(clue, triplet)

        print()
        print("CORRECT" if correct else "INCORRECT")
        print()

        print(
            f"Clue: {clue}, Score: {clue_score}, count: {clue_count}, terms: {clue_terms}"
        )
        explore_clue(clue, triplet.positive, triplet.negative)
        print()

        if correct:
            score += 2
            triplet.clues.append(clue)
        else:
            triplet.nonclues.append(clue)

        with open(EVALUATION_TRIPLETS_PATH, "w") as out_file:
            yaml.dump(
                evaluation_triplets.to_yaml_obj(), out_file, default_flow_style=None
            )

    accuracy = score / total
    print(f"Accuracy: {score} / {total} = {accuracy}")


if __name__ == "__main__":
    main()
