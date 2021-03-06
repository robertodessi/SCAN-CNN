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
    std = float(elem.split('std: ')[1].split(',')[0])
    jump_enc_list.append((dec_value, accuracy, std))
    jump_enc_list.sort(key=lambda x : x[0])

jump_std1 = [elem[2] for elem in jump_enc_1]
jump_std2 = [elem[2] for elem in jump_enc_2]
jump_std3 = [elem[2] for elem in jump_enc_3]
jump_std4 = [elem[2] for elem in jump_enc_4]
jump_std5 = [elem[2] for elem in jump_enc_5]

jump_enc_1 = [elem[1] for elem in jump_enc_1]
jump_enc_2 = [elem[1] for elem in jump_enc_2]
jump_enc_3 = [elem[1] for elem in jump_enc_3]
jump_enc_4 = [elem[1] for elem in jump_enc_4]
jump_enc_5 = [elem[1] for elem in jump_enc_5]

t1 = t2 = t3 = t4 = t5 = np.arange(1, 6)

plt.close('all')

#fig = plt.figure(figsize=(24,8), frameon=False)
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True)

fig.set_size_inches(22,8)
#fig_size = plt.rcParams["figure.figsize"]

#fig_size[0] = 16
#fig_size[1] = 12

ax2.set_title('JUMP', fontsize=24)
ax2.errorbar(t1, jump_enc_1, jump_std1, label='enc_1', marker='D', color='g', uplims=True, lolims=True, barsabove=True, linewidth=4, elinewidth=-1)
ax2.errorbar(t2, jump_enc_2, jump_std2, label='enc_2', marker='o', color='b', uplims=True, lolims=True, barsabove=True, linewidth=4, elinewidth=-1)
ax2.errorbar(t3, jump_enc_3, jump_std3, label='enc_3', marker='x', color='r', uplims=True, lolims=True, barsabove=True, linewidth=4, elinewidth=-1)
ax2.errorbar(t4, jump_enc_4, jump_std4, label='enc_4', marker='p', color='c', uplims=True, lolims=True, barsabove=True, linewidth=4, elinewidth=-1)
ax2.errorbar(t5, jump_enc_5, jump_std5, label='enc_5', marker='s', color='m', uplims=True, lolims=True, barsabove=True, linewidth=4, elinewidth=-1)

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
    std = float(elem.split('std: ')[1].split(',')[0])
    random_enc_list.append((dec_value, accuracy, std))
    random_enc_list.sort(key=lambda x : x[0])

random_std1 = [elem[2] for elem in random_enc_1]
random_std2 = [elem[2] for elem in random_enc_2]
random_std3 = [elem[2] for elem in random_enc_3]
random_std4 = [elem[2] for elem in random_enc_4]
random_std5 = [elem[2] for elem in random_enc_5]

random_enc_1 = [elem[1] for elem in random_enc_1]
random_enc_2 = [elem[1] for elem in random_enc_2]
random_enc_3 = [elem[1] for elem in random_enc_3]
random_enc_4 = [elem[1] for elem in random_enc_4]
random_enc_5 = [elem[1] for elem in random_enc_5]

ax1.set_title('RANDOM', fontsize=24)
ax1.errorbar(t1, random_enc_1, random_std1, label='enc_1', marker='D', color='g', uplims=True, lolims=True, barsabove=True, linewidth=4, elinewidth=-1)
ax1.errorbar(t2, random_enc_2, random_std2, label='enc_2', marker='o', color='b', uplims=True, lolims=True, barsabove=True, linewidth=4, elinewidth=-1)
ax1.errorbar(t3, random_enc_3, random_std3, label='enc_3', marker='x', color='r', uplims=True, lolims=True, barsabove=True, linewidth=4, elinewidth=-1)
ax1.errorbar(t4, random_enc_4, random_std4, label='enc_4', marker='p', color='c', uplims=True, lolims=True, barsabove=True, linewidth=4, elinewidth=-1)
ax1.errorbar(t5, random_enc_5, random_std5, label='enc_5', marker='s', color='m', uplims=True, lolims=True, barsabove=True, linewidth=4, elinewidth=-1)

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
    std = float(elem.split('std: ')[1].split(',')[0])
    template_enc_list.append((dec_value, accuracy, std))
    template_enc_list.sort(key=lambda x : x[0])

template_std1 = [elem[2] for elem in template_enc_1]
template_std2 = [elem[2] for elem in template_enc_2]
template_std3 = [elem[2] for elem in template_enc_3]
template_std4 = [elem[2] for elem in template_enc_4]
template_std5 = [elem[2] for elem in template_enc_5]

template_enc_1 = [elem[1] for elem in template_enc_1]
template_enc_2 = [elem[1] for elem in template_enc_2]
template_enc_3 = [elem[1] for elem in template_enc_3]
template_enc_4 = [elem[1] for elem in template_enc_4]
template_enc_5 = [elem[1] for elem in template_enc_5]

ax3.set_title('AROUND-RIGHT', fontsize=24)
ax3.errorbar(t1, template_enc_1, template_std1, label='enc_1', marker='D', color='g', uplims=True, lolims=True, barsabove=True, linewidth=4, elinewidth=-1)
ax3.errorbar(t2, template_enc_2, template_std2, label='enc_2', marker='o', color='b', uplims=True, lolims=True, barsabove=True, linewidth=4, elinewidth=-1)
ax3.errorbar(t3, template_enc_3, template_std3, label='enc_3', marker='x', color='r', uplims=True, lolims=True, barsabove=True, linewidth=4, elinewidth=-1)
ax3.errorbar(t4, template_enc_4, template_std4, label='enc_4', marker='p', color='c', uplims=True, lolims=True, barsabove=True, linewidth=4, elinewidth=-1)
ax3.errorbar(t5, template_enc_5, template_std5, label='enc_5', marker='s', color='m', uplims=True, lolims=True, barsabove=True, linewidth=4, elinewidth=-1)

#ax3.errorbar(t5, template_enc_5, template_std5, label='enc_5', marker='s', color='m', uplims=True, lolims=True, barsabove=True, capthick=4)
#ax3.errorbar(t4, template_enc_4, template_std4, label='enc_4', marker='1', color='c', uplims=True, lolims=True, barsabove=True, elinewidth=2)

x_list = [elem for elem in range(1, 6)]
y_list = [elem for elem in range(0, 101, 5)]

ax1.xaxis.set_ticks(x_list)
ax1.xaxis.set_tick_params(labelsize=24)
#ax1.yaxis.set_ticklabels(y_list)
ax1.yaxis.set_tick_params(labelsize=24)

ax2.xaxis.set_ticks(x_list)
ax2.xaxis.set_tick_params(labelsize=24)
#ax2.yaxis.set_ticklabels(y_list)
ax2.yaxis.set_tick_params(labelsize=24)

ax3.xaxis.set_ticks(x_list)
ax3.xaxis.set_tick_params(labelsize=24)
#ax3.yaxis.set_ticklabels(y_list)
ax3.yaxis.set_tick_params(labelsize=24)


ax1.tick_params(axis='y', direction='out', width=4, length=8, pad=8)
ax1.tick_params(axis='y', which='minor', direction='out', width=1, length=4)
ax2.tick_params(axis='y', direction='out', width=4, length=8, pad=8)
ax2.tick_params(axis='y', which='minor', direction='out', width=1, length=4)
ax3.tick_params(axis='y', direction='out', width=4, length=8, pad=8)
ax3.tick_params(axis='y', which='minor', direction='out', width=1, length=4)

ax1.tick_params(axis='x', which='minor', bottom=False)
ax2.tick_params(axis='x', which='minor', bottom=False)
ax3.tick_params(axis='x', which='minor', bottom=False)

ax1.minorticks_on()
ax2.minorticks_on()
ax3.minorticks_on()

#ax3.yaxis.set_ticks(y_list)

ax2.yaxis.set_ticks_position('left')
ax3.yaxis.set_ticks_position('left')

ax1.legend(fontsize=24)
#ax2.legend(fontsize=14)
#ax3.legend(fontsize=14, bbox_to_anchor=(1.5,1),borderaxespad=0)

#plt.show()
fig.savefig('/Users/robertodessi/Desktop/SCAN-CNN/writeups/acl2019/figures/kernel_exp.png', format='png', bbox_inches='tight', dpi=100)
