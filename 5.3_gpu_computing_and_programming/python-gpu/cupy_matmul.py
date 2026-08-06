import time
import numpy as np
import cupy as cp


def time_numpy_matmul(n):
    A = np.random.random((n, n)).astype(np.float32)
    B = np.random.random((n, n)).astype(np.float32)

    t0 = time.perf_counter()
    C = A @ B
    t1 = time.perf_counter()

    return t1 - t0, C[0, 0]


def time_cupy_matmul(n):
    A = cp.random.random((n, n), dtype=cp.float32)
    B = cp.random.random((n, n), dtype=cp.float32)

    cp.cuda.Stream.null.synchronize()
    t0 = time.perf_counter()

    C = A @ B

    cp.cuda.Stream.null.synchronize()
    t1 = time.perf_counter()

    return t1 - t0, float(C[0, 0].get())


if __name__ == "__main__":
    N = 2048

    print(f"Matrix size: {N} x {N}")
    print()

    cpu_time, cpu_value = time_numpy_matmul(N)
    gpu_time, gpu_value = time_cupy_matmul(N)

    print(f"NumPy matrix multiply time: {cpu_time:.6f} s")
    print(f"CuPy matrix multiply time:  {gpu_time:.6f} s")
    print()
    print(f"Example NumPy value C[0,0]: {cpu_value:.6e}")
    print(f"Example CuPy value C[0,0]:  {gpu_value:.6e}")
    print()
    print("Note: Results are not expected to match because NumPy and CuPy use different random matrices.")
