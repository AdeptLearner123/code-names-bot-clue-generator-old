import os
import random
import yaml

from .scenario import ScenarioSet

from config import TRIPLETS_PATH, TRAIN_TRIPLETS_PATH, TEST_TRIPLETS_PATH

def main():
    all_triplet_uuids = []

    for file in os.listdir(TRIPLETS_PATH):
        path = os.path.join(TRIPLETS_PATH, file)
        with open(path, 'r') as f:
            triplets = ScenarioSet.from_yaml_obj(yaml.safe_load(f))
        all_triplet_uuids += list(map(lambda scenario: scenario.id, triplets.scenarios))
    
    train_ids = random.sample(all_triplet_uuids, len(all_triplet_uuids) // 2)
    test_ids = list(set(all_triplet_uuids) - set(train_ids))

    with open(TRAIN_TRIPLETS_PATH, 'w') as f:
        for train_id in train_ids:
            f.write(f"{train_id}\n")

    with open(TEST_TRIPLETS_PATH, 'w') as f:
        for test_id in test_ids:
            f.write(f"{test_id}\n")


if __name__ == "__main__":
    main()
