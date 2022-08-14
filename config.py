TERMS_PATH = "static/terms.txt"

TRIPLETS_PATH = "static/triplets/"
TRAIN_TRIPLETS_PATH = "static/train_triplets.txt"
TEST_TRIPLETS_PATH = "static/test_triplets.txt"

WIKI = "wiki"
HYPERNYM = "hypernym"

GET_SCORES_PATH = lambda alias: f"output/{alias}_scores.sqlite"
GET_TRAIN_EVAL_REPORT_PATH = lambda alias: f"evaluation_reports/{alias}_train_eval_report.yaml"
GET_TEST_EVAL_REPORT_PATH = lambda alias: f"evaluation_reports/{alias}_test_eval_report.yaml"
