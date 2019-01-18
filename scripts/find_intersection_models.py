import sys

first, second, third = [], [], []
first_models, second_models, third_models = [], [], []

def extract_info(elem):
    rank = int(elem.split('Model: ')[0].strip().split('| ')[1][:-1])
    model_name = elem.split('Model:')[1].split(', ')[0].strip()
    return rank, model_name

first_dict = {}
with open(sys.argv[1]) as f:
    tmp = f.readlines()
    for elem in tmp:
        first.append(extract_info(elem))
        first_models.append(extract_info(elem)[1])
        first_dict[extract_info(elem)[1]] = extract_info(elem)[0]

second_dict = {}
with open(sys.argv[2]) as s:
    tmp = s.readlines()
    for elem in tmp:
        second.append(extract_info(elem))
        second_models.append(extract_info(elem)[1])
        second_dict[extract_info(elem)[1]] = extract_info(elem)[0]

third_dict = {}
with open(sys.argv[3]) as t:
    tmp = t.readlines()
    for elem in tmp:
        third.append(extract_info(elem))
        third_models.append(extract_info(elem)[1])
        third_dict[extract_info(elem)[1]] = extract_info(elem)[0]


assert all(first[i][0] <= first[i+1][0] for i in range(len(first)-1))
assert all(second[i][0] <= second[i+1][0] for i in range(len(second)-1))
assert all(second[i][0] <= second[i+1][0] for i in range(len(second)-1))


finals = []
for elem in first_models:
    if elem in second_models and elem in third_models:
        finals.append(elem)

best = ''
best_rank = 9999999
n = 0
for i, elem in enumerate(finals):
    assert elem in first_dict
    assert elem in second_dict
    assert elem in third_dict
    print("| {}. Model: {}, jump_rank: {}, random_rank: {}, template_rank: {}\n".format(i+1, elem, first_dict[elem], second_dict[elem], third_dict[elem]))

    model_rank = max([ first_dict[elem], second_dict[elem], third_dict[elem] ])
    if model_rank < best_rank:
        best = elem
        best_rank = model_rank
        n = i + 1

print("| Best model: {}, best_rank {}, idx = {}".format(best, best_rank, n))







