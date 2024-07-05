# -*- encoding = utf-8 -*-
"""
@description: Generate your own graphical dataset by imitating the Cora graphical dataset, making it meet the input of GraphSmote
@date: 2023/12/29 9:39
@File : Graph_builder
@Software : PyCharm
"""
import csv
import os
import random
from scipy.spatial.distance import pdist, squareform
import torch
from torch_geometric.data import Data
from torch_geometric.datasets import TUDataset, Planetoid
from torch_geometric.loader import DataLoader
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
import numpy as np



train_dataset = []
val_dataset = []
test_dataset = []
edge_line_nums = []
edge_line2vec = {}
edge_labels = {}
edge_vec_dim = 0
edge_line_num = 0

def solve(path):
    global tot
    global edge_labels
    lbs = []
    def read_file(pt):
        if not os.path.exists(pt):
            return
        with open(pt, 'r') as fp:
            lines = fp.read().split('\n')
            # print(lines)
            for line in lines:
                if line == '':
                    break
                ranges = [int(x) for x in line.split(',')[-2:]]
                flag = 0
                with open(path + '\\extract_range.csv', 'r') as er:
                    ls = er.read().split('\n')
                    for li in ls:
                        if li == '':
                            continue
                        rgs = [int(x) for x in li.split(',')]
                        if (rgs[0] >= ranges[0] and rgs[1] <= ranges[1]) or (rgs[0] <= ranges[0] and rgs[1] >= ranges[1]):
                            flag = 1
                            break

                if flag == 1:
                    lbs.append(1)
                else:
                    lbs.append(0)
    read_file(path + '\\method_range.csv')
    read_file(path + '\\field_range.csv')
    for ix in range(len(lbs)):
        edge_labels[ix+tot] = lbs[ix]
    ebs = []
    with open(path + '\\method_embedding.csv', 'r') as me:
        lines = me.read().split('\n')
        for line in lines:
            if line == '':
                continue
            li = [float(x) for x in line.split(',')]
            ebs.append(li)
    # codeBERT codeGPT codeT5 coTexT graphCodeBERT PLBART
    if os.path.exists(path + '\\codeEmbedding\\codeGPT.csv'):
        with open(path + '\\codeEmbedding\\codeGPT.csv', 'r') as fe:
            lines = fe.read().split('\n')
            for line in lines:
                if line == '':
                    continue
                li = [float(x) for x in line.split(',')]
                ebs.append(li)
    el = []
    er = []
    if os.path.exists(path + '\\relation.csv'):
        with open(path + '\\relation.csv', 'r') as re:
            lines = re.read().split('\n')
            for line in lines:
                if line == '':
                    continue
                li = [int(x)+tot for x in line.split(',')]
                with open('test.txt', mode='a', newline='') as file:
                    writer = csv.writer(file, delimiter=' ')
                    writer.writerow(li)
                el.append(li[0]+tot)
                el.append(li[1]+tot)
                er.append(li[1]+tot)
                er.append(li[0]+tot)
    cent = []
    for i in range(len(lbs)):
        ct = [tot+i]
        for x in ebs[i]:
            ct.append(float(x))
        ct.append(lbs[i])
        cent.append(ct)
    with open('cora.content', mode='a', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        for row in cent:
            writer.writerow(row)
    tot += len(lbs)
    lbs = np.array(lbs, dtype=int)
    ebs = np.array(ebs)
    edge = np.array([el, er])

    labels = torch.tensor(lbs, dtype=torch.int)
    x = torch.tensor(ebs, dtype=torch.float)
    edge = torch.tensor(edge, dtype=torch.long)
    data = Data(x=x, edge_index=edge.contiguous(), y=labels)
    return data

def train_search(path):
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if os.path.isdir(file_path):
            if file_name.startswith('1'):
                xi = tot-1
                train_dataset.append(solve(file_path))
                print(path, xi, tot-1)

            else:
                train_search(file_path)

def test_search(path):
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if os.path.isdir(file_path):
            if file_name.startswith('1'):
                xi = tot-1
                test_dataset.append(solve(file_path))
                print(path, xi, tot-1)
            else:
                test_search(file_path)
tot = 1
train_search('E:/datasets/train')
test_search('E:/datasets/test)
print(len(train_dataset))
print(len(test_dataset))
