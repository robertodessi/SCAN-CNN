import sys

split1 = sys.argv[1]
split2 = sys.argv[2]

l_1, l_2 = [], []
with open(split1) as f:
    l_1 = f.readlines()

with open(split2) as g:
    l_2 = g.readlines()


l_12 = [elem.split('\t')[0].strip() for elem in l_1]
l_22 = [elem.split('\t')[0].strip() for elem in l_2]

found = 0

for elem in l_1:
    l_1 = elem.split('\t')[0].strip()
    for elem2 in l_2:
        if l_1 == elem2.split('\t')[0].strip():
            found += 1
            print(elem)
            break

print("| Found {} common samples".format(found))



