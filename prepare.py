"""
Fixed MAGIk benchmark utilities.

This file plays the same role as autoresearch's prepare.py: it owns the
benchmark scenarios, sensor/environment model, and evaluation metric. The
experiment loop should treat this file as read-only and modify train.py.
"""

from __future__ import annotations

import copy
import math
import random
from dataclasses import dataclass
from statistics import mean
from typing import Callable

import numpy as np


@dataclass(frozen=True)
class Scenario:
    name: str
    k: int
    num_sensors: int
    sensing_range: float
    com_range: float
    width: int
    height: int
    max_mobility: float


@dataclass
class Sensor:
    x: float
    y: float
    sensing_range: float
    com_range: float
    active: bool = True
    max_mobility: float = 0.0
    home_x: float | None = None
    home_y: float | None = None

    def __post_init__(self) -> None:
        if self.home_x is None:
            self.home_x = self.x
        if self.home_y is None:
            self.home_y = self.y

    def move(self, dx: float, dy: float, width: int, height: int) -> None:
        """Move, clamping to the RoI and this sensor's mobility budget."""
        nx = min(max(self.x + dx, 0.0), width - 1)
        ny = min(max(self.y + dy, 0.0), height - 1)
        hx, hy = float(self.home_x), float(self.home_y)
        dist = math.hypot(nx - hx, ny - hy)
        if self.max_mobility > 0 and dist > self.max_mobility:
            scale = self.max_mobility / dist
            nx = hx + (nx - hx) * scale
            ny = hy + (ny - hy) * scale
        self.x = min(max(nx, 0.0), width - 1)
        self.y = min(max(ny, 0.0), height - 1)

    def movement_distance(self) -> float:
        return math.hypot(self.x - float(self.home_x), self.y - float(self.home_y))

    def covers(self, px: int, py: int) -> bool:
        return math.hypot(self.x - px, self.y - py) <= self.sensing_range

    def is_neighbor(self, other: "Sensor") -> bool:
        return math.hypot(self.x - other.x, self.y - other.y) <= self.com_range


class Environment:
    def __init__(self, width: int, height: int, sensors: list[Sensor] | None = None):
        self.width = width
        self.height = height
        self.sensor_list = sensors or []

    @property
    def active_sensors(self) -> list[Sensor]:
        return [sensor for sensor in self.sensor_list if sensor.active]

    @property
    def active_sensor_count(self) -> int:
        return len(self.active_sensors)

    def clone(self) -> "Environment":
        return copy.deepcopy(self)

    def coverage_grid(self) -> np.ndarray:
        grid = np.zeros((self.height, self.width), dtype=np.uint16)
        for sensor in self.active_sensors:
            min_y = max(0, int(math.floor(sensor.y - sensor.sensing_range)))
            max_y = min(self.height - 1, int(math.ceil(sensor.y + sensor.sensing_range)))
            min_x = max(0, int(math.floor(sensor.x - sensor.sensing_range)))
            max_x = min(self.width - 1, int(math.ceil(sensor.x + sensor.sensing_range)))
            for y in range(min_y, max_y + 1):
                for x in range(min_x, max_x + 1):
                    if sensor.covers(x, y):
                        grid[y, x] += 1
        return grid


@dataclass
class SolutionMetrics:
    active_sensors: int
    coverage_rate: float
    k_coverage_rate: float
    connectivity_rate: float
    feasible: bool
    average_movement: float

    def rank_key(self) -> tuple[float, float, float, float, float]:
        """Higher is better; feasible low-active solutions dominate."""
        return (
            1.0 if self.feasible else 0.0,
            self.k_coverage_rate,
            self.connectivity_rate,
            -float(self.active_sensors),
            -self.average_movement,
        )


@dataclass
class BenchmarkResult:
    scenario: str
    run: int
    feasible: bool
    active_sensors: int
    k_coverage_rate: float
    connectivity_rate: float
    average_movement: float


DEFAULT_SCENARIOS = [
    Scenario("small-k2-mobile", 2, 100, 10, 20, 50, 50, 5),
    Scenario("small-k3-mobile", 3, 100, 10, 20, 50, 50, 5),
    Scenario("medium-k2-mobile", 2, 300, 15, 30, 100, 100, 8),
    Scenario("medium-k3-mobile", 3, 300, 15, 30, 100, 100, 8),
]


def make_initial_environment(scenario: Scenario, seed: int, max_attempts: int = 200) -> Environment:
    rng = random.Random(seed)
    best_env = None
    best_metrics = None
    for _ in range(max_attempts):
        positions = set()
        sensors = []
        while len(sensors) < scenario.num_sensors:
            x = rng.randint(0, scenario.width - 1)
            y = rng.randint(0, scenario.height - 1)
            if (x, y) in positions:
                continue
            positions.add((x, y))
            sensors.append(
                Sensor(
                    x,
                    y,
                    scenario.sensing_range,
                    scenario.com_range,
                    active=True,
                    max_mobility=scenario.max_mobility,
                )
            )
        env = Environment(scenario.width, scenario.height, sensors)
        metrics = evaluate_solution(env, scenario.k)
        if best_metrics is None or metrics.rank_key() > best_metrics.rank_key():
            best_env, best_metrics = env, metrics
        if metrics.feasible:
            return env
    return best_env


def calculate_connectivity_rate(sensors: list[Sensor]) -> float:
    active = [sensor for sensor in sensors if sensor.active]
    if not active:
        return 0.0

    graph = {idx: [] for idx in range(len(active))}
    for i, sensor in enumerate(active):
        for j in range(i + 1, len(active)):
            if sensor.is_neighbor(active[j]):
                graph[i].append(j)
                graph[j].append(i)

    visited = set()
    stack = [0]
    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        stack.extend(neighbor for neighbor in graph[current] if neighbor not in visited)
    return len(visited) / len(active)


def evaluate_solution(environment: Environment, k: int) -> SolutionMetrics:
    grid = environment.coverage_grid()
    active = environment.active_sensors
    coverage_rate = float((grid > 0).mean())
    k_coverage_rate = float(np.minimum(grid, k).sum() / (environment.width * environment.height * k))
    connectivity_rate = calculate_connectivity_rate(environment.sensor_list)
    feasible = bool(np.all(grid >= k) and connectivity_rate == 1.0)
    average_movement = sum(sensor.movement_distance() for sensor in active) / max(1, len(active))
    return SolutionMetrics(
        active_sensors=len(active),
        coverage_rate=coverage_rate,
        k_coverage_rate=k_coverage_rate,
        connectivity_rate=connectivity_rate,
        feasible=feasible,
        average_movement=average_movement,
    )


def run_benchmark(
    solve_fn: Callable[[Scenario, int, int], tuple[Environment, SolutionMetrics]],
    runs: int,
    generations: int,
    seed: int,
    scenarios: list[Scenario] | None = None,
) -> list[BenchmarkResult]:
    results = []
    for scenario in scenarios or DEFAULT_SCENARIOS:
        for run in range(runs):
            _, metrics = solve_fn(scenario, seed + run, generations)
            results.append(
                BenchmarkResult(
                    scenario=scenario.name,
                    run=run,
                    feasible=metrics.feasible,
                    active_sensors=metrics.active_sensors,
                    k_coverage_rate=metrics.k_coverage_rate,
                    connectivity_rate=metrics.connectivity_rate,
                    average_movement=metrics.average_movement,
                )
            )
    return results


def summarize_score(results: list[BenchmarkResult]) -> tuple[bool, float]:
    feasible = all(result.feasible for result in results)
    if not feasible:
        return False, float("inf")
    return True, mean(result.active_sensors for result in results)


def print_results(results: list[BenchmarkResult]) -> None:
    print(
        "scenario\trun\tfeasible\tactive_sensors\tk_coverage_rate\t"
        "connectivity_rate\taverage_movement"
    )
    for result in results:
        print(
            f"{result.scenario}\t{result.run}\t{result.feasible}\t"
            f"{result.active_sensors}\t{result.k_coverage_rate:.4f}\t"
            f"{result.connectivity_rate:.4f}\t{result.average_movement:.2f}"
        )
    feasible, score = summarize_score(results)
    print("---")
    print(f"feasible:       {feasible}")
    print(f"active_sensors: {score:.2f}")
