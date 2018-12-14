import os
import argparse

#/private/home/mbaroni/fairseq/new_run/template_around_right/model_files/lr_0.1_maxtok_25_lay_6_embed_dim_128_kernel_3_dropout_0.1/accuracy.txt

def main():
    parser = argparse.ArgumentParser(description='Best cnn models on SCAN dataset')
    parser.add_argument('--input', type=str, required=True)
    parser.add_argument('--output', type=str, required=True)
    parser.add_argument('--n', type=int, default=10)

    args = vars(parser.parse_args())

    file_list = []
    for (dirpath, dirnames, filenames) in os.walk(args['input']):
        file_list = dirnames
        break

    res_list = []
    err_list = []
    for elem in file_list:
        if elem.startswith('lr'):
            if not os.path.isfile(args['input'] + '/'+ elem + '/accuracy.txt'):
                err_list.append(elem)
                continue
                # there's no accuracy.txt file

            with open(args['input'] + '/' +elem + '/accuracy.txt') as f:
                tmp = f.readlines()
                if len(tmp) == 0:
                    err_list.append(elem)
                    continue
                    # exsists an accuracy.txt file but it's empty
                data = float(tmp[0].strip()) 
                res_list.append((elem, round(data, 2)))

    res_list.sort(key=lambda x : x[1], reverse = True)

    output_file = args['output'] + 'top_' + str(args['n']) + '_accuracies.txt' if args['output'][-1] == '/' else args['output'] + '/top_' +  str(args['n'])  + '_accuracies.txt'

    if os.path.isfile(output_file):
        os.remove(output_file)

    with open(output_file, 'a') as g:
        for idx in range(args['n']):
            output_message = '| ' + str(idx +1) + '. Model: ' + res_list[idx][0] + ', accuracy: ' + str(res_list[idx][1]) + '\n'
            g.write(output_message)

        g.write("\nError models:")
        for i, elem in enumerate(err_list):
            g.write('|' + str(err_list[i]))
        final_msg = "\n| Total number of model successfully evaluated: " + str(len(res_list)) + '. Total number of uncompleted train runs: ' + str(len(err_list))
        g.write(final_msg)

if __name__ == '__main__':
    main()

