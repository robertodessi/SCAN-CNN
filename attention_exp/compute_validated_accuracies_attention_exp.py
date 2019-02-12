import os
import argparse
import numpy as np
import statistics

def main():

    parser = argparse.ArgumentParser(description='Best cnn models on SCAN template')
    parser.add_argument('--input', required=True, type=str)
    parser.add_argument('--output', required=True, type=str)

    args = vars(parser.parse_args())

    with open(args['input']) as f:
        file_lines = f.readlines()

    models = {'jump' : {},
              'template' : {},
              'random' : {},
            }

    for idx in range(0, len(file_lines), 3):
        split = file_lines[idx].strip().split('/')[1]
        model_name = file_lines[idx].strip().split('/')[2]
        seed_value = int(file_lines[idx].strip().split('/')[-2][-1])
        accuracy = round(float(file_lines[idx+1]), 2)
        seed_name = 'seed_' + str(seed_value)
        if model_name in models[split]:
            models[split][model_name].update({seed_name : accuracy })
        else:
            models[split][model_name] = {}
            models[split][model_name].update({seed_name : accuracy })

    finals = {'jump' : {},
              'template' : {},
              'random' : {},
            }

    split_list = ['jump', 'random', 'template']
    for split in split_list:
        for model_name in models[split].keys():
            accuracy_list = []
            for seed in models[split][model_name]:
                accuracy_list.append(models[split][model_name][seed])

            median_values = statistics.median(accuracy_list)
            reference_seed = (accuracy_list.index(median_values) + 2) if len(accuracy_list) % 2 else 0

            finals[split][model_name] = { 'model_name' : model_name,
                    'avg_acc' : sum(accuracy_list) / len(accuracy_list),
                    'min_acc' : min(accuracy_list),
                    'max_acc' : max(accuracy_list),
                    'var': np.var(accuracy_list),
                    'std': np.std(accuracy_list),
                    'num_models' : len(accuracy_list),
                    'reference_seed' : reference_seed,
                    }

    final_random_list, final_jump_list, final_template_list= [], [], []
    for split in split_list:
        for keys in finals[split]:
            if split == 'random':
                final_random_list.append((keys, finals[split][keys]['avg_acc']))
            elif split == 'template':
                final_template_list.append((keys, finals[split][keys]['avg_acc']))
            elif split == 'jump':
                final_jump_list.append((keys, finals[split][keys]['avg_acc']))
            else:
                print('| ERROR!')
                exit(1)

    sorted_jump = sorted(final_jump_list, key=lambda x : x[1], reverse=True)
    sorted_template = sorted(final_template_list, key=lambda x : x[1], reverse=True)
    sorted_random = sorted(final_random_list, key=lambda x : x[1], reverse=True)

    output_file = args['output'] + 'validated_accuracies.txt'

    if os.path.isfile(output_file):
            os.remove(output_file)

    top10_std = []
    with open(output_file, 'a') as to_write:
        to_write.write("| RANDOM split \n\n")

        for i, elem in enumerate(sorted_random):
            model_data = finals['random'][elem[0]]
            if i < 10:
                top10_std.append(model_data['std'])
            output_msg = '| ' + str(i+1) + \
                        '. Model: ' + model_data['model_name'] + \
                        ', avg accuracy across seeds: ' + str(round(model_data['avg_acc'], 2)) + \
                        ', min accuracy across seeds: ' + str(round(model_data['min_acc'], 2)) + \
                        ', max_accuracy across seeds: ' + str(round(model_data['max_acc'], 2)) + \
                        ', variance: ' +  str(round(model_data['var'], 2)) + \
                        ', std: ' + str(round(model_data['std'], 2)) + \
                        ', reference seed: ' + str(model_data['reference_seed'])+ \
                        '. Number of runs considered: ' + str(model_data['num_models']) + \
                        '\n'
            to_write.write(output_msg)

        max10, min10, avg10 =  round(max(top10_std), 2), round(min(top10_std), 2), round(np.mean(top10_std), 2)
        to_write.write('\n| Max std top10 models: {}, min {}, avg {}'
            .format(max10, min10, avg10))

        to_write.write('\n\n=======================\n\n')
        to_write.write("| JUMP split \n\n")

        for i, elem in enumerate(sorted_jump):
            model_data = finals['jump'][elem[0]]
            if i < 10:
                top10_std.append(model_data['std'])
            output_msg = '| ' + str(i+1) + \
                        '. Model: ' + model_data['model_name'] + \
                        ', avg accuracy across seeds: ' + str(round(model_data['avg_acc'], 2)) + \
                        ', min accuracy across seeds: ' + str(round(model_data['min_acc'], 2)) + \
                        ', max_accuracy across seeds: ' + str(round(model_data['max_acc'], 2)) + \
                        ', variance: ' +  str(round(model_data['var'], 2)) + \
                        ', std: ' + str(round(model_data['std'], 2)) + \
                        ', reference seed: ' + str(model_data['reference_seed'])+ \
                        '. Number of runs considered: ' + str(model_data['num_models']) + \
                        '\n'
            to_write.write(output_msg)

        max10, min10, avg10 =  round(max(top10_std), 2), round(min(top10_std), 2), round(np.mean(top10_std), 2)
        to_write.write('\n| Max std top10 models: {}, min {}, avg {}'
            .format(max10, min10, avg10))


        to_write.write('\n\n=======================\n\n')
        to_write.write("| TEMPLATE split \n\n")

        for i, elem in enumerate(sorted_template):
            model_data = finals['template'][elem[0]]
            if i < 10:
                top10_std.append(model_data['std'])
            output_msg = '| ' + str(i+1) + \
                        '. Model: ' + model_data['model_name'] + \
                        ', avg accuracy across seeds: ' + str(round(model_data['avg_acc'], 2)) + \
                        ', min accuracy across seeds: ' + str(round(model_data['min_acc'], 2)) + \
                        ', max_accuracy across seeds: ' + str(round(model_data['max_acc'], 2)) + \
                        ', variance: ' +  str(round(model_data['var'], 2)) + \
                        ', std: ' + str(round(model_data['std'], 2)) + \
                        ', reference seed: ' + str(model_data['reference_seed'])+ \
                        '. Number of runs considered: ' + str(model_data['num_models']) + \
                        '\n'
            to_write.write(output_msg)

        max10, min10, avg10 =  round(max(top10_std), 2), round(min(top10_std), 2), round(np.mean(top10_std), 2)
        to_write.write('\n| Max std top10 models: {}, min {}, avg {}'
            .format(max10, min10, avg10))

if __name__== '__main__':
    main()
