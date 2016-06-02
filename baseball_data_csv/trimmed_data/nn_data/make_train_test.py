import csv
import random

data_x = open("data_x.csv", "w")
test_x = open("test_x.csv", "w")

data_y = open("data_y.csv", "w")
test_y = open("test_y.csv", "w")

with open("../data.csv") as f:
    data_lines = f.readlines()
    label_lines = open("../data_labels.csv").readlines()
    
    for idx, val in enumerate(data_lines):
        if (idx == 0): # header goes to both files
            data_x.write(val)
            test_x.write(val)
            data_y.write(label_lines[idx])
            test_y.write(label_lines[idx])
        else:
            r = random.random()
            if (r < 0.8):
                data_x.write(val)
                data_y.write(label_lines[idx])
            else:
                test_x.write(val)
                test_y.write(label_lines[idx])

