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

lengths_list2 = []
false_false_list2 = []
false_true_list2 = []
true_false_list2 = []
true_true_list2 = []

with open(sys.argv[2]) as g:
    for line in g:
        mylist2 = line.strip().split("\t")
        lengths_list2.append(int(mylist2[0]))
        false_false_list2.append(float(mylist2[1]))
        false_true_list2.append(float(mylist2[2]))
        true_false_list2.append(float(mylist2[3]))
        true_true_list2.append(float(mylist2[4]))

lengths2=np.asarray(lengths_list2)
false_false2=np.asarray(false_false_list2)
false_true2=np.asarray(false_true_list2)
true_false2=np.asarray(true_false_list2)
true_true2=np.asarray(true_true_list2)

ind2=np.arange(lengths2.size)

plt.close('all')

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.set_size_inches(16,16)

ax1.set_title(r"\textbf{JUMP}", fontsize=30)
ax1.bar(ind,true_false,)
ax1.bar(ind,false_true,bottom=true_false)
ax1.bar(ind,true_true,bottom=true_false+false_true)
ax1.bar(ind,false_false,bottom=true_false+false_true+true_true)

ax2.set_title(r"\textbf{AROUND-RIGHT}", fontsize=30)
ax2.bar(ind2,true_false2,)
ax2.bar(ind2,false_true2,bottom=true_false2)
ax2.bar(ind2,true_true2,bottom=true_false2+false_true2)
ax2.bar(ind2,false_false2,bottom=true_false2+false_true2+true_true2)

#plt.xticks(ind,lengths)
#ax1.xticks(ind,lengths)
#ax2.xticks(ind,lengths)

y_list = [elem for elem in np.arange(0, 1.1, 0.2)]
ax1.xaxis.set_ticks(ind)
ax1.set_xticklabels(lengths)
ax1.yaxis.set_ticks(y_list)
ax2.xaxis.set_ticks(ind2)
ax2.set_xticklabels(lengths2)
ax2.yaxis.set_ticks(y_list)


#plt.rcParams['axes.titlesize'] = 'x-large'
#plt.rcParams['axes.labelsize'] = 'medium'


ax1.tick_params(axis='x', labelrotation=45)
ax2.tick_params(axis='x', labelrotation=45)
#ax2.tick_params(axis='x', labelsize='10', labelrotation=45)

#plt.legend(['only dec 1', 'only dec 5', 'both', 'neither'], bbox_to_anchor=(1.01,1),borderaxespad=0)
#ax1.legend(['only dec 1', 'only dec 5', 'both', 'neither'], bbox_to_anchor=(1.01,1),borderaxespad=0)
#ax2.legend(['only dec 1', 'only dec 5', 'both', 'neither'], bbox_to_anchor=(1.01,1),borderaxespad=0)

#plt.subplots_adjust(right=0.8)

fig.savefig(sys.argv[3], format='png', bbox_inches='tight', dpi=100)
fig.savefig('out.png', format='png', bbox_inches='tight', dpi=100)
