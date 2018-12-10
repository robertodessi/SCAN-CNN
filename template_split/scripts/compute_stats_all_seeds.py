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

    models = {}

    '''
    models = {
        'lr_0.001_maxtok_100_lay_10_embed_dim_512_kernel_4_dropout_0' :
            { 'seed_2' : 11.45,
              'seed_3' : 9.34,
              ...
              }
          ...
    }

    '''

    def extract_params(model):
        params = model.strip().split('_')
        return {'lr' : params[1],
                'maxtok' : params[3],
                'lay' : params[5],
                'embed_dim' : params[8],
                'kernel' : params[10],
                'dropout' : params[12],
                }

    for idx in range(0, len(file_lines), 3):
        model_name = file_lines[idx].strip().split('/')[-3]
        seed_value = int(file_lines[idx].strip().split('/')[-2][-1])
        accuracy = round(float(file_lines[idx+1]), 2)
        seed_name = 'seed_' + str(seed_value)
        if model_name in models:
            models[model_name].update({seed_name : accuracy })
        else:
            models[model_name] = {}
            models[model_name].update({seed_name : accuracy })

    finals = {}

    for model_name in models.keys():
        accuracy_list = []
        for seed in models[model_name]:
            #if len(accuracy_list) > 5:
            #    continue
            accuracy_list.append(models[model_name][seed])

        median_values = statistics.median(accuracy_list)
        reference_seed = (accuracy_list.index(median_values) + 2) if len(accuracy_list) % 2 else 0

        finals[model_name] = { 'model_name' : model_name,
                'avg_acc' : sum(accuracy_list) / len(accuracy_list),
                'min_acc' : min(accuracy_list),
                'max_acc' : max(accuracy_list),
                'var': np.var(accuracy_list),
                'std': np.std(accuracy_list),
                'num_models' : len(accuracy_list),
                'reference_seed' : reference_seed,
                }

    final_list = []
    for keys in finals:
        final_list.append((keys, finals[keys]['avg_acc']))


    sorted_finals = sorted(final_list, key=lambda x : x[1], reverse=True)

    output_file = args['output'] + 'validated_accuracies.txt'

    if os.path.isfile(output_file):
            os.remove(output_file)

    top10_std = []
    with open(output_file, 'a') as to_write:
        for i, elem in enumerate(sorted_finals):
            model_data = finals[elem[0]]
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
