"""Run a Python script with CPU 0 left free for system tasks.

Usage: python tools/run_reserved.py <script.py> [args...]

Sets this process's CPU affinity to every logical CPU except CPU 0, then runs the
script in-process (runpy). Child processes (multiprocessing pools, subprocesses)
inherit the affinity. Also exports RESERVED_WORKERS = (logical CPUs - 1) for
scripts that size their worker pools.
"""
import ctypes
import os
import runpy
import sys


def reserve_cpu0():
    n = os.cpu_count() or 1
    if n < 2:
        return 1
    if os.name == "nt":
        from ctypes import wintypes
        k = ctypes.WinDLL("kernel32", use_last_error=True)
        k.GetCurrentProcess.restype = wintypes.HANDLE
        k.SetProcessAffinityMask.argtypes = [wintypes.HANDLE, ctypes.c_size_t]
        k.GetProcessAffinityMask.argtypes = [wintypes.HANDLE, ctypes.POINTER(ctypes.c_size_t),
                                             ctypes.POINTER(ctypes.c_size_t)]
        h = k.GetCurrentProcess()
        proc, system = ctypes.c_size_t(), ctypes.c_size_t()
        k.GetProcessAffinityMask(h, ctypes.byref(proc), ctypes.byref(system))
        if not k.SetProcessAffinityMask(h, system.value & ~1):
            raise OSError(ctypes.get_last_error(), "SetProcessAffinityMask failed")
    elif hasattr(os, "sched_setaffinity"):
        os.sched_setaffinity(0, set(range(1, n)))
    return n - 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    workers = reserve_cpu0()
    os.environ["RESERVED_WORKERS"] = str(workers)
    print(f"[run_reserved] CPU 0 reserved; {workers} logical CPUs available", file=sys.stderr)
    script, sys.argv = sys.argv[1], sys.argv[1:]
    runpy.run_path(script, run_name="__main__")
