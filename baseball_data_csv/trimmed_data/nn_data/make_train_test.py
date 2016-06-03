import csv
import random

data_x = open("data_x.csv", "w")
test_x = open("test_x.csv", "w")

data_y = open("data_y.csv", "w")
test_y = open("test_y.csv", "w")

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
            if (idx in train_row_idx):
                data_x.write(val)
                data_y.write(label_lines[idx])
            else:
                test_x.write(val)
                test_y.write(label_lines[idx])

