"""Command-line entry point for the skydiving model."""

from __future__ import annotations

import argparse

from .physics import terminal_velocity, time_to_fraction


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Calculate terminal velocity for a skydiver."
    )
    parser.add_argument("--mass", type=float, default=80.0, help="Mass in kilograms")
    parser.add_argument(
        "--drag",
        type=float,
        default=0.26,
        help="Quadratic drag coefficient",
    )
    parser.add_argument(
        "--gravity",
        type=float,
        default=9.81,
        help="Gravitational acceleration in m/s^2",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    limit = terminal_velocity(args.mass, args.drag, args.gravity)
    seconds = time_to_fraction(0.99, args.mass, args.drag, args.gravity)
    print(f"Terminal velocity: {limit:.2f} m/s downward")
    print(f"Time to reach 99% of terminal velocity: {seconds:.2f} s")


if __name__ == "__main__":
    main()
