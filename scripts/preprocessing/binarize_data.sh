path=$1
dest=$2

python preprocess.py -s co -t ac --trainpref $path/train --validpref $path/valid --test $path/test --destdir $dest

