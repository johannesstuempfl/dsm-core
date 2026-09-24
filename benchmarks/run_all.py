"""
Convenience runner: runs every bm*.py script in this folder, one after
another, and stops at the first failure. Each script is also fully
self-contained and can be run on its own, e.g.:

    python3 benchmarks/bm1_simply_supported_point_load.py

Run: python3 benchmarks/run_all.py
"""
import subprocess
import sys
from pathlib import Path

benchmark_scripts = sorted(Path(__file__).parent.glob("bm*.py"))

for script in benchmark_scripts:
    print(f"\n--- {script.name} ---")
    subprocess.run([sys.executable, str(script)], check=True)

print("\nAll benchmarks passed.")
