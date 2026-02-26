#!/bin/zsh
# Automates Q2 verification: recompiles aleae, sweeps MOI 1-10, prints stealth/hijack table.

set -e
cd "$(dirname "$0")/vanilla"

echo "=== Recompiling aleae ==="
make clean && make
echo ""

TRIALS=100

echo "=== Q2: Lambda Phage Stealth vs Hijack, $TRIALS trials per MOI ==="
printf "%-6s %-14s %-14s\n" "MOI" "Pr(Stealth)" "Pr(Hijack)"
echo "------------------------------------"

for MOI in $(seq 1 10); do
    # Replace MOI line in lambda.in
    sed "s/^MOI [0-9]*/MOI $MOI/" lambda.in > lambda_tmp.in

    output=$(./aleae lambda_tmp.in lambda.r $TRIALS -1 0 2>&1)

    # Parse threshold lines: "cI2 >= 145: k (p%)" and "Cro2 >= 55: k (p%)"
    stealth=$(echo "$output" | grep "cI2 >= 145:" | sed 's/.*: \([0-9]*\).*/\1/')
    hijack=$(echo "$output" | grep "Cro2 >= 55:" | sed 's/.*: \([0-9]*\).*/\1/')

    pr_s=$(echo "scale=4; $stealth / $TRIALS" | bc)
    pr_h=$(echo "scale=4; $hijack / $TRIALS" | bc)

    printf "%-6s %-14s %-14s\n" "$MOI" "$pr_s" "$pr_h"
done

rm -f lambda_tmp.in
echo ""
echo "=== Done ==="
