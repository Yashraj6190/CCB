#!/bin/zsh
# Automates Q3 verification: recompiles aleae, runs all test cases, prints table values.

set -e
cd "$(dirname "$0")/vanilla"

echo "=== Recompiling aleae ==="
make clean && make
echo ""

TRIALS=10000

# ─── Q3a: Z = X * log2(Y) ───
echo "=== Q3a Verification (Z = X₀ · log₂(Y₀)), $TRIALS trials each ==="
printf "%-6s %-6s %-12s %-10s %-10s\n" "X₀" "Y₀" "Expected Z" "Avg Z" "Avg L"
echo "---------------------------------------------------"

q3a_cases=("3 8 9" "4 16 16" "2 32 10" "5 4 10" "1 64 6")

for case in "${q3a_cases[@]}"; do
    X=$(echo $case | cut -d' ' -f1)
    Y=$(echo $case | cut -d' ' -f2)
    EZ=$(echo $case | cut -d' ' -f3)

    sed "s/^Y .*/Y $Y N/" q3a.in | sed "s/^X .*/X $X N/" > q3a_tmp.in
    output=$(./aleae q3a_tmp.in q3a.r $TRIALS -1 0 2>&1)

    # Parse avg line: species order is b,a1,Y,c,Yp,W1,L,X,a2,Lp,Z,W2
    avg_line=$(echo "$output" | grep "^avg \[")
    # Extract L (index 6) and Z (index 10)
    avg_L=$(echo "$avg_line" | sed 's/.*L=\([0-9.]*\).*/\1/')
    avg_Z=$(echo "$avg_line" | sed 's/.*Z=\([0-9.]*\).*/\1/')

    printf "%-6s %-6s %-12s %-10s %-10s\n" "$X" "$Y" "$EZ" "$avg_Z" "$avg_L"
done

echo ""

# ─── Q3b: Y = 2^(log2(X)) ───
echo "=== Q3b Verification (Y = 2^(log₂(X₀))), $TRIALS trials each ==="
printf "%-6s %-14s %-10s %-10s\n" "X₀" "Expected Y=X₀" "Avg Y" "Avg L (W2)"
echo "-------------------------------------------"

q3b_cases=("4" "8" "16" "32")

for X in "${q3b_cases[@]}"; do
    sed "s/^X .*/X $X N/" q3b.in > q3b_tmp.in
    output=$(./aleae q3b_tmp.in q3b.r $TRIALS -1 0 2>&1)

    avg_line=$(echo "$output" | grep "^avg \[")
    # species order: b,a1,X,c,Xp,W1,L,a2,Y,Yp,W2
    avg_Y=$(echo "$avg_line" | sed 's/.*Y=\([0-9.]*\).*/\1/')
    # W2 = number of L triggers consumed = effective log2(X)
    avg_W2=$(echo "$avg_line" | sed 's/.*W2=\([0-9.]*\).*/\1/')

    printf "%-6s %-14s %-10s %-10s\n" "$X" "$X" "$avg_Y" "$avg_W2"
done

echo ""
echo "=== Done ==="
