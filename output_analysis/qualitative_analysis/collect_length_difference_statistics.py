import numpy as np
import sys

target_out_field = int(sys.argv[1]) - 1
outcome_field = target_out_field + 2
data_file = sys.argv[2]

diffs = []

with open(data_file) as f:
    for line in f:
        F = line.strip().split("\t")
        if (F[outcome_field] == "False"):
            gold_length = len(F[-1].split(" "))
            out_length =  len(F[target_out_field].split(" "))
            diffs.append(out_length-gold_length)

diffs_np=np.asarray(diffs)

print np.mean(diffs_np)
print np.std(diffs_np)

