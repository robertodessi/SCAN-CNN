import matplotlib.pyplot as plt
import numpy as np

#jump = [(60.67, 8.33, 'ful'), (4.12, 0.97, 'fon'), (10.81, 1.91, 'ftw'), (16.15, 5.52, 'fth'), (56.36, 17.5, 'lth'), (56.25, 10.42, 'ltw'), (65.73, 5.89, 'lon')]
jump = [(4.12, 0.97, 'fon'), (10.81, 1.91, 'ftw'), (16.15, 5.52, 'fth'), (56.36, 17.5, 'lth'), (56.25, 10.42, 'ltw'), (65.73, 5.89, 'lon')]
#t = [elem[2] for elem in jump]
t = ['bottom1', 'bottom2', 'bottom3', 'top3', 'top2', 'top1']
jump_std = [elem[1] for elem in jump]
jump = [elem[0] for elem in jump]
jump_full = [60.67] * len(t)

template = [(0.02, 0.04, 'fon'), (18.70, 9.61, 'ftw'), (9.63, 10.63, 'fth'), (63.93, 13.69, 'lth'), (42.62, 14.09, 'ltw'), (7.31, 3.32, 'lon')]
template_std = [elem[1] for elem in template]
template = [elem[0] for elem in template]
template_full = [53.25] * len(t)

random = [(99.29, 0.35, 'fon'), (99.9, 0.03, 'ftw'), (99.9, 0.04, 'fth'), (99.57, 0.19, 'lth'), (98.95, 0.28, 'ltw'), (96.16, 0.26, 'lon')]
random_std = [elem[1] for elem in random]
random = [elem[0] for elem in random]
random_full = [99.92] * len(t)

plt.close('all')
plt.figure(1)
#plt.xlabel('Attention')
#plt.ylabel('Accuracy')
#plt.title("Attention ablation study")

f = plt.figure(figsize=(6,4), frameon=False)

plt.errorbar(t, random, random_std, label='random', marker='x', color='r')#, uplims=True, lolims=True)
plt.errorbar(t, jump, jump_std, label='jump', marker='s', color='g', uplims=True, lolims=True)
plt.errorbar(t, template, template_std, label='around-right', marker='o', color='b', uplims=True, lolims=True)
plt.plot(t, jump_full, linestyle='--', color='g')
plt.plot(t, template_full, linestyle='--', color='b')
plt.plot(t, random_full, linestyle='--', color='r')

y_list = np.arange(0, 101, 10)
plt.xticks(t, fontsize=12)
plt.yticks(y_list, fontsize=14)

#plt.text(20, 80, 'Dashed lines report split means')
plt.legend(loc='lower center', bbox_to_anchor=(0.7, 0.0), fontsize=12)
#plt.show()

f.savefig('/Users/robertodessi/Desktop/SCAN-CNN/writeups/acl2019/figures/attention_exp2.png', format='png', bbox_inches='tight')#, dpi=50)


#plt.errorbar(t1, jump_enc_1, jump_std1, label='enc_1', marker='.', color='g', uplims=True, lolims=True)
#plt.plot(t1, jump_enc_1, label='enc_1', marker='.', color='g')
