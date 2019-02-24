import numpy as np
import matplotlib.pyplot as plt
import sys

lengths_list = []
false_false_list = []
false_true_list = []
true_false_list = []
true_true_list = []

with open(sys.argv[1]) as f:
    for line in f:
        mylist = line.strip().split("\t")
        lengths_list.append(int(mylist[0]))
        false_false_list.append(float(mylist[1]))
        false_true_list.append(float(mylist[2]))
        true_false_list.append(float(mylist[3]))
        true_true_list.append(float(mylist[4]))

lengths=np.asarray(lengths_list)
false_false=np.asarray(false_false_list)
false_true=np.asarray(false_true_list)
true_false=np.asarray(true_false_list)
true_true=np.asarray(true_true_list)

ind=np.arange(lengths.size)

# plt.bar(ind,false_false)
# plt.bar(ind,false_true,bottom=false_false)
# plt.bar(ind,true_false,bottom=false_false+false_true)
# plt.bar(ind,true_true,bottom=false_false+false_true+true_false)

plt.bar(ind,true_false,)
plt.bar(ind,false_true,bottom=true_false)
plt.bar(ind,true_true,bottom=true_false+false_true)
plt.bar(ind,false_false,bottom=true_false+false_true+true_true)

plt.xticks(ind,lengths)

plt.legend(['only dec 1', 'only dec 5', 'both', 'neither'], bbox_to_anchor=(1.01,1),borderaxespad=0)

plt.subplots_adjust(right=0.8)

plt.savefig(sys.argv[2])
plt.close()

# N=5
# ind=np.arange(N)
# p1=plt.bar(ind,(2,2,2,2,2))
# p2=plt.bar(ind,(3,3,3,3,3),bottom=(2,2,2,2,2))
# plt.show()

# L	False_False	False_True	True_False	True_True
