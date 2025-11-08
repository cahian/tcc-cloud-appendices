"""
Ferramenta de análise dos experimentos
Apêndice E - TCC: Eficiência e Escalabilidade com Cloud Computing
"""

from __future__ import annotations

import csv
import pathlib
import statistics
from collections import defaultdict

DATA_FILE = pathlib.Path(__file__).with_name("experiment_results.csv")


def load_results():
    with open(DATA_FILE, newline="", encoding="utf-8") as handler:
        reader = csv.DictReader(handler)
        rows = []
        for row in reader:
            rows.append(
                {
                    "framework": row["framework"],
                    "dataset_gb": float(row["dataset_gb"]),
                    "nodes": int(row["nodes"]),
                    "time_min": float(row["time_min"]),
                    "cost_usd": float(row["cost_usd"]),
                    "throughput_gbps": float(row["throughput_gbps"]),
                }
            )
        return rows


def best_framework_per_dataset(rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["dataset_gb"]].append(row)

    best = {}
    for dataset, results in grouped.items():
        best_result = min(results, key=lambda r: r["time_min"])
        best[dataset] = best_result

    return best


def aggregate_metrics(rows):
    metrics = defaultdict(lambda: {"time": [], "cost": [], "throughput": []})
    for row in rows:
        label = row["framework"]
        metrics[label]["time"].append(row["time_min"])
        metrics[label]["cost"].append(row["cost_usd"])
        metrics[label]["throughput"].append(row["throughput_gbps"])
    return metrics


def main():
    rows = load_results()
    print("=" * 72)
    print("RELATÓRIO EXPERIMENTAL - APÊNDICE E")
    print("=" * 72)
    print(f"Total de execuções catalogadas: {len(rows)}")

    best = best_framework_per_dataset(rows)
    print("\nMelhor framework por dataset (menor tempo):")
    for dataset in sorted(best.keys()):
        result = best[dataset]
        print(
            f"- {int(dataset)}GB: {result['framework']} "
            f"({result['time_min']} min, throughput {result['throughput_gbps']} GB/s)"
        )

    aggregates = aggregate_metrics(rows)
    print("\nEstatísticas por framework:")
    for framework, values in aggregates.items():
        avg_time = statistics.mean(values["time"])
        avg_cost = statistics.mean(values["cost"])
        avg_tp = statistics.mean(values["throughput"])
        print(
            f"- {framework.capitalize():9s} | "
            f"Tempo médio: {avg_time:.2f} min | "
            f"Custo médio: ${avg_cost:.2f} | "
            f"Throughput médio: {avg_tp:.2f} GB/s"
        )

    overall_tp = statistics.mean(row["throughput_gbps"] for row in rows)
    print(f"\nThroughput médio global: {overall_tp:.2f} GB/s")
    print("=" * 72)


if __name__ == "__main__":
    main()
