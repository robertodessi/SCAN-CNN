#!/bin/bash
date

data_bin=$1
save_dir=$2
gpu=$3

echo '### Starting the experiments'

for lr in 0.1 0.01 0.001
do
    for max_tokens in 25 50 100 200
    do
        for enc_lay in 1 2
        do
            for dec_lay in 1 2
            do
                out_prefix="lr_"$lr"_maxtok"$max_tokens'_enc_lay_'$enc_lay'_dec_lay_'$dec_lay

                echo '--------------------------------------'
                echo '###  Evaluating model ' $out_prefix

                echo $save_dir'/'$out_prefix

                CUDA_VISIBLE_DEVICES=$gpu python ./train.py $data_bin \
                    --clip-norm 0.1 --max-tokens $max_tokens \
                    --save-dir $save_dir'/'$out_prefix \
                    --max-epoch 1 --no-epoch-checkpoints \
                    --lr $lr \
                    --optimizer nag \
                    --arch lstm_scan \
                    --encoder-layers $enc_lay \
                    --decoder-layers $dec_lay
 
                python generate.py $data_bin \
                    --path $save_dir'/'$out_prefix'/checkpoint_best.pt' \
                    --batch-size 128 \
                    --quiet \
                    --beam 1 > results/$out_prefix 
 
 
            done
        done
    done
done

date
echo DONE
