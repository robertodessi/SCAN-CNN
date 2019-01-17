import sys

def fix_name(string):
    ll = string.split('_')
    temp_name = ll[4:6] + ll[-2:] + ll[2:4] + ll[:2] + ll[8:10] + ll[6:8]
    new_name = '_'.join(temp_name)
    return new_name

lines = []
with open(sys.argv[1]) as f:
    lines = f.readlines()

for elem in lines:
    final = []
    final.append(elem.split('Model: ')[0])
    model_name = elem.split('Model:')[1].split(', ')[0].strip()
    final.append("Model: " + fix_name(model_name))
    final.append(", " + " ".join(elem.split('Model:')[1].split(', ')[1:]))
    to_write = "".join(final).replace('dim', 'embed_dim')
    print(to_write.strip())



