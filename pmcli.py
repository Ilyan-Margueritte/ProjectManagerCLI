#!/usr/bin/env python3
"""
Shim to maintain compatibility with the user's existing `pmcli` command.
This delegates to the new modular architecture.
"""
import sys
import os

# Ensure the local pmcli package is on the path (since we're running the script directly)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pmcli.cli import main

if __name__ == "__main__":
    main()