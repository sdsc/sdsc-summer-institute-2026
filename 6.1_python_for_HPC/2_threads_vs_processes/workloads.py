"""Small, importable workloads for the threads-versus-processes notebook."""

import time


def fib(n: int) -> int:
    """Return Fibonacci number n using deliberately CPU-heavy Python recursion."""
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def sleepy(seconds: float) -> float:
    """Wait for seconds and return the same value."""
    time.sleep(seconds)
    return seconds
