import os

folder = os.listdir('../Image/resized/')

n = int(len(folder) * 0.9)

train = folder[:n]
valid = folder[n:]

with open ('train_names.txt', 'w') as f:
    for i in train:
        f.write(i + '\n')

with open ('valid_names.txt', 'w') as f:
    for i in valid:
        f.write(i + '\n')
