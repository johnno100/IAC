# tools/validators/check_connectivity.sh
#!/bin/bash
# Script to check connectivity between all hosts in inventory

hosts=("$@")
echo "Connectivity matrix for ${#hosts[@]} hosts:"
echo "==============================================="
printf "%-20s" " "
for dest in "${hosts[@]}"; do
    printf "%-10s" "$dest"
done
echo ""

for src in "${hosts[@]}"; do
    printf "%-20s" "$src"
    for dest in "${hosts[@]}"; do
        if [ "$src" == "$dest" ]; then
            printf "%-10s" "self"
        else
            ping -c 1 -W 1 "$dest" >/dev/null 2>&1
            if [ $? -eq 0 ]; then
                printf "%-10s" "OK"
            else
                printf "%-10s" "FAIL"
            fi
        fi
    done
    echo ""
done