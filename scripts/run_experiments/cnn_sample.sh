#!/bin/bash 
date

data_bin=$1
save_dir=$2 


for lr in 0.1 0.01 0.001
do
    for max_tokens in 25 50 100 200 500 1000
    do  
        for layers in 6 7 8 9 10
        do  
            for embed_dim in 128 256 512 
            do  
                for kernel_width in 3 4 5 
                do  
                    for dropout in 0 0.25 0.5 
                    do  
                        for seed in 1 2 3 4 5
                        do

                            out_prefix="lr_"$lr"_maxtok_"$max_tokens"_lay_"$layers"_embed_dim_"$embed_dim"_kernel_"$kernel_width"_dropout_"$dropout
                            mkdir $save_dir'/'$out_prefix 
                            
                            python ./train.py $data_bin \
                                --clip-norm 0.1 \
                                --max-tokens $max_tokens \
                                --save-dir $save_dir'/'$out_prefix'/seed_'$seed \
                                --max-epoch 1 \
                                --no-epoch-checkpoints \
                                --lr $lr \
                                --encoder-embed-dim $embed_dim \
                                --encoder-layers "[("$embed_dim", "$kernel_width")] * "$layers \
                                --decoder-embed-dim $embed_dim \
                                --decoder-layers "[("$embed_dim", "$kernel_width")] * "$layers \
                                --decoder-out-embed-dim $embed_dim \
                                --optimizer nag \
                                --arch fconv \
                                --dropout $dropout \
                                --decoder-attention True \
                                --seed $seed
                           
                            python generate.py $data_bin \
                                --path $save_dir"/"$out_prefix"/seed_"$seed"/checkpoint_best.pt" \
                                --batch-size 128 \
                                --quiet \
                                --output $save_dir'/'$out_prefix'/seed_'$seed'/accuracy.txt' \
                                --beam 1 
                        done
                    done 
                done
            done 
        done
    done
done

date
echo DONE
