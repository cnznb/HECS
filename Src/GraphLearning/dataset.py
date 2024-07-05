# -*- encoding = utf-8 -*-
"""
@description: Dataset construction
@date: 2024/1/17
@File : dataset.py
@Software : PyCharm
"""
import os
import random
from dhg.structure.graphs import Graph
import dhg
import numpy as np
import torch
import pandas as pd
import pickle


train_set = []
val_set = []
test_set = []


# Intra-class Dependency Hypergraph Construction
def convert_hypergraph(graph):
    hypergraph = []
    for v in graph.v:
        edges = [v]
        for e in graph.e[0]:
            in_vertex, out_vertex = e
            if out_vertex == v:
                edges.append(in_vertex)
        hypergraph.append(edges)
    return dhg.Hypergraph(graph.v, hypergraph)


# Intra-class Dependency Graph Construction
def create_digraph(path):
    edges = []
    v = 0
    with open(path + '\\graph_node.csv', "r", encoding="utf-8") as gr:
        # View all members of a class
        lines = gr.readlines()
        v += len(lines)
    if not os.path.exists(path + '\\graph.csv'):
        return dhg.Graph(v, edges)
    with open(path + '\\graph.csv', "r", encoding="utf-8") as pr:
        for line in pr:
            line = line.strip('\n').split(',')
            edges.append([int(line[0]), int(line[1])])
    return dhg.Graph(v, edges)


def create_hyperlink(path):
    v = 0
    positive = []
    negative = []
    with open(path + "\\graph_node.csv", 'r', encoding="utf-8") as gr:
        for line in gr:
            v += 1
            line = line.strip('\n').split(',')
            label = line[8]
            # Construct negative samples
            negative.append(int(line[0]))
            # Construct positive samples
            if label == "1":
                positive.append(int(line[0]))
    return dhg.Hypergraph(v, positive), dhg.Hypergraph(v, negative)

def l1_mormalize(features):
    return torch.nn.functional.normalize(features, p=1, dim=1)


# codebert codegpt codet5 cotext graphcodebert plbart
def get_features(path, name):
    features = []
    with open(path + "\\embedding\\" + name + ".csv", 'r', encoding="utf-8") as gr:
        for line in gr:
            line = [float(x) for x in line.strip('\n').split(',')]
            features.append(line)
    features_tensor = torch.tensor(features)
    features_tensor = l1_mormalize(features_tensor)
    return features_tensor


def solve(path, tag, emb_type):
    global train_set
    global val_set
    global test_set
    features = get_features(path, emb_type)
    g = create_digraph(path)
    hg = convert_hypergraph(g)
    link1, link2 = create_hyperlink(path)
    if tag == 1:
        train_set.append([hg, link1, features, torch.tensor(1)])
        train_set.append([hg, link2, features, torch.tensor(0)])
    elif tag == 2:
        val_set.append([hg, link1, features, torch.tensor(1)])
        val_set.append([hg, link2, features, torch.tensor(0)])
    elif tag == 3:
        test_set.append([hg, link1, features, torch.tensor(1)])
        test_set.append([hg, link2, features, torch.tensor(0)])



def scan_dir(path, tag, emb_type):
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if os.path.isdir(file_path):
            if file_name.startswith('1') or file_name.startswith('2'):
                solve(file_path, tag, emb_type)
            else:
                scan_dir(file_path, tag, emb_type)


def get_dataset(emb):
    global train_set
    global val_set
    global test_set
    train_set.clear()
    val_set.clear()
    test_set.clear()

    print("prepare dataset")
    scan_dir('E:\\dataset\\train', 1, emb)
    scan_dir('E:\\dataset\\val', 2, emb)
    scan_dir('E:\\dataset\\test', 3, emb)
    print(f'train_set: {len(train_set)}, val_set: {len(val_set)}, test_set: {len(test_set)}')
    return train_set, val_set, test_set
