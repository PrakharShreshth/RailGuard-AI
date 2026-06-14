import os
from collections import Counter

counter = Counter()

label_folder = r"dataset\train\labels"

for file in os.listdir(label_folder):

    if file.endswith(".txt"):

        with open(os.path.join(label_folder, file), "r") as f:

            for line in f:

                cls = line.split()[0]
                counter[cls] += 1

print(counter)
