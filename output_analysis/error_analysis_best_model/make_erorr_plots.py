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

plt.bar(ind,proportions)

plt.xticks(ind,commands,rotation=90)
plt.ylim((0,0.55))

plt.title(sys.argv[2])

plt.tight_layout()

plt.savefig(sys.argv[3])
plt.close()

# N=5
# ind=np.arange(N)
# p1=plt.bar(ind,(2,2,2,2,2))
# p2=plt.bar(ind,(3,3,3,3,3),bottom=(2,2,2,2,2))
# plt.show()

# L	False_False	False_True	True_False	True_True
