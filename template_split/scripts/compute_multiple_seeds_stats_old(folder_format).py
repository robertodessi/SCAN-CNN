import os
import argparse
import numpy as np
import statistics

'''
model.update({'params' : elem, 'avg_acc' : avg_acc, 'min_acc' : min_acc,
                'max_acc' : max_acc, 'var': var, 'var1' : var1, 'std': std,
                'std1' : std1, 'num_models' : completed_out_of_five, 'reference_seed' : reference_seed})
'''


def main():

    parser = argparse.ArgumentParser(description='Best cnn models on SCAN template')
    parser.add_argument('--output', required=True, type=str)

    args = vars(parser.parse_args())

    folder_list = []
    for (dirpath, dirnames, filenames) in os.walk('./'):
            folder_list = dirnames
            break

    def not_exist(fpath):
        return (not os.path.isfile(fpath)) or (os.path.getsize(fpath) is  0)

    def extract_params(model):
        params = model.strip().split('_')
        return {'lr' : params[1],
                'maxtok' : params[3],
                'lay' : params[5],
                'embed_dim' : params[8],
                'kernel' : params[10],
                'dropout' : params[12],
                }

    # lr_0.01_maxtok_25_lay_6_embed_dim_512_kernel_3_dropout_0.25
    model_stats = [] # model stats averaged across seeds
    err_list = [] # seed that did not complete
    no_seed_models = [] # models without any seeds completing
    reference_seed = [] # support list to compute reference seed 
    total = 0 # total number of models computed
    for i, elem in enumerate(folder_list):
        if elem.startswith('lr'):
            param = extract_params(elem)
            if param['dropout'] == '0.1':
                continue    # ignoring models with dropout 0.1 for consistency with experiment with jump split

            seed_stats = []    # saving seed stats for a given model
            completed_out_of_five = 0 # how many seed for a given model completed the run

            for (dirpath, dirnames, filenames) in os.walk(elem):
                seed_folder_list = dirnames
                break

            if len(seed_folder_list) == 0:
                continue

            for seed_id in range(2, 7):
                model_with_seed_id = elem + '/seed_' + str(seed_id) + '/accuracy.txt'
                if not_exist(model_with_seed_id):
                    err_list.append(elem + '/seed_' + str(seed_id))
                    continue
                with open(model_with_seed_id) as f:
                    tmp = f.readlines()
                    data = float(tmp[0].strip())
                    seed_stats.append((elem + '/seed_' + str(seed_id), data))
                    completed_out_of_five += 1

            # getting the seed (= index+1) of related to the median accuracy for a model 

            if len(seed_stats) == 0:
                no_seed_models.append(elem)
                continue
            #if i == 1424:
            #    import pdb; pdb.set_trace()
            seed_values = [round(data[1], 2) for data in seed_stats]
            median_values = statistics.median(seed_values)
            reference_seed = (seed_values.index(median_values) + 2) if len(seed_values) % 2 else 0
            seed_stats.sort(key=lambda x : float(x[1]))

            total += 1

            min_acc, max_acc = seed_stats[0][1], seed_stats[-1][1]
            values = [ x[1] for x in seed_stats ]
            var = np.var(values)
            var1 = np.var(values, ddof=1)
            std = np.std(values)
            std1 = np.std(values, ddof=1)
            model = {}
            avg_acc = float(sum(values)) / float(completed_out_of_five)
            model.update({'params' : elem,
                'avg_acc' : avg_acc,
                'min_acc' : min_acc,
                'max_acc' : max_acc,
                'var': var,
                'var1' : var1,
                'std': std,
                'std1' : std1,
                'num_models' : completed_out_of_five,
                'reference_seed' : reference_seed,
            })
            model_stats.append(model)

    model_stats.sort(key=lambda x : x['avg_acc'], reverse = True)

    output_file = args['output'] + 'validated_accuracies.txt' if args['output'][-1] == '/' else args['output'] + '/validated_accuracies.txt'
    if os.path.isfile(output_file):
            os.remove(output_file)

    if os.path.isfile(output_file):
        os.remove(output_file)

    with open(output_file, 'a') as to_write:
            for idx in range(len(model_stats)):
                elem = model_stats[idx]
                output_msg = '| ' + str(idx+1) + \
                        '. Model: ' + elem['params'] + \
                        ', avg accuracy across seeds: ' + str(elem['avg_acc']) + \
                        ', variance: ' +  str(elem['var']) + \
                        ', std: ' + str(elem['std']) + \
                        ', reference seed: ' + str(elem['reference_seed']) + \
                        '. Number of runs considered: ' + str(elem['num_models']) + \
                        '\n\n'
#                        ', var n-1 dof: ' + str(elem['var1']) + \
#                        ', std n-1 dof: ' + str(elem['std1'])+ \
                to_write.write(output_msg)

            models_std = [ elem['std'] for elem in model_stats ]
            mean_std, max_std, min_std = np.mean(models_std), max(models_std), min(models_std)
            models_std10 = [ elem['std'] for elem in model_stats[:10] ]
            mean_std10, max_std10, min_std10 = np.mean(models_std10), max(models_std10), min(models_std10)

            to_write.write('\n\n| Average std across models: {}, min std {}, max std {} \n'.format(mean_std, min_std, max_std))

            to_write.write('\n\n| Average std across best 10 models: {}, min std {}, max std {} \n'.format(mean_std10, min_std10, max_std10))


#            err_msg = '\n\n| Error in loading/finding ' + str(len(err_list)) + ' models.\n'
#            to_write.write(err_msg)
            no_seed_msg = '\n| Models without any seed run completed: ' + \
                    str(len(no_seed_models)) + ' out of ' + str(total) + \
                    ' out of 300. ' + str(round(len( no_seed_models) / 300, 2)) + '% \n'
            to_write.write(no_seed_msg)
            for elem in no_seed_models:
                to_write.write(elem)
                to_write.write('\n')
            err_msg = '\n| Runs that did not complete. Total number: ' + str(len(err_list)) + ' out of 1500. ' + str(round(len(err_list) / 1500, 2)) + '% \n'
            to_write.write(err_msg)
            for elem in err_list:
                    to_write.write(elem)
                    to_write.write('\n')

if __name__ == '__main__':
    main()

