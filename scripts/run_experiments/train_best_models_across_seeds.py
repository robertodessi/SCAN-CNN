import argparse
import os

def main():

    parser = argparse.ArgumentParser(description='Best cnn models on SCAN dataset')
    parser.add_argument('--n', type=int, default=300)
    parser.add_argument('--data-bin', type=str, required=True)
    parser.add_argument('--save-dir', type=str, required=True)
    parser.add_argument('--accuracies', type=str, required=True)
    parser.add_argument('--output-train-path', type=str, default='./train.txt')
    parser.add_argument('--output-generate-path', type=str, default='./generate.txt')

    args = vars(parser.parse_args())

    l = []
    with open(args['accuracies']) as f:
        l = f.readlines()

    done = 0
    for idx in range(len(l)):
        model = l[idx].strip().split('Model: ')[1].split(', accuracy')[0]
        params = model.split('_')
        lr = params[1]
        maxtok = params[3]
        layers = params[5]
        embed_dim = params[8]
        kernel = params[10]
        dropout = params[12]

        if dropout == '0.1':
            continue

        out_prefix = "lr_" + lr +  "_maxtok_" + maxtok + \
                "_lay_" + layers + "_embed_dim_" + embed_dim + \
                "_kernel_" + kernel + "_dropout_" + dropout


        for i in range(1, 6):
            seed = i+1
            save_dir = os.path.join(args['save_dir'], out_prefix) + '/seed_' + str(seed)
            train_command = 'python ./train.py ' + args['data_bin'] + \
                    ' --clip-norm 0.1' + \
                    ' --max-tokens ' +  maxtok + \
                    ' --save-dir ' + save_dir + \
                    ' --max-epoch 1' + \
                    ' --no-epoch-checkpoints' + \
                    ' --lr ' + lr + \
                    ' --encoder-embed-dim ' + embed_dim + \
                    ' --encoder-layers ' + '\"[('+embed_dim+', '+kernel+')] * '+layers + '\"' + \
                    ' --decoder-embed-dim ' + embed_dim + \
                    ' --decoder-layers ' + '\"[('+embed_dim+', '+kernel+')] * '+layers + '\"' + \
                    ' --decoder-out-embed-dim ' + embed_dim + \
                    ' --optimizer nag' + \
                    ' --arch fconv' + \
                    ' --dropout ' + dropout + \
                    ' --decoder-attention True' + \
                    ' --seed ' + str(seed)


            generate_command = 'python generate.py ' + args['data_bin'] + \
                    ' --path ' + save_dir + '/checkpoint_best.pt' + \
                    ' --batch-size 128' + \
                    ' --quiet' + \
                    ' --output ' + save_dir + '/accuracy.txt' + \
                    ' --beam 1'

            with open(args['output_train_path'], 'a') as g:
                g.write(train_command)
                g.write('\n')
            with open(args['output_generate_path'], 'a') as k:
                k.write(generate_command)
                k.write('\n')

        done += 1
        if done == int(args['n']):
            break

if __name__ == '__main__':
    main()
