import numpy as np
import matplotlib.pyplot as plt
import sys

# arguments: input data file, plot name, file name

command_list = []
proportion_list = []

with open(sys.argv[1]) as f:
    for line in f:
        mylist = line.strip().split("\t")
        command_list.append(mylist[0])
        proportion_list.append(float(mylist[1]))

commands=np.asarray(command_list)
proportions=np.asarray(proportion_list)

ind=np.arange(commands.size)

f = plt.figure(figsize=(8,4), frameon=False)

plt.bar(ind,proportions)

plt.xticks(ind,commands, fontsize=18, rotation=60)
#plt.ylim((0,0.55))
y_list = np.arange(0, 0.51, 0.1)
plt.yticks(y_list, fontsize=18)

plt.title(sys.argv[2], fontsize=20)

plt.tight_layout()

f.savefig('/Users/robertodessi/Desktop/SCAN-CNN/writeups/acl2019/figures/' + sys.argv[3] + '.png', format='png', bbox_inches='tight')#, dpi=50)
plt.close()

# N=5
# ind=np.arange(N)
# p1=plt.bar(ind,(2,2,2,2,2))
# p2=plt.bar(ind,(3,3,3,3,3),bottom=(2,2,2,2,2))
# plt.show()

# L	False_False	False_True	True_False	True_True
