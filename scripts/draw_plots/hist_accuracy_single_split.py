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

jump_results = []
for i, elem in enumerate(jump_lines):
    if elem != '\n':
        jump_results.append(float(elem.split('avg accuracy across seeds: ')[1].split(',')[0]))

random_lines = []
with open(args['random']) as f:
    random_lines = f.readlines()

random_results = []
for i, elem in enumerate(random_lines):
    if elem != '\n':
        random_results.append(float(elem.split('avg accuracy across seeds: ')[1].split(',')[0]))

template_lines = []
with open(args['template']) as f:
    template_lines = f.readlines()

template_results = []
for i, elem in enumerate(template_lines):
    if elem != '\n':
        template_results.append(float(elem.split('avg accuracy across seeds: ')[1].split(',')[0]))

bins = np.linspace(0, 100)

#plt.hist(jump_results, bins, density=True)
#plt.hist(random_results, bins, density=True)
plt.hist(template_results, bins, density=True)
#plt.hist(template_results, bins, density=True, histtype='step', stacked=True, label='template')

#plt.legend(loc='upper left')

h = sorted(template_results)

fit = stats.norm.pdf(h, np.mean(h), np.std(h))  #this is a fitting indeed

plt.plot(h, fit)

plt.ylabel('probability')
plt.xlabel('avg accuracy across seeds')
plt.title("Template Split")
#plt.text(90, 4, 'blabla')
#plt.legend()

plt.show()
