import csv
import random
import math

data_x = open("data_x.csv", "w")
test_x = open("test_x.csv", "w")

data_y = open("data_y.csv", "w")
test_y = open("test_y.csv", "w")

# 0: 0
# 1-4HR: 1, 5-9: 2, etc
def createHomeRunBins(homeRuns):
    binDelim = 5
    if (int(homeRuns.strip()) == 0):
        return '0'
    else:
        return str(int(math.ceil(int(homeRuns.strip())/binDelim)) + 1)

with open("../data.csv") as f:
    data_lines = f.readlines()
    label_lines = open("../data_labels.csv").readlines()
    
    train_row_idx = random.sample(range(1, len(data_lines)), 11600)
    
    for idx, val in enumerate(data_lines):
        addHeaders = False
        if (idx == 0): # header goes to both files
            if addHeaders:
                data_x.write(val)
                test_x.write(val)
                data_y.write(label_lines[idx])
                test_y.write(label_lines[idx])
        else:
            label = label_lines[idx]
            if (idx in train_row_idx):
                data_x.write(val)
                data_y.write( createHomeRunBins(label) + '\n')
            else:
                test_x.write(val)
                test_y.write(createHomeRunBins(label) + '\n')

