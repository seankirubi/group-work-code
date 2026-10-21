"""
BIT 2118: Scientific Computing
Master Runner & Verification Script
Executes all base tasks (02-20) and modified tasks (02-20),
capturing outputs and generating all figures.
"""

import sys
import os
import glob
import subprocess

def run_script(script_path):
    print(f"\n{'='*70}")
    print(f"RUNNING: {os.path.basename(script_path)}")
    print(f"{'='*70}")
    env = os.environ.copy()
    env["MPLBACKEND"] = "Agg" # Prevent GUI window popups during batch execution
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, env=env)
    if result.returncode != 0:
        print(f"ERROR: {script_path} failed with code {result.returncode}")
        print("STDERR:\n", result.stderr)
        return False, result.stdout, result.stderr
    else:
        print("SUCCESS!")
        print("OUTPUT:\n", result.stdout.strip())
        return True, result.stdout, result.stderr

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    code_dir = os.path.join(base_dir, "code")
    mod_dir = os.path.join(base_dir, "modified")
    os.makedirs(os.path.join(base_dir, "figures"), exist_ok=True)
    
    base_scripts = sorted(glob.glob(os.path.join(code_dir, "Task_*.py")))
    mod_scripts = sorted(glob.glob(os.path.join(mod_dir, "Task_*.py")))
    
    print(f"Found {len(base_scripts)} Base Task Scripts.")
    print(f"Found {len(mod_scripts)} Modified Task Scripts.")
    
    failures = []
    
    print("\n--- STAGE 1: EXECUTING BASE TASKS (02 TO 20) ---")
    for script in base_scripts:
        success, _, _ = run_script(script)
        if not success:
            failures.append(script)
            
    print("\n--- STAGE 2: EXECUTING MODIFIED TASKS (02 TO 20) ---")
    for script in mod_scripts:
        success, _, _ = run_script(script)
        if not success:
            failures.append(script)
            
    print(f"\n{'='*70}")
    print("VERIFICATION SUMMARY")
    print(f"{'='*70}")
    if not failures:
        print(f"ALL {len(base_scripts) + len(mod_scripts)} SCRIPTS COMPLETED SUCCESSFULLY (100% PASS RATE)!")
    else:
        print(f"{len(failures)} script(s) failed:")
        for f in failures:
            print(f" - {f}")

if __name__ == "__main__":
    main()
