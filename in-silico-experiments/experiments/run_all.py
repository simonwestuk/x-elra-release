"""Reproduce the entire X-ELRA evaluation: tests, model check, studies, samples.

Run: python3 experiments/run_all.py
Outputs land in results/ (JSON), sample_traces/ (JSON), and figures/ (after
running make_figures.py).
"""

from __future__ import annotations

import importlib
import os
import subprocess
import sys

THIS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(THIS)
sys.path.insert(0, ROOT)
sys.path.insert(0, THIS)


def sh(cmd):
    print(f"\n$ {cmd}")
    subprocess.run(cmd, shell=True, check=True)


def main():
    os.chdir(ROOT)   # robust to being invoked from experiments/ or the root
    # Verification first.
    sh(f"{sys.executable} tests/test_determinism.py")
    sh(f"{sys.executable} tests/test_boundedness.py")
    sh(f"{sys.executable} tests/verify_properties.py")
    sh(f"{sys.executable} tests/test_adapter_regression.py")
    # Studies.
    for mod in ("study1_oscillation", "study2_audit", "study3_sensitivity",
                "study4_robustness", "study5_latency_fairness",
                "study6_fairness", "gen_samples"):
        print(f"\n===== {mod} =====")
        m = importlib.import_module(mod)
        m.main()
    print("\nAll studies complete. Run experiments/make_figures.py to (re)generate figures.")


if __name__ == "__main__":
    main()
