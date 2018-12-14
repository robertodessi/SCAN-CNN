#!/bin/bash
date

echo '##### SCAN repo does not exists'
echo '##### Cloning SCAN repository...'
git clone https://github.com/brendenlake/SCAN.git
mkdir SCAN/work
echo '##### Successfully downloaded the SCAN dataset'

echo '##### Copying train and test tasks for jump into a temp folder called work...'
cp SCAN/add_prim_split/tasks_train_addprim_jump.txt SCAN/work/
cp SCAN/add_prim_split/tasks_test_addprim_jump.txt SCAN/work/

mv create_dataset.py SCAN/work
cd SCAN/work
echo '##### Running a python script to create train and test splits from .txt files...'
python create_dataset.py

cd ../../

src=co
tgt=ac
exp_folder=scan-jump

echo '##### Creating folders data-bin, jump_exp results and checkpoints'
mkdir -p data-bin/$exp_folder
mkdir -p data/$exp_folder/
mkdir -p checkpoints/$exp_folder
mkdir -p results


cp SCAN/work/train.* data/$exp_folder
cp SCAN/work/valid.* data/$exp_folder
cp SCAN/work/test.* data/$exp_folder


echo '##### Preprocessing datasets to create binarized files...'

python preprocess.py --source-lang $src --target-lang $tgt --trainpref \
	data/$exp_folder/train --validpref data/$exp_folder/valid --testpref \
	data/$exp_folder/test --destdir data-bin/$exp_folder


echo '##### Starting the experiments'
for embedding_dim in 128 256 512
do      
	for layers in 1 2 3 4 5 6 7 8 9 10
	do 
		for lr in 10 1 0.1 0.01 0.001
		do 
			for kernel_size in 5 4 3 2 1
			do 
				for max_tokens in 25 50 100 500 1000 2000
				do 
					for dropout in 0 0.25 0.5
					do
						out_prefix="dim_"$embedding_dim"_lay_"$layers"_lr_"$lr"_do_"$dropout"_kernel_"$kernel_size"_maxtok_"$max_tokens
						echo '--------------------------------------'
						echo '##### Evaluating model ' $out_prefix
						rm -f checkpoints/$exp_folder/*
						CUDA_VISIBLE_DEVICES=0 python ./train.py ./data-bin/$exp_folder --clip-norm 0.1 --max-tokens $max_tokens \
							--save-dir checkpoints/$exp_folder --max-epoch 1 --no-epoch-checkpoints \
							--encoder-embed-dim $embedding_dim \
							--encoder-layers '[('$embedding_dim', '$kernel_size')] * '$layers \
							--decoder-embed-dim $embedding_dim \
							--decoder-layers '[('$embedding_dim', '$kernel_size')] * '$layers \
							--decoder-out-embed-dim $embedding_dim \
							--lr $lr \
							--dropout $dropout \
						       	--optimizer nag \
							--arch fconv
							--decoder-attention True 
							#--seed N to set seed

						CUDA_VISIBLE_DEVICES=0 python generate.py data-bin/$exp_folder \
							--path checkpoints/$exp_folder/checkpoint_last.pt \
							--batch-size 128 \
							--quiet \
							--beam 1 | tee results/$out_prefix'.txt'
					done
				done
			done
		done
	done
done

cp find_best_models.py results/
cd results
python find_best_models.py

date
echo DONE
