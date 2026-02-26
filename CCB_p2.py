"""
Problem 2: Lambda Phage – Stealth vs Hijack
Sweeps MOI from 1 to 10, runs aleae for each, outputs probabilities to q2_results.txt.
"""

import subprocess
import re
import os

BASE_DIR = os.path.join(os.path.dirname(__file__), 'vanilla')
ALEAE    = os.path.join(BASE_DIR, 'aleae')
IN_FILE  = os.path.join(BASE_DIR, 'lambda.in')
R_FILE   = os.path.join(BASE_DIR, 'lambda.r')
TRIALS   = 1000

# Read the template .in file
with open(IN_FILE) as f:
    template = f.read()

results = []

print(f"Running {TRIALS} trials per MOI value (1-10)...\n")

for moi in range(1, 11):
    # Create temp .in with modified MOI
    modified = re.sub(r'^MOI \d+', f'MOI {moi}', template, flags=re.MULTILINE)
    tmp_in = f'/tmp/lambda_moi{moi}.in'
    with open(tmp_in, 'w') as f:
        f.write(modified)

    # Run aleae
    result = subprocess.run(
        [ALEAE, tmp_in, R_FILE, str(TRIALS), '-1', '0'],
        capture_output=True, text=True, timeout=600
    )

    # Parse output
    stealth = hijack = 0
    for line in result.stdout.split('\n'):
        m = re.search(r'cI2 >= 145:\s+(\d+)', line)
        if m: stealth = int(m.group(1))
        m = re.search(r'Cro2 >= 55:\s+(\d+)', line)
        if m: hijack = int(m.group(1))

    pr_s = stealth / TRIALS
    pr_h = hijack / TRIALS
    results.append((moi, pr_s, pr_h, stealth, hijack))
    print(f"  MOI={moi:>2}  Pr(stealth)={pr_s:.4f}  Pr(hijack)={pr_h:.4f}")

# Write results to file
out_path = os.path.join(os.path.dirname(__file__), 'q2_results.txt')
with open(out_path, 'w') as f:
    f.write(f"Lambda Phage: Stealth vs Hijack ({TRIALS} trials per MOI)\n")
    f.write(f"Stealth = cI2 >= 145  |  Hijack = Cro2 >= 55\n\n")
    f.write(f"{'MOI':>4}  {'Pr(stealth)':>12}  {'Pr(hijack)':>12}  {'Stealth':>10}  {'Hijack':>10}\n")
    f.write("-" * 60 + "\n")
    for moi, pr_s, pr_h, s, h in results:
        f.write(f"{moi:>4}  {pr_s:>12.4f}  {pr_h:>12.4f}  {s:>10}  {h:>10}\n")

print(f"\nResults written to {out_path}")
