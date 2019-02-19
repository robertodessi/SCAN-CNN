import sys

l1 = l2 = []
with open(sys.argv[1]) as f:
    l1 = f.readlines()
with open(sys.argv[2]) as g:
    l2 = g.readlines()

assert len(l1) == len(l2), 'len'
real_true1 = real_true2 = 0
outp = open('./output.txt', 'w')
for i, elem in enumerate(zip(l1, l2)):
    if i != len(l1) - 1:
        m1, m2 = elem[0], elem[1]
        lm1 = m1.strip().split('\t')
        lm2 = m2.strip().split('\t')

        # counting how main correct commands for m1 and for m2
        real_true1 += 1 if eval(lm1[-1]) else 0
        real_true2 += 1 if eval(lm2[-1]) else 0

        # checking input_str is equal
        assert lm1[0] == lm2[0], '1'
        # checking gold_truth is equal
        assert lm1[2] == lm2[2], '2'

        out = '{}\t{}\t{}\t{}\t{}\t{}'.format(lm1[0], lm1[1], lm2[1], lm1[-1], lm2[-1], lm1[2])
        outp.write(out)
        outp.write('\n')
    else:
        final1 = 'Model_1: ' + elem[0]
        final2 = 'Model_2: ' + elem[1]

        # saving number of correctly translated commands
        true1 = int(final1.split(' ' )[3])
        true2 = int(final2.split(' ' )[3])

        assert real_true1 == true1, '3'
        assert real_true2 == true2, '4'

        outp.write(final1)
        outp.write(final2)

outp.close()

