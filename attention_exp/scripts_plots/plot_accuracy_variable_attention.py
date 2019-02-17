import matplotlib.pyplot as plt
import numpy as np

jump = [(60.67, 8.33, 'ful'), (4.12, 0.97, 'fon'), (10.81, 1.91, 'ftw'), (16.15, 5.52, 'fth'), (56.36, 17.5, 'lth'), (56.25, 10.42, 'ltw'), (65.73, 5.89, 'lon')]
t = [elem[2] for elem in jump]
jump_std = [elem[1] for elem in jump]
jump = [elem[0] for elem in jump]
jump_full = [jump[0]] * len(t)

template = [(53.25, 19.08, 'ful'), (0.14, 0.15, 'fon'), (24.48, 13.84, 'ftw'), (24.65, 24.54, 'fth'), (59.48, 8.74, 'lth'), (29.6, 12.72, 'ltw'), (3.15, 1.92, 'lon')]
template_std = [elem[1] for elem in template]
template = [elem[0] for elem in template]
template_full = [template[0]] * len(t)

random = [(99.92, 0.07, 'ful'), (99.29, 0.35, 'fon'), (99.9, 0.03, 'ftw'), (99.9, 0.04, 'fth'), (99.57, 0.19, 'lth'), (98.95, 0.28, 'ltw'), (96.16, 0.26, 'lon')]
random_std = [elem[1] for elem in random]
random = [elem[0] for elem in random]
random_full = [random[0]] * len(t)

plt.close('all')
plt.figure(1)
plt.xlabel('Attention')
plt.ylabel('Accuracy')
plt.title("Attention ablation study")

plt.errorbar(t, jump, jump_std, label='jump', marker='.', color='g', uplims=True, lolims=True)
plt.errorbar(t, template, template_std, label='template', marker='o', color='b', uplims=True, lolims=True)
plt.errorbar(t, random, random_std, label='random', marker='x', color='r')#, uplims=True, lolims=True)
plt.plot(t, jump_full, linestyle='--', color='g')
plt.plot(t, template_full, linestyle='--', color='b')
plt.plot(t, random_full, linestyle='--', color='r')

#plt.text(20, 80, 'Dashed lines report split means')
plt.legend()
plt.show()

#plt.errorbar(t1, jump_enc_1, jump_std1, label='enc_1', marker='.', color='g', uplims=True, lolims=True)
#plt.plot(t1, jump_enc_1, label='enc_1', marker='.', color='g')
