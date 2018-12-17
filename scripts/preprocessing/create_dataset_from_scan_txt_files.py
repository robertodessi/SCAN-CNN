import argparse
import os

parser = argparse.ArgumentParser(description='Cnn models on SCAN dataset')
parser.add_argument('--train', type=str, required=True)
parser.add_argument('--test', type=str, required=True)
parser.add_argument('--output', type=str, required=True)

args = vars(parser.parse_args())

output_folder = args['output']

in_train = args['train']
in_test = args['test']

out_test_co = os.path.join(output_folder, 'test.co')
out_test_ac = os.path.join(output_folder, 'test.ac'

out_train_co = os.path.join(output_folder, 'train.co')
out_train_ac = os.path.join(output_folder, 'train.ac')

out_valid_co = os.path.join(output_folder, 'valid.co')
out_valid_ac = os.path.join(output_folder, 'valid.ac')

test_co = open(out_test_co, 'w')
test_ac = open(out_test_ac, 'w')

train_co = open(out_train_co, 'w')
train_ac = open(out_train_ac, 'w')

valid_co = open(out_valid_co, 'w')
valid_ac = open(out_valid_ac, 'w')

import random
train_commands = []
with open(in_train) as f:
        train_commands = f.readlines()

for _ in range(100000):
        index = random.randint(0, len(train_commands)-1)
        st_com = train_commands[index].split('OUT')
        train_co.write(st_com[0][4:].strip())
        train_co.write('\n')
        train_ac.write(st_com[1][2:])

with open(in_test) as g:
        for elem in g:
                co, ac = elem.split('OUT: ')
                test_co.write(co[4:].strip())
                test_co.write("\n")
                test_ac.write(ac)

with open('train.ac') as h:
        for i, elem in enumerate(h):
                valid_ac.write(elem)
                if i == 9:
                        break

with open('train.co') as k:
        for i, elem in enumerate(k):
                valid_co.write(elem)
                if i == 9:
                        break

test_co.close()
test_ac.close()
train_co.close()
train_ac.close()
valid_co.close()
valid_ac.close()
