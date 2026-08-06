import time
import numpy as np
from numba import cuda


@cuda.jit
def vector_add_kernel(a, b, c):
    i = cuda.grid(1)
    if i < c.size:
        c[i] = a[i] + b[i]


if __name__ == "__main__":
    N = 10_000_000
    threads_per_block = 256
    blocks = (N + threads_per_block - 1) // threads_per_block

    print(f"N = {N:,}")
    print(f"Threads per block = {threads_per_block}")
    print(f"Blocks = {blocks}")
    print()

    # Host arrays
    a = np.random.random(N).astype(np.float32)
    b = np.random.random(N).astype(np.float32)

    # Copy input arrays to GPU
    a_d = cuda.to_device(a)
    b_d = cuda.to_device(b)

    # Allocate output array on GPU
    c_d = cuda.device_array_like(a_d)

    # Warm-up launch.
    # The first launch includes JIT compilation overhead.
    # Equivalent CUDA C idea:
    # vector_add_kernel<<<blocks, threads_per_block>>>(a_d, b_d, c_d)
    vector_add_kernel[blocks, threads_per_block](a_d, b_d, c_d)
    cuda.synchronize()

    # Timed launch
    t0 = time.perf_counter()
    vector_add_kernel[blocks, threads_per_block](a_d, b_d, c_d)
    cuda.synchronize()
    t1 = time.perf_counter()

    # Copy result back to CPU
    c = c_d.copy_to_host()

    print(f"GPU kernel time: {t1 - t0:.6f} s")
    print("Result correct:", np.allclose(c, a + b))

