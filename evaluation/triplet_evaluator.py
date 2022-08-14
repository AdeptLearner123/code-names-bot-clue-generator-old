import random

from enum import Enum
import yaml
import os

from config import TRAIN_TRIPLETS_PATH, TEST_TRIPLETS_PATH, TRIPLETS_PATH, HYPERNYM, GET_SCORES_PATH, GET_TRAIN_EVAL_REPORT_PATH, GET_TEST_EVAL_REPORT_PATH
from evaluation.clue_generator import ClueGenerator

from .scenario import ScenarioSet


ALIAS = HYPERNYM

class NoAliasDumper(yaml.Dumper):
    def ignore_aliases(self, data):
        return True


class ScenarioResult(Enum):
    INCORRECT = 0
    SKIPPED = 1
    CORRECT = 2


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


def test_scenario(triplet, clue_generator):
    clue, clue_score, clue_count, clue_terms, clue_reasons = clue_generator.get_best_clue(
        triplet.positive, triplet.negative, triplet.positive + triplet.negative
    )

    scenario_report = {
        "id": triplet.id,
        "pos": triplet.positive,
        "neg": triplet.negative,
        "clue": clue,
        "score": clue_score,
        "count": clue_count,
        "terms": clue_terms,
        "reasons": clue_reasons
    }

    if clue is None or clue_count == 1:
        scenario_report["result"] = ScenarioResult.SKIPPED.name
        return ScenarioResult.SKIPPED, scenario_report

    if clue in triplet.clues:
        scenario_report["result"] = ScenarioResult.CORRECT.name
        return ScenarioResult.CORRECT, scenario_report
    elif clue in triplet.nonclues:
        scenario_report["result"] = ScenarioResult.INCORRECT.name
        return ScenarioResult.INCORRECT, scenario_report

    correct = get_guess(clue, triplet)

    if correct:
        triplet.clues.append(clue)
    else:
        triplet.nonclues.append(clue)

    result = ScenarioResult.CORRECT if correct else ScenarioResult.INCORRECT
    scenario_report["result"] = result.name

    print_clue_details(triplet.positive, triplet.negative, clue, clue_score, clue_count, clue_terms, clue_reasons)

    return result, scenario_report


def print_clue_details(pos_terms, neg_terms, clue, clue_score, clue_count, clue_terms, clue_reasons):
    print(
        f"Clue: {clue}, Score: {clue_score}, count: {clue_count}, terms: {clue_terms}"
    )
    print("--- POSITIVE ---")
    for pos_term in pos_terms:
        if pos_term not in clue_reasons:
            print(pos_term, "NA")
        else:
            print(pos_term, clue_reasons[pos_term]["type"], clue_reasons[pos_term]["reason"])
    print("--- NEGATIVE ---")
    for neg_term in neg_terms:
        if neg_term not in clue_reasons:
            print(neg_term, "NA")
        else:
            print(neg_term, clue_reasons[neg_term]["type"], clue_reasons[neg_term]["reason"])


def get_scenarios_dict():
    all_scenarios = {}
    for file in os.listdir(TRIPLETS_PATH):
        path = os.path.join(TRIPLETS_PATH, file)
        with open(path, 'r') as f:
            triplets = ScenarioSet.from_yaml_obj(yaml.safe_load(f))
            for triplet in triplets.scenarios:
                all_scenarios[triplet.id] = (triplet, triplets, path)
    return all_scenarios


def create_report(is_train, scenarios_dict, clue_generator):
    print("Create report", is_train)
    triplet_ids_path = TRAIN_TRIPLETS_PATH if is_train else TEST_TRIPLETS_PATH
    scenario_ids = list(open(triplet_ids_path, "r").read().splitlines())

    report = {
        "correct_scenarios": [],
        "skipped_scenarios": [],
        "incorrect_scenarios": []
    }
    correct = skipped = incorrect = 0
    total = len(scenario_ids)
    i = 0

    for scenario_id in scenario_ids:
        triplet, scenario_set, path = scenarios_dict[scenario_id]
        i += 1
        print("\n\n")
        print(f"--- Scenario {i} / {total} ---")

        result, scenario_report = test_scenario(triplet, clue_generator)

        if result == ScenarioResult.CORRECT:
            correct += 1
            report["correct_scenarios"].append(scenario_report)
        elif result == ScenarioResult.SKIPPED:
            skipped += 1
            report["skipped_scenarios"].append(scenario_report)
        else:
            incorrect += 1
            report["incorrect_scenarios"].append(scenario_report)

        with open(path, "w") as out_file:
            yaml.dump(
                scenario_set.to_yaml_obj(), out_file, default_flow_style=None, sort_keys=False
            )

    score = correct * 2 + skipped
    avg_score = score / total
    print(f"Correct: {correct}, Skipped: {skipped}, Incorrect: {incorrect}")
    print(f"Avg score: {score} / {total} = {avg_score}")

    report["correct"] = correct
    report["skipped"] = skipped
    report["incorrect"] = incorrect

    eval_path = GET_TRAIN_EVAL_REPORT_PATH(ALIAS) if is_train else GET_TEST_EVAL_REPORT_PATH(ALIAS)
    with open(eval_path, "w") as out_file:
        yaml.dump(
            report, out_file, default_flow_style=None, sort_keys=False, Dumper=NoAliasDumper
        )


def main():
    scenarios_dict = get_scenarios_dict()
    clue_generator = ClueGenerator(GET_SCORES_PATH(ALIAS))
    create_report(True, scenarios_dict, clue_generator)
    create_report(False, scenarios_dict, clue_generator)


if __name__ == "__main__":
    main()
