import matplotlib.pyplot as plt
import numpy as np

jump_acc = [69.24, 67.64, 67.09, 67.03, 66.54, 65.75, 65.5, 64.8, 64.8, 64.7]
jump_models = ['dim_128_lay_6_lr_0.1_do_0.25_kernel_5_maxtok_500', 'dim_128_lay_9_lr_0.1_do_0.25_kernel_5_maxtok_500', 'dim_128_lay_10_lr_0.1_do_0.25_kernel_5_maxtok_500',
        'dim_256_lay_10_lr_0.1_do_0.25_kernel_5_maxtok_500', 'dim_512_lay_3_lr_0.01_do_0.5_kernel_4_maxtok_25', 'dim_256_lay_8_lr_0.1_do_0.25_kernel_5_maxtok_1000',
        'dim_128_lay_7_lr_0.1_do_0.25_kernel_5_maxtok_500', 'dim_128_lay_10_lr_0.1_do_0.25_kernel_3_maxtok_500', 'dim_256_lay_8_lr_0.1_do_0.5_kernel_5_maxtok_500',
        'dim_512_lay_10_lr_0.1_do_0.25_kernel_5_maxtok_500']
jump_std = [8.17, 7.97, 9.56, 9.37, 10.38, 4.72, 6.13, 8.99, 6.53, 11.9]
jump_avg = [np.mean(jump_acc)] * 10

random_acc = [99.97, 99.96, 99.95, 99.95, 99.4, 99.4, 99.4, 99.4, 99.3, 99.3]
random_avg = [ np.mean(random_acc) ] * 10
random_models = ['lr_0.01_maxtok_25_lay_7_embed_dim_512_kernel_4_dropout_0', 'lr_0.01_maxtok_25_lay_10_embed_dim_512_kernel_4_dropout_0',
        'lr_0.01_maxtok_25_lay_10_embed_dim_512_kernel_5_dropout_0', 'lr_0.01_maxtok_25_lay_9_embed_dim_512_kernel_3_dropout_0',
        'lr_0.01_maxtok_50_lay_6_embed_dim_512_kernel_4_dropout_0', 'lr_0.01_maxtok_25_lay_10_embed_dim_256_kernel_3_dropout_0',
        'lr_0.01_maxtok_25_lay_7_embed_dim_512_kernel_5_dropout_0', 'lr_0.01_maxtok_50_lay_9_embed_dim_512_kernel_4_dropout_0',
        'lr_0.01_maxtok_25_lay_8_embed_dim_512_kernel_5_dropout_0', 'lr_0.01_maxtok_50_lay_9_embed_dim_512_kernel_5_dropout_0']
random_std = [0.03, 0.03, 0.03, 0.02, 0.03, 0.03, 0.05, 0.02, 0.07, 0.03]

template_acc = [56.7, 53.25, 45.79, 45.7, 44.73, 44.47, 44.33, 43.04, 42.27, 42.04]
#template_models = 
template_std = [10.24, 19.08, 13.49, 5.73, 18.56, 24.79, 9.93, 16.36, 16.44, 15.61]
template_avg = [np.mean(template_acc)] * 10

t = np.arange(1., 11., 1.)

plt.errorbar(t, jump_acc, jump_std, label='jump_split', linestyle='None', marker='.', color='g', uplims=True, lolims=True)
plt.errorbar(t, random_acc, random_std, label='random_split', linestyle='None', marker='x', color='r')
plt.errorbar(t, template_acc, template_std, label='template_split', linestyle='None', marker='o', color='b', uplims=True, lolims=True)
plt.plot(t, random_avg, linestyle='--', color='r')
plt.plot(t, jump_avg, linestyle='-.', color='g')
plt.plot(t, template_avg, linestyle=':', color='b')

y_list = np.arange(20, 101, 5)

plt.yticks(y_list)

plt.xlabel('ranking')
plt.ylabel('accuracy')
plt.title("Split accuracies")
plt.text(7, 20, 'Dashed lines report split means')
plt.legend()
plt.show()

