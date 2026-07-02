# MAGIk Autoresearch

This is an autoresearch-style experiment for MAGIk sensor scheduling with
mobile sensors.

## Setup

The repository mirrors the original autoresearch layout:

- `prepare.py`: fixed benchmark scenarios, sensor/environment model, mobility
  constraints, coverage/connectivity evaluation, and result reporting. Do not
  modify this during experiments.
- `train.py`: the solver. Modify this file to improve the algorithm.
- `program.md`: these instructions.
- `benchmark.py`: a thin benchmark entry point that runs `train.py`.
- `MAGIk.py`: compatibility wrapper for older commands.
- `MAGIk_graphs.py`: legacy plotting code from the source repository.

## Objective

The benchmark is least active sensors.

Lower `active_sensors` is better, but only when every benchmark run is feasible.
A feasible run has:

- every grid point covered by at least `k` active sensors
- all active sensors connected through communication range
- every moved active sensor within its `max_mobility` radius

If a change reduces active sensors but makes any run infeasible, discard it.

## Baseline

Run a quick smoke test with:

```bash
python train.py --runs 1 --generations 5
```

Run the benchmark with:

```bash
python train.py --runs 5 --generations 250
```

The final summary prints:

```text
---
feasible:       True
active_sensors: 99.75
```

The score is the average number of active sensors across all benchmark runs.

## Experiment Loop

1. Modify only `train.py`.
2. Run the benchmark.
3. Keep the change only if `feasible` remains `True` and `active_sensors` is
   lower.
4. Prefer simple changes when scores are close.
