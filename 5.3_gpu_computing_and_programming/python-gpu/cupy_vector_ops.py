import time
import numpy as np
import cupy as cp

def time_numpy(n):
    x = np.random.random(n).astype(np.float32)
    y = np.random.random(n).astype(np.float32)

    t0 = time.perf_counter()
    z = x + y
    result = z.sum()
    t1 = time.perf_counter()

    return t1 - t0, result

def time_cupy(n):
    x = cp.random.random(n, dtype=cp.float32)
    y = cp.random.random(n, dtype=cp.float32)

    cp.cuda.Stream.null.synchronize()
    t0 = time.perf_counter()

    z = x + y
    result = z.sum()

    cp.cuda.Stream.null.synchronize()
    t1 = time.perf_counter()

    return t1 - t0, float(result.get())

if __name__ == "__main__":
    N = 10_000_000

    print(f"N = {N:,}")
    print()

    cpu_time, cpu_result = time_numpy(N)
    gpu_time, gpu_result = time_cupy(N)

    print(f"NumPy time: {cpu_time:.6f} s")
    print(f"CuPy time: {gpu_time:.6f} s")
    print()
    print(f"NumPy result: {cpu_result:.6e}")
    print(f"CuPy result: {gpu_result:.6e}")
    print() print("Note: Results will not be identical because random inputs are generated separately.")
