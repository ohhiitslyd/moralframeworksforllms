"""Run a Python script with low-numbered CPUs left free for system tasks.

Usage: python tools/run_reserved.py <script.py> [args...]

Reserved CPUs come from env RESERVED_CPUS (comma list), default "0,1,2,3": the
owner's rule for Step 0.5, 1, 1.5, 2 and 3 analytics jobs. Sets this process's CPU affinity to
every other logical CPU, then runs the script in-process (runpy). Child processes (multiprocessing pools, subprocesses)
inherit the affinity. Also exports RESERVED_WORKERS = (usable logical CPUs) for
scripts that size their worker pools.
"""
import ctypes
import os
import runpy
import sys


def reserved_set(n):
    raw = os.environ.get("RESERVED_CPUS", "0,1,2,3")
    keep = {int(x) for x in raw.split(",") if x.strip()}
    keep = {c for c in keep if 0 <= c < n}
    if len(keep) >= n:  # never reserve everything
        keep = {0} if n > 1 else set()
    return keep


def reserve_cpus():
    n = os.cpu_count() or 1
    reserved = reserved_set(n)
    usable = [c for c in range(n) if c not in reserved]
    mask_out = sum(1 << c for c in reserved)
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
        if not k.SetProcessAffinityMask(h, system.value & ~mask_out):
            raise OSError(ctypes.get_last_error(), "SetProcessAffinityMask failed")
    elif hasattr(os, "sched_setaffinity"):
        os.sched_setaffinity(0, set(usable))
    return len(usable), sorted(reserved)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    workers, reserved = reserve_cpus()
    os.environ["RESERVED_WORKERS"] = str(workers)
    print(f"[run_reserved] CPUs {reserved} reserved; {workers} logical CPUs available", file=sys.stderr)
    script, sys.argv = sys.argv[1], sys.argv[1:]
    runpy.run_path(script, run_name="__main__")
