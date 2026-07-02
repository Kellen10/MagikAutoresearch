"""
Fixed MAGIk benchmark entry point.

The solver comes from train.py, but scoring and scenarios come from prepare.py.
"""

from __future__ import annotations

from train import main


if __name__ == "__main__":
    main()
