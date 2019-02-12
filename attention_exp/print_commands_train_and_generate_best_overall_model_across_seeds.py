import argparse
import os

def main():

    parser = argparse.ArgumentParser(description='Best cnn models on SCAN dataset')
    parser.add_argument('--jump', type=str, required=True)
    parser.add_argument('--template', type=str, required=True)
    parser.add_argument('--random', type=str, required=True)
    parser.add_argument('--save-dir', type=str, required=True)
    parser.add_argument('--output-folder', type=str, default='commands/')

    args = vars(parser.parse_args())

    if args['output_folder'] == 'commands/':
        if not os.path.exists('commands/'):
                os.makedirs('commands/')

    splits = ['jump', 'random', 'template']
    lr = '0.01'
    maxtok = '25'
    lay = '6'
    embed_dim = '512'
    do = '0.25'
    kernel = '5'
   #lr_0.01_maxtok_25_lay_6_embed_dim_512_kernel_5_do_0.25


    jump_train_commands, template_train_commands , random_train_commands = [], [], []
    jump_generate_commands, template_generate_commands , random_generate_commands = [], [], []
    train_dict = {'random' : random_train_commands, 'jump' : jump_train_commands, 'template' : template_train_commands}
    generate_dict = {'random' : random_generate_commands, 'jump' : jump_generate_commands, 'template' : template_generate_commands}

    generate_list = []
    train_list = []
    attention_list = [('[1,0,0,0,0,0]','fon'), ('[1,1,0,0,0,0]','ftw'), ('[1,1,1,0,0,0]','fth'), ('[0,0,0,1,1,1]','lth'), ('[0,0,0,0,1,1]','ltw'), ('[0,0,0,0,0,1]','lon')]
    for split in splits:
        for attention in attention_list:
            for seed in range(1, 6):
                out_prefix = "lr_" + lr +  "_maxtok_" + maxtok + \
                        "_lay_" + lay + "_embed_dim_" + embed_dim + \
                        "_kernel_" + kernel + \
                        "_do_" + do + "_attention_" + attention[1]
                save_dir = os.path.join(args['save_dir'], split, out_prefix) + '/seed_' + str(seed)
                train_command = 'python ./train.py ' + args[split] + \
                        ' --clip-norm 0.1' + \
                        ' --max-tokens ' +  maxtok + \
                        ' --save-dir ' + save_dir + \
                        ' --max-epoch 1' + \
                        ' --no-epoch-checkpoints' + \
                        ' --lr ' + lr + \
                        ' --encoder-embed-dim ' + embed_dim + \
                        ' --encoder-layers ' + '\"[('+embed_dim+', '+kernel+')] * '+ lay + '\"' + \
                        ' --decoder-embed-dim ' + embed_dim + \
                        ' --decoder-layers ' + '\"[('+embed_dim+', '+kernel+')] * '+ lay + '\"' + \
                        ' --decoder-out-embed-dim ' + embed_dim + \
                        ' --optimizer nag' + \
                        ' --arch fconv' + \
                        ' --dropout ' + do + \
                        ' --decoder-attention ' + attention[0] + \
                        ' --seed ' + str(seed)

                train_dict[split].append(train_command)

                generate_command = 'python generate.py ' + args[split] + \
                        ' --path ' + save_dir + '/checkpoint_best.pt' + \
                        ' --batch-size 128' + \
                        ' --quiet' + \
                        ' --output ' + save_dir + '/accuracy.txt' + \
                        ' --beam 1'
                generate_dict[split].append(generate_command)

    with open(os.path.join(args['output_folder'], 'attention_exp_template_train_commands.txt'), 'w') as g:
        for elem in template_train_commands:
            g.write(elem)
            g.write('\n')

    with open(os.path.join(args['output_folder'], 'attention_exp_random_train_commands.txt'), 'w') as k:
        for elem in random_train_commands:
            k.write(elem)
            k.write('\n')

    with open(os.path.join(args['output_folder'], 'attention_exp_jump_train_commands.txt'), 'w') as l:
        for elem in jump_train_commands:
            l.write(elem)
            l.write('\n')

    with open(os.path.join(args['output_folder'], 'attention_exp_template_generate_commands.txt'), 'w') as p:
        for elem in template_generate_commands:
            p.write(elem)
            p.write('\n')

    with open(os.path.join(args['output_folder'], 'attention_exp_random_generate_commands.txt'), 'w') as q:
        for elem in random_generate_commands:
            q.write(elem)
            q.write('\n')

    with open(os.path.join(args['output_folder'], 'attention_exp_jump_generate_commands.txt'), 'w') as z:
        for elem in jump_generate_commands:
            z.write(elem)
            z.write('\n')

if __name__ == '__main__':
    main()
