import sys
import math
import numpy
from sklearn.metrics import f1_score
from scipy.optimize import linear_sum_assignment
# from ClusterMetrics import ConfusionMatrix

def intersection(a, b):
    return list(set(a) & set(b))

def union(a, b):
    return list(set(a) | set(b))

def dict_to_list(conv):
    t_id_list = []
    ts_list = []
    for t_id, t_list in conv.items():
        for ts in t_list:
            t_id_list.append(t_id)
            ts_list.append(ts)
    ts_list, t_id_list = zip(*sorted(zip(ts_list, t_id_list)))
    return t_id_list

def entropy(convo):
    entr = 0.0
    n = sum(len(v) for v in convo.values())
    for thread_id in convo.keys():
        f = len(convo[thread_id]) / n
        entr += f * math.log(f, 2)
    return abs(entr)


def processFile(filename):
    conv_dict = {}
    with open(filename, 'r', encoding='latin1') as f:
        idx = 1
        for line in f:
            if not line.isspace():
                parts = line.split(' ')
                thread_id = parts[0]
                timestamp = parts[1]
                if timestamp == '0':
                    timestamp = str(idx)
                # remove 'T' in the thread
                thread_id = int(thread_id[1:])
                if thread_id not in conv_dict.keys():
                    conv_dict[thread_id] = list()
                conv_dict[thread_id].append(timestamp)
                idx = idx + 1
    return conv_dict


def f_measure_micro(convo1, goldset):
    f_micro = 0.0
    n = sum(len(v) for v in convo1.values())
    for g_t_id, g_t_list in goldset.items():
        max_pair_score = 0.0
        for t_id, t_list in convo1.items():
            prec = len(intersection(t_list,g_t_list)) / len(t_list)
            recall =  len(intersection(t_list,g_t_list)) / len(g_t_list)
            if (prec + recall) > 0.0:
                pair_score = (2 * prec * recall) / (prec + recall)
                if pair_score > max_pair_score:
                    max_pair_score = pair_score
        f_micro += (len(g_t_list) / n) * max_pair_score
    return f_micro


def one_to_one_acc(convo1, goldset):
    cost_mat = numpy.zeros((max(convo1.keys()), max(goldset.keys())))
    for t_id, t_list in convo1.items():
        for g_t_id, g_t_list in goldset.items():
            cost_mat[t_id-1,g_t_id-1] = len(intersection(t_list,g_t_list))
    row_ind, col_ind = linear_sum_assignment(cost_mat * -1)
    right = 0
    for row, col in zip(row_ind, col_ind):
        right += cost_mat[row, col]
    total = cost_mat.sum()
    return right / total


# def one_to_one_acc_elsner(convo1, goldset):
#     cm = ConfusionMatrix()
#     for gold, proposed in zip(dict_to_list(goldset), dict_to_list(convo1)):
#         cm.add(gold, proposed)
#     return cm.eval_mapping(cm.one_to_one_optimal_mapping(), verbose=False)[2]


if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("\tExample:\tpython compareChat.py conversation.txt goldset.txt")
        sys.exit()

    convo1 = processFile(sys.argv[1])
    goldset = processFile(sys.argv[2])
    comp_measure = 0.0
    if (entropy(convo1) > entropy(goldset)):
        comp_measure = f_measure_micro(convo1, goldset)
    else:
        comp_measure = f_measure_micro(goldset, convo1)
    one2one = one_to_one_acc(convo1, goldset)
    #print('micro-averaged f-score:' + str(comp_measure))
    print(sys.argv[1] + "," + sys.argv[2] + "," + str(comp_measure) + "," + str(one2one))
