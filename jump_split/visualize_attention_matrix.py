import numpy as np
import pdb

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.stats import linregress
import math

import argparse

#attention_path = 'out.txt'
attention_path = 'attention.txt'
def main():
    parser = argparse.ArgumentParser(description='Inspect attention matrix.')
    parser.add_argument('--save-output', type=str)
    parser.add_argument('--show-matrix', action='store_true', default=False)

    group = parser.add_mutually_exclusive_group(required=True)
#    group.add_argument('--range', nargs='*', help='list of range(s) of attention matrix to inspect')
    group.add_argument('--sample', type=int, help='exact id of the attention matrix to be inspected')
    group.add_argument('--interactive', action='store_true', default=False, help='run the inspection in interactive mode')
    group.add_argument('--string-action', type=str, nargs='*')
    group.add_argument('--compare', type=str, nargs='*')
    group.add_argument('--contains', type=str, nargs='*')

    parser.add_argument('--value', type=float)
    parser.add_argument('--modifier', type=str)
    parser.add_argument('--max-occ', type=int, default = -1, help='max number of occurences in contains mode')
    parser.add_argument('--train-and-test' , action = 'store_true', default = False, help = 'consider both train and test set' )
    parser.add_argument('--train-only' , action = 'store_true', default = False, help = 'consider train set only' )

    args = vars(parser.parse_args())
    args = upd_args(args)

    if args['sample']:
        seq = build_dict(args, sample_id = args['sample'])
        print_matrix(seq, args)
    elif args['interactive']:
        while True:
            print('>> Insert sample_id or source_string to inspect. "q" or "Q" to quit ')
            sample_id = input('>> ')
            if sample_id == 'q' or sample_id == 'Q':
                print('>> Exiting program. ')
                exit(1)
            elif sample_id.isdigit():
                seq = build_dict(args, sample_id = int(sample_id))
                print_matrix(seq, args)
            else:
                seq = build_dict(args, command_string = sample_id)
                print_matrix(seq, args)
    elif args['string_action']:
        search_string = args['string_action']
        comm = ' '.join([ elem.strip() for elem in search_string ])
        seq = build_dict(args, command_string = comm)
        print_matrix(seq, args)
    elif args['contains'] is not 'dummy':
        args['contains'] = ' '.join([ elem.strip() for elem in args['contains'] ])
        seq = build_dict(args, max_occ =  args['max_occ'])
#        print_matrix(seq, args)
    elif args['compare']:
        com_list = []
        com = ''
        for elem in args['compare']:
            if elem != '.':
                com+=elem + ' '
            else:
                com_list.append(com.strip())
                com = ''
        seq = build_dict(args, command_string = com_list)
        print_matrix(seq, args)

def upd_args(args):
    if not args['contains']:
        args['contains'] = 'dummy'
    return args
def build_dict(args, sample_id = None, command_string = None, max_occ = None):
    final = []
    with open(attention_path) as f:
        idx =  1
        mat = ''
        src = ''
        target = ''
        ground = ''
        evaluation = ''
        for elem in f:
            if elem[0].isdigit():
                mat += elem
            elif elem[0].isupper():
                target = elem.strip()
            elif elem[0] == '/':
                ground = elem[1:-1].strip()
            elif elem[0] == '=':
                evaluation = elem[1:-1]
            elif elem[0].islower():
                src = elem.strip()
            elif elem[0] == '-':
                if args['train_only'] and idx < 7706:
                    continue
                if not args['train_and_test'] and idx == 7707:
                    break
                if args['compare']:
                    if not command_string:
                        break
                    for i, elem in enumerate(command_string):
                        if elem == src:
                            mat = mat.replace('\n', '; ').replace('\t', ' ')[:-3]
                            mat = np.matrix(mat)
                            final.append({'mat': mat, 'src': src,
                                'target': target, 'ground': ground,
                                'evaluation': evaluation, 'idx': idx})
                            del command_string[i]
                            break
                if idx == sample_id  or command_string == src:
                    mat = mat.replace('\n', '; ').replace('\t', ' ')[:-3]
                    mat = np.matrix(mat)
                    final.append({'mat': mat, 'src': src,
                        'target': target, 'ground': ground,
                        'evaluation': evaluation, 'idx': idx})
                if args['contains'] in src:
                    mat = mat.replace('\n', '; ').replace('\t', ' ')[:-3]
                    mat = np.matrix(mat)
                    final.append({'mat': mat, 'src': src,
                        'target': target, 'ground': ground,
                        'evaluation': evaluation, 'idx': idx})
                    if max_occ > 0 and len(final) == max_occ:
                        break
                mat = ''
                src = ''
                target = ''
                ground = ''
                evaluation = ''
                idx = idx + 1
        if not final:
            print("Could not find a matching sample")
            print("Exiting program")
            exit(1)
    if args['contains'] is not 'dummy':
        target_len = []
        ev = []
        right_att_right_eval = 0
        right_att_wrong_eval = 0
        wrong_att_right_eval = 0
        wrong_att_wrong_eval = 0
        total = 0
        for k, elem in enumerate(final):
            mat = elem['mat']
            i, j = np.unravel_index(mat.argmax(), mat.shape)
            max_value = mat[i,j]
            src_split = elem['src'].split(' ')
            #target_split = elem['target'].split(' ')
            src_index = elem['src'].split(' ').index(args['modifier'])
            arr = np.squeeze(np.asarray(mat[src_index]))
            curr_max = max(arr)

            target_len.append(len(elem['target'].split(' ')))

            if elem['evaluation'] == 'True':
                if curr_max / max_value > args['value']:
                    right_att_right_eval += 1
                    ev.append(1)
                else:
                    wrong_att_right_eval += 1
                    ev.append(2)
            else:
                if curr_max / max_value > args['value']:
                    right_att_wrong_eval += 1
                    ev.append(3)
                else:
                    wrong_att_wrong_eval += 1
                    ev.append(4)

            total += 1
        print('| {} total example. {} right_att_right_eval, {} had wrong_att_right eval, {} had right_att_wrong_eval, {} had wrong_att_wrong_eval'.format(total, right_att_right_eval, wrong_att_right_eval, right_att_wrong_eval, wrong_att_wrong_eval ))

        correct_evaluation = right_att_right_eval + wrong_att_right_eval
        acc_evaluation = correct_evaluation / total
        correct_attention =  right_att_right_eval + right_att_wrong_eval
        acc_attention = correct_attention / total

        print('| {} samples were correctly evaluated, acc = {:.4f}. {} samples had right attention for modifier {} with a percentage attention score > {}, acc {:.4f}'.format(correct_evaluation, acc_evaluation, correct_attention, args['modifier'], args['value'], acc_attention ) )
        pri_final = '| {} esempi in totale, il {:.2f}% ({} esempi) e stato tradotto correttamente. Di quelli tradotti correttamente il {:.2f}% ({} esempi) aveva un\'attenzione data a {} > {}%.\n| Di tutti gli esempi (corretti e non corretti) il {:.2f}% ({} esempi) aveva l\'attenzione sopra tale livello '.format(total, (correct_evaluation/total)*100, correct_evaluation, (right_att_right_eval/correct_evaluation)*100, right_att_right_eval, args['modifier'], int(args['value']*100), (correct_attention/total)*100, correct_attention)

        print(pri_final)

    return final

'''
    tmp = linregress(target_len, ev)
    slope, intercept = tmp[0], tmp[1]
    print('| rvalue = {}, pvalue = {}'.format(tmp[2], tmp[3]))
    ab = [slope * i + intercept for i in target_len]

    plt.scatter(target_len, ev)
    plt.plot(target_len, ab, 'b')
    plt.show()


    import scipy.stats as stats
    h = sorted(target_len)
    fit = stats.norm.pdf(h, np.mean(h), np.std(h))  #this is a fitting indeed
    plt.plot(h,fit,'-o')
    plt.hist(h,normed=True)      #use this to draw histogram of your data

    plt.show()
'''


def print_matrix(seq, args):
    fig = plt.figure()
    l = len(seq)
    if l > 6:
        rows = 3
    elif l > 3:
        rows = 2
    else:
        rows  = 1
    cols = math.ceil(l/rows)
    for i, elem in enumerate(seq):
        ax = fig.add_subplot(rows,cols,i+1)
        cax = ax.matshow(elem['mat'], cmap='bone')
        fig.colorbar(cax)
        train_or_test = 'Test' if elem['idx'] <= 7706 else 'Train'
        title = 'Evaluation: {}\nSample_id: {}. {} element'.format(
                elem['evaluation'], elem['idx'], train_or_test)
        plt.xlabel(title)

        src = [''] + elem['src'].split(" ") + ['<EOS>']
        target = [''] + elem['target'].split(" ") + ['<EOS>']
        # Set up axes
        ax.set_xticklabels(target, rotation = 90)
        ax.set_yticklabels(src)

        print("| src: {}\n| target: {}\n| ground_truth: {}\n| eval: {} ".format(
            elem['src'], elem['target'], elem['ground'], elem['evaluation'] ))

        # Show label at every tick
        ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    if args['show_matrix']:
        plt.show()
    if args['save_output']:
        path = args['save_output'] + '/sample' + str(idx) + '.png'
        fig.savefig(path)

if __name__ == '__main__':
        main()
