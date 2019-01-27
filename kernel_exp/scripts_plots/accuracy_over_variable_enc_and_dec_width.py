import matplotlib.pyplot as plt
import argparse
import numpy as np
import scipy.stats as stats

parser = argparse.ArgumentParser(description='plot histogram')
parser.add_argument('--jump', type=str)
parser.add_argument('--template', type=str)
parser.add_argument('--random', type=str)

args = vars(parser.parse_args())

jump_lines = []
with open(args['jump']) as f:
    jump_lines = f.readlines()

def get_jump_list(enc):
    if enc == '1':
        return jump_enc_1
    if enc == '2':
        return jump_enc_2
    if enc == '3':
        return jump_enc_3
    if enc == '4':
        return jump_enc_4
    if enc == '5':
        return jump_enc_5

jump_enc_1, jump_enc_2, jump_enc_3, jump_enc_4, jump_enc_5 = [], [], [], [], []
for i, elem in enumerate(jump_lines):
    jump_enc_list = get_jump_list(elem.split('enc_')[1][0])
    dec_value = int(elem.split('dec_')[1][0])
    accuracy = float(elem.split('avg accuracy across seeds: ')[1].split(',')[0])
    jump_enc_list.append((dec_value, accuracy))
    jump_enc_list.sort(key=lambda x : x[0])

jump_enc_1 = [elem[1] for elem in jump_enc_1]
jump_enc_2 = [elem[1] for elem in jump_enc_2]
jump_enc_3 = [elem[1] for elem in jump_enc_3]
jump_enc_4 = [elem[1] for elem in jump_enc_4]
jump_enc_5 = [elem[1] for elem in jump_enc_5]

t1 = t2 = t3 = t4 = t5 = np.arange(1, 6)

plt.close('all')

plt.figure(1)
plt.xlabel('Decoder kernel width')
plt.ylabel('accuracy')
plt.title("JUMP: Variable kernel width accuracies")
plt.plot(t1, jump_enc_1, label='enc_1', marker='.', color='g')
plt.plot(t2, jump_enc_2, label='enc_2', marker='o', color='b')
plt.plot(t3, jump_enc_3, label='enc_3', marker='x', color='r')
plt.plot(t4, jump_enc_4, label='enc_4', marker='1', color='c')
plt.plot(t5, jump_enc_5, label='enc_5', marker='v', color='m')
plt.legend()

###

random_lines = []
with open(args['random']) as f:
    random_lines = f.readlines()

def get_random_list(enc):
    if enc == '1':
        return random_enc_1
    if enc == '2':
        return random_enc_2
    if enc == '3':
        return random_enc_3
    if enc == '4':
        return random_enc_4
    if enc == '5':
        return random_enc_5

random_enc_1, random_enc_2, random_enc_3, random_enc_4, random_enc_5 = [], [], [], [], []
for i, elem in enumerate(random_lines):
    random_enc_list = get_random_list(elem.split('enc_')[1][0])
    dec_value = int(elem.split('dec_')[1][0])
    accuracy = float(elem.split('avg accuracy across seeds: ')[1].split(',')[0])
    random_enc_list.append((dec_value, accuracy))
    random_enc_list.sort(key=lambda x : x[0])

random_enc_1 = [elem[1] for elem in random_enc_1]
random_enc_2 = [elem[1] for elem in random_enc_2]
random_enc_3 = [elem[1] for elem in random_enc_3]
random_enc_4 = [elem[1] for elem in random_enc_4]
random_enc_5 = [elem[1] for elem in random_enc_5]

plt.figure(2)
plt.xlabel('Decoder kernel width')
plt.ylabel('accuracy')
plt.title("RANDOM: Variable kernel width accuracies")
plt.plot(t1, random_enc_1, label='enc_1', marker='.', color='g')
plt.plot(t2, random_enc_2, label='enc_2', marker='o', color='b')
plt.plot(t3, random_enc_3, label='enc_3', marker='x', color='r')
plt.plot(t4, random_enc_4, label='enc_4', marker='1', color='c')
plt.plot(t5, random_enc_5, label='enc_5', marker='v', color='m')
plt.legend()
#plt.show()

###

template_lines = []
with open(args['template']) as f:
    template_lines = f.readlines()

template_enc_1, template_enc_2, template_enc_3, template_enc_4, template_enc_5 = [], [], [], [], []

def get_template_list(enc):
    if enc == '1':
        return template_enc_1
    if enc == '2':
        return template_enc_2
    if enc == '3':
        return template_enc_3
    if enc == '4':
        return template_enc_4
    if enc == '5':
        return template_enc_5

for i, elem in enumerate(template_lines):
    template_enc_list = get_template_list(elem.split('enc_')[1][0])
    dec_value = int(elem.split('dec_')[1][0])
    accuracy = float(elem.split('avg accuracy across seeds: ')[1].split(',')[0])
    template_enc_list.append((dec_value, accuracy))
    template_enc_list.sort(key=lambda x : x[0])

template_enc_1 = [elem[1] for elem in template_enc_1]
template_enc_2 = [elem[1] for elem in template_enc_2]
template_enc_3 = [elem[1] for elem in template_enc_3]
template_enc_4 = [elem[1] for elem in template_enc_4]
template_enc_5 = [elem[1] for elem in template_enc_5]

plt.figure(3)
plt.xlabel('Decoder kernel width')
plt.ylabel('accuracy')
plt.title("TEMPLATE: Variable kernel width accuracies")
plt.plot(t1, template_enc_1, label='enc_1', marker='.', color='g')
plt.plot(t2, template_enc_2, label='enc_2', marker='o', color='b')
plt.plot(t3, template_enc_3, label='enc_3', marker='x', color='r')
plt.plot(t4, template_enc_4, label='enc_4', marker='1', color='c')
plt.plot(t5, template_enc_5, label='enc_5', marker='v', color='m')
plt.legend()
plt.show()

