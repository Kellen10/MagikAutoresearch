"""
MAGIk experiment script.

This file plays the same role as autoresearch's train.py. It contains the
solver that an autonomous experimenter should modify. The fixed benchmark,
scenario generation, and metric live in prepare.py.
"""

from __future__ import annotations

import argparse
import math
import random

from prepare import (
    Environment,
    Scenario,
    SolutionMetrics,
    evaluate_solution,
    make_initial_environment,
    print_results,
    run_benchmark,
)


def mutate_environment(
    environment: Environment,
    rng: random.Random,
    mutation_rate: float,
    mobility_step: float,
) -> Environment:
    mutated = environment.clone()
    count = max(1, math.ceil(len(mutated.sensor_list) * mutation_rate))
    for sensor in rng.sample(mutated.sensor_list, count):
        action = rng.random()
        if action < 0.45:
            sensor.active = not sensor.active
        elif action < 0.9:
            sensor.active = True
            angle = rng.random() * 2 * math.pi
            radius = rng.random() * mobility_step
            sensor.move(math.cos(angle) * radius, math.sin(angle) * radius, mutated.width, mutated.height)
        else:
            sensor.active = True
            sensor.move(
                float(sensor.home_x) - sensor.x,
                float(sensor.home_y) - sensor.y,
                mutated.width,
                mutated.height,
            )
    return mutated


def solve(scenario: Scenario, seed: int, generations: int = 250) -> tuple[Environment, SolutionMetrics]:
    rng = random.Random(seed)
    best_env = make_initial_environment(scenario, seed)
    best_metrics = evaluate_solution(best_env, scenario.k)

    candidates = max(20, 10 * math.ceil(math.log2(scenario.num_sensors + 1)))
    mutation_rate = 0.08
    mobility_step = max(1.0, scenario.max_mobility / 2)

    for generation in range(generations):
        accepted_this_generation = False
        for _ in range(candidates):
            candidate = mutate_environment(best_env, rng, mutation_rate, mobility_step)
            metrics = evaluate_solution(candidate, scenario.k)
            if metrics.rank_key() > best_metrics.rank_key():
                best_env, best_metrics = candidate, metrics
                accepted_this_generation = True

        if (generation + 1) % 25 == 0:
            mutation_rate = max(0.01, mutation_rate * 0.85)
            mobility_step = max(0.5, mobility_step * 0.9)
        if best_metrics.feasible and not accepted_this_generation:
            mutation_rate = max(0.01, mutation_rate * 0.98)

    return best_env, best_metrics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the MAGIk least-active-sensors benchmark.")
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--generations", type=int, default=250)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = run_benchmark(solve, runs=args.runs, generations=args.generations, seed=args.seed)
    print_results(results)


if __name__ == "__main__":
    main()
