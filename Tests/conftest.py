import sys
import os

# Ensure the project's PythonSrc directory is on sys.path so tests can import modules
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PYTHONSRC = os.path.join(ROOT, 'PythonSrc')
if PYTHONSRC not in sys.path:
    sys.path.insert(0, PYTHONSRC)
