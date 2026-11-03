"""Quality gate: move the champion alias only to a clearly better model version.

Usage:
    uv run python src/food11/promote.py --version 8
"""
import argparse
import math
import os
import sys

from mlflow.tracking import MlflowClient

MODEL_NAME = "food11"
METRIC = "test_accuracy"
# test_accuracy is measured on the evaluation split of food11_processed_mini
TEST_SIZE = 1096


def accuracy_of(client, version):
    return client.get_run(version.run_id).data.metrics[METRIC]


def main():
    parser = argparse.ArgumentParser(description="Promote a food11 version if it beats the champion")
    parser.add_argument("--version", required=True, help="registered version number of the candidate")
    parser.add_argument("--test-size", type=int, default=TEST_SIZE)
    args = parser.parse_args()

    client = MlflowClient(tracking_uri=os.environ.get("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000"))
    candidate = client.get_model_version(MODEL_NAME, args.version)
    champion = client.get_model_version_by_alias(MODEL_NAME, "champion")
    if candidate.version == champion.version:
        sys.exit(f"version {candidate.version} is already the champion")

    acc_candidate = accuracy_of(client, candidate)
    acc_champion = accuracy_of(client, champion)
    # standard error of the champion's accuracy: how much it could move just by chance
    se = math.sqrt(acc_champion * (1 - acc_champion) / args.test_size)
    threshold = acc_champion + 2 * se

    if acc_candidate >= threshold:
        client.set_registered_model_alias(MODEL_NAME, "champion", candidate.version)
        decision = "promoted"
    else:
        client.set_registered_model_alias(MODEL_NAME, "challenger", candidate.version)
        decision = "challenger"

    tags = {
        "gate_decision": decision,
        "candidate_test_accuracy": f"{acc_candidate:.4f}",
        "champion_test_accuracy": f"{acc_champion:.4f}",
        "champion_version": champion.version,
        "gate_threshold": f"{threshold:.4f}",
    }
    for key, value in tags.items():
        client.set_model_version_tag(MODEL_NAME, candidate.version, key, value)

    print(f"candidate version {candidate.version}: {METRIC} {acc_candidate:.4f}")
    print(f"champion  version {champion.version}: {METRIC} {acc_champion:.4f}")
    print(f"se = sqrt(p(1-p)/n) with n={args.test_size}: {se:.4f}, so 2*se = {2 * se:.4f}")
    if decision == "promoted":
        print(f"needed {threshold:.4f} -> promoted, champion now points to version {candidate.version}")
    else:
        print(f"needed {threshold:.4f} -> not enough, version {candidate.version} becomes the challenger "
              f"and champion stays on version {champion.version}")


if __name__ == "__main__":
    main()
