import random

import yaml
import uuid

from config import TRAIN_TRIPLETS_PATH, TEST_TRIPLETS_PATH, TERMS_PATH

from .scenario import Scenario, ScenarioSet


class NoAliasDumper(yaml.Dumper):
    def ignore_aliases(self, data):
        return True


def prune_positive_terms(terms, triplets_set):
    remaining_terms = set(terms)
    for triplet in triplets_set.scenarios:
        remaining_terms = remaining_terms - set(triplet.positive)
    return list(remaining_terms)


def print_options_list(options):
    for i in range(len(options)):
        print(f"[{i}] {options[i]}")


def main():
    terms = list(open(TERMS_PATH, "r").read().splitlines())

    with open(TEST_TRIPLETS_PATH, "r") as in_file:
        evaluation_triplets = ScenarioSet.from_yaml_obj(yaml.safe_load(in_file))

    pruned_terms = prune_positive_terms(terms, evaluation_triplets)

    while len(pruned_terms) > 0:
        positive_options = random.sample(pruned_terms, min(len(pruned_terms), 9))
        negative_terms = random.sample(list(set(terms) - set(positive_options)), 6)

        print(f"Choosing from {len(pruned_terms)}")
        print("--- POSITIVE ---")
        print_options_list(positive_options)
        print()
        print("--- NEGATIVE ---")
        print_options_list(negative_terms)

        print("Choose first positive term")
        positive_idx_1 = int(input())
        print("Choose second positive term")
        positive_idx_2 = int(input())
        print("Enter clue")
        clue = str(input()).upper()

        new_scenario = Scenario(
            uuid.uuid4(),
            [positive_options[positive_idx_1], positive_options[positive_idx_2]],
            negative_terms,
            [clue],
        )
        evaluation_triplets.scenarios.append(new_scenario)
        pruned_terms = list(set(pruned_terms) - set(new_scenario.positive))

        with open(TEST_TRIPLETS_PATH, "w") as out_file:
            yaml.dump(
                evaluation_triplets.to_yaml_obj(),
                out_file,
                sort_keys=False,
                default_flow_style=None,
                Dumper=NoAliasDumper,
            )


if __name__ == "__main__":
    main()
