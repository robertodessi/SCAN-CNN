import argparse
import os

def main():

    parser = argparse.ArgumentParser(description='Best cnn models on SCAN dataset')
    parser.add_argument('--data-bin', type=str, required=True)
    parser.add_argument('--save-dir', type=str, required=True)

    args = vars(parser.parse_args())

    with open('./train.txt', 'a') as g:
        with open('./generate.txt', 'a') as k:

            for lr in ['0.1', '0.01', '0.001']:
                for maxtok in ['25', '50', '100', '200', '500', '1000']:
                    for layers in ['6', '7', '8', '9', '10']:
                        for embed_dim in ['128', '256', '512']:
                            for kernel in ['3', '4', '5']:
                                for dropout in ['0', '0.25', '0.5']:
                                    out_prefix = "lr_" + lr + "_maxtok_" + maxtok + \
                                            "_lay_" + layers + "_embed_dim_" + embed_dim + \
                                            "_kernel_" + kernel + "_dropout_" + dropout + '/seed_1'

                                        #for i in range(5):
                                            #seed = i+1
                                            #save_dir = args['save_dir'] + out_prefix + '/seed_' + str(seed)

                                    save_dir = os.path.join(args['save_dir'], out_prefix)
                                    train_command = 'python ./train.py ' + args['data_bin'] + \
                                            ' --clip-norm 0.1' + \
                                            ' --max-tokens ' +  maxtok + \
                                            ' --save-dir ' + save_dir + \
                                            ' --max-epoch 1' + \
                                            ' --no-epoch-checkpoints' + \
                                            ' --lr ' + lr + \
                                            ' --encoder-embed-dim ' + embed_dim + \
                                            ' --encoder-layers ' + '[('+embed_dim+', '+kernel+')] * '+layers + \
                                            ' --decoder-embed-dim ' + embed_dim + \
                                            ' --decoder-layers ' + '[('+embed_dim+', '+kernel+')] * '+layers + \
                                            ' --decoder-out-embed-dim ' + embed_dim + \
                                            ' --optimizer nag' + \
                                            ' --arch fconv' + \
                                            ' --dropout ' + dropout + \
                                            ' --decoder-attention True' + \
                                            ' --seed 1'
                                            # ' --seed ' + str(seed)

                                    generate_command = 'python generate.py ' + args['data_bin'] + \
                                            ' --path ' + save_dir + '/checkpoint_best.pt' + \
                                            ' --batch-size 128' + \
                                            ' --quiet' + \
                                            ' --output ' + save_dir + '/accuracy.txt' + \
                                            ' --beam 1'

                                    g.write(train_command)
                                    g.write('\n')
                                    k.write(generate_command)
                                    k.write('\n')

if __name__ == '__main__':
    main()
