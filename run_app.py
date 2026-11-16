"""
run_app.py
==========
Convenience launcher to run the Streamlit DNA Sequence Similarity Checker
directly from the root repository directory.

Usage:
    streamlit run dna_similarity_checker/app.py
    OR
    python run_app.py
"""

import os
import subprocess
import sys

def main():
    script_path = os.path.join(os.path.dirname(__file__), "dna_similarity_checker", "app.py")
    cmd = [sys.executable, "-m", "streamlit", "run", script_path]
    print(f"Launching DNA Sequence Similarity Checker: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\nApplication stopped by user.")

if __name__ == "__main__":
    main()
