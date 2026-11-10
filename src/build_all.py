#!/usr/bin/env python3
"""Compatibility wrapper for the reorganized project layout."""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ROOT_BUILD = REPO_ROOT / 'build_all.py'

if __name__ == '__main__':
    subprocess.run([sys.executable, str(ROOT_BUILD), *sys.argv[1:]], cwd=str(REPO_ROOT), check=True)
