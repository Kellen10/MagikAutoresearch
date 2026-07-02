"""
MAGIk experiment script.

This file plays the same role as autoresearch's train.py. It contains the
solver that an autonomous experimenter should modify. The fixed benchmark,
scenario generation, and metric live in prepare.py.
"""

from __future__ import annotations

import argparse
import math

import numpy as np

from prepare import (
    DEFAULT_SCENARIOS,
    Environment,
    Scenario,
    SolutionMetrics,
    evaluate_solution,
    make_initial_environment,
    print_results,
    run_benchmark,
)


def covered_points(sensor, width: int, height: int) -> list[tuple[int, int]]:
    points = []
    min_y = max(0, int(math.floor(sensor.y - sensor.sensing_range)))
    max_y = min(height - 1, int(math.ceil(sensor.y + sensor.sensing_range)))
    min_x = max(0, int(math.floor(sensor.x - sensor.sensing_range)))
    max_x = min(width - 1, int(math.ceil(sensor.x + sensor.sensing_range)))
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if sensor.covers(x, y):
                points.append((y, x))
    return points


def communication_neighbors(environment: Environment) -> list[list[int]]:
    sensors = environment.sensor_list
    neighbors = [[] for _ in sensors]
    for i, sensor in enumerate(sensors):
        for j in range(i + 1, len(sensors)):
            if sensor.is_neighbor(sensors[j]):
                neighbors[i].append(j)
                neighbors[j].append(i)
    return neighbors


def connectivity_rate(active: list[bool], neighbors: list[list[int]]) -> float:
    active_count = sum(active)
    if active_count == 0:
        return 0.0

    start = next(index for index, is_active in enumerate(active) if is_active)
    visited = [False] * len(active)
    visited_count = 0
    stack = [start]
    while stack:
        current = stack.pop()
        if visited[current] or not active[current]:
            continue
        visited[current] = True
        visited_count += 1
        stack.extend(index for index in neighbors[current] if active[index] and not visited[index])
    return visited_count / active_count


def fast_metrics(
    active: list[bool],
    coverage: np.ndarray,
    neighbors: list[list[int]],
    k: int,
) -> SolutionMetrics:
    active_count = sum(active)
    connected = connectivity_rate(active, neighbors)
    k_coverage_rate = float(np.minimum(coverage, k).sum() / (coverage.shape[0] * coverage.shape[1] * k))
    feasible = bool(np.all(coverage >= k) and connected == 1.0)
    return SolutionMetrics(
        active_sensors=active_count,
        coverage_rate=float((coverage > 0).mean()),
        k_coverage_rate=k_coverage_rate,
        connectivity_rate=connected,
        feasible=feasible,
        average_movement=0.0,
    )


def one_pass_prune(
    active: list[bool],
    coverage: np.ndarray,
    k: int,
    covered: list[list[tuple[int, int]]],
    reserve: int,
) -> tuple[list[bool], np.ndarray]:
    candidate_active = active.copy()
    candidate_coverage = coverage.copy()
    order = [index for index, is_active in enumerate(candidate_active) if is_active]
    order.sort(
        key=lambda index: (
            min(candidate_coverage[y, x] for y, x in covered[index]),
            sum(float(candidate_coverage[y, x]) for y, x in covered[index]) / max(1, len(covered[index])),
        ),
        reverse=True,
    )

    for index in order:
        points = covered[index]
        if all(candidate_coverage[y, x] > k + reserve for y, x in points):
            candidate_active[index] = False
            for y, x in points:
                candidate_coverage[y, x] -= 1
    return candidate_active, candidate_coverage


def reactivate_tight_batch(
    active: list[bool],
    coverage: np.ndarray,
    k: int,
    covered: list[list[tuple[int, int]]],
    count: int,
) -> tuple[list[bool], np.ndarray]:
    if count <= 0:
        return active, coverage

    candidate_active = active.copy()
    candidate_coverage = coverage.copy()
    inactive = [index for index, is_active in enumerate(candidate_active) if not is_active]
    inactive.sort(
        key=lambda index: sum(1 for y, x in covered[index] if candidate_coverage[y, x] <= k),
        reverse=True,
    )
    for index in inactive[:count]:
        candidate_active[index] = True
        for y, x in covered[index]:
            candidate_coverage[y, x] += 1
    return candidate_active, candidate_coverage


def environment_from_active(base_env: Environment, active: list[bool]) -> Environment:
    environment = base_env.clone()
    for sensor, is_active in zip(environment.sensor_list, active):
        sensor.active = is_active
    return environment


def bounded_candidate_solve(
    scenario: Scenario,
    seed: int,
    generations: int,
) -> tuple[Environment, SolutionMetrics]:
    base_env = make_initial_environment(scenario, seed)
    base_active = [True] * len(base_env.sensor_list)
    base_coverage = base_env.coverage_grid()
    covered = [covered_points(sensor, base_env.width, base_env.height) for sensor in base_env.sensor_list]
    neighbors = communication_neighbors(base_env)
    best_active = base_active
    best_metrics = fast_metrics(base_active, base_coverage, neighbors, scenario.k)

    reactivation_batches = [0, 128, 192] if scenario.k <= 2 else [0, 8, 32, 150]
    for index, batch in enumerate(reactivation_batches):
        active, coverage = one_pass_prune(
            base_active,
            base_coverage,
            scenario.k,
            covered,
            0,
        )
        if batch:
            active, coverage = reactivate_tight_batch(active, coverage, scenario.k, covered, batch)
            active, coverage = one_pass_prune(
                active,
                coverage,
                scenario.k,
                covered,
                0,
            )
        metrics = fast_metrics(active, coverage, neighbors, scenario.k)
        if metrics.rank_key() > best_metrics.rank_key():
            best_active, best_metrics = active, metrics

    best_env = environment_from_active(base_env, best_active)
    best_metrics = evaluate_solution(best_env, scenario.k)
    return best_env, best_metrics


def solve(scenario: Scenario, seed: int, generations: int = 250) -> tuple[Environment, SolutionMetrics]:
    return bounded_candidate_solve(scenario, seed, generations)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the MAGIk least-active-sensors benchmark.")
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--generations", type=int, default=250)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--scenario",
        default="all",
        help="Scenario name substring to run, or 'all' for the full benchmark.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scenarios = None
    if args.scenario != "all":
        scenarios = [scenario for scenario in DEFAULT_SCENARIOS if args.scenario in scenario.name]
        if not scenarios:
            raise SystemExit(f"No scenarios match: {args.scenario}")
    results = run_benchmark(
        solve,
        runs=args.runs,
        generations=args.generations,
        seed=args.seed,
        scenarios=scenarios,
    )
    print_results(results)


if __name__ == "__main__":
    main()
