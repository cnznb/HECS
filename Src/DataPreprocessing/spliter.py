# -*- encoding = utf-8 -*-
"""
@description: Cut the vectors of each class method into its own directory
@date: 2023/4/10 19:44
@File : spliter
@Software : PyCharm
"""
import javalang
import re
import os
import numpy as np
import pandas as pd
import csv
from javalang.tree import MethodDeclaration


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        return content


# Using Javalang to obtain the method/field code range in each class
def solve(file_path):
    data = pd.DataFrame({
        'id': pd.Series([], dtype=np.int64),
        'name': pd.Series([], dtype='str'),
        'st': pd.Series([], dtype=np.int64),
        'ed': pd.Series([], dtype=np.int64),
        'tag': pd.Series([], dtype=np.int64)
    }, columns=['id', 'name', 'st', 'ed', 'tag'])
    print(file_path)
    # 读取Java文件内容

    # file_path = 'E:\\dataset\\eucalyptus\\10030'
    java_file = read_file(file_path + '\\old.java')
    # 解析Java代码
    tree = javalang.parse.parse(java_file)
    code = java_file.split('\n')
    codes = [''] + code
    # print(codes)
    with open(file_path + '\\class_range.csv', 'r') as fp:
        ranges = [int(x) for x in fp.read().split('\n')[0].split(',')]
    # print(ranges)
    # 筛选出类成员中的方法和字段
    Mnames = []
    Mlines = []
    for path, node in tree.filter(javalang.tree.MethodDeclaration):
        if node.position is not None:
            start_line, _ = node.position

            if start_line < ranges[0]:
                continue
            elif start_line > ranges[1]:
                break
            else:
                Mnames.append(node.name)
                Mlines.append(start_line)
    for i in range(0, len(Mlines)):
        def search(st):
            ed = ranges[1] - 1
            lc = 0
            rc = 0
            for i in range(st, ranges[1]):
                lc += len(re.findall('{', codes[i]))
                rc += len(re.findall('}', codes[i]))
                if lc == rc and lc != 0 and rc != 0:
                    ed = i
                    break
            return ed

        ed = search(Mlines[i])
        flag = 0
        with open(file_path + '\\extract_range.csv', 'r') as er:
            ls = er.read().split('\n')
            for li in ls:
                if li == '':
                    continue
                rgs = [int(x) for x in li.split(',')]
                if (rgs[0] >= Mlines[i] and rgs[1] <= ed) or (rgs[0] <= Mlines[i] and rgs[1] >= ed):
                    flag = 1
                    break

        new_row = {'id': i, 'name': Mnames[i], 'st': Mlines[i], 'ed': ed, 'tag': flag}
        data = data.append(new_row, ignore_index=True)
    # print(data)
    data.to_csv(file_path + '\\method_range.csv', sep=',', header=None, index=None, encoding='utf-8')
    print("######################################")
    data.drop(data.index, inplace=True)
    Fnames = []
    Flines = []

    for path, node in tree.filter(javalang.tree.FieldDeclaration):
        if node.position is not None:
            start_line, _ = node.position
            # print(node.declarators[0].name,  node.position)
            if start_line < ranges[0]:
                continue
            elif start_line > ranges[1]:
                break
            else:
                Fnames.append(node.declarators[0].name)
                Flines.append(start_line)
    for i in range(0, len(Flines)):
        def search(st):
            ed = ranges[1] - 1
            lc = 0
            rc = 0
            for i in range(st, ranges[1]):
                lc += len(re.findall('{', codes[i]))
                rc += len(re.findall('}', codes[i]))
                if re.search(';', codes[i]) and lc == rc:
                    ed = i
                    break
            return ed

        ed = search(Flines[i])
        flag = 0
        with open(file_path + '\\extract_range.csv', 'r') as er:
            ls = er.read().split('\n')
            for li in ls:
                if li == '':
                    continue
                rgs = [int(x) for x in li.split(',')]
                if (rgs[0] >= Flines[i] and rgs[1] <= ed) or (rgs[0] <= Flines[i] and rgs[1] >= ed):
                    flag = 1
                    break
        new_row = {'id': i + len(Mlines), 'name': Fnames[i], 'st': Flines[i], 'ed': ed, 'tag': flag}
        data = data.append(new_row, ignore_index=True)
    # print(data)
    data.to_csv(file_path + '\\field_range.csv', sep=',', header=None, index=None, encoding='utf-8')
    # print("######################################")


open_id = 0
datasets = pd.DataFrame({
    'id': pd.Series([], dtype=np.int64),
    'code': pd.Series([], dtype='str'),
}, columns=['id', 'code'])
# read method vector file
source = pd.read_csv('../../../astnn/data/embedding.tsv', sep='\t', header=None, encoding='utf-8')
source.columns = ['id', 'code']


# Cut the vectors of each class method into its own directory
def get_tsv(path):
    global open_id
    global datasets
    print(path)
    java_file = read_file(path + '\\old.java')
    code = java_file.split('\n')
    codes = [''] + code
    with open(path + '\\method_range.csv', 'r') as fp:
        lines = fp.read().split('\n')
        # print(lines)
        for line in lines:
            if line == '':
                break
            code_line = ''
            ranges = [int(x) for x in line.split(',')[-2:]]
            for i in range(ranges[0], ranges[1] + 1):
                code_line += codes[i].rstrip() + '\n'
            new_row = {'id': open_id, 'code': code_line}
            datasets = datasets.append(new_row, ignore_index=True)
            # if os.path.exists(path+'\\method_embedding.csv'):
            #     os.remove(path+'\\method_embedding.csv')
            with open(path+'\\method_embedding.csv', 'a', newline='') as csv_file:
                writer = csv.writer(csv_file)
                data = source.iloc[open_id]['code']
                datas = [float(x) for x in data[1:-1].split(',')]
                writer.writerow(datas)
            open_id += 1


# Recursive scanning dataset
def scan_dir(path):
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)

        if os.path.isdir(file_path):
            if file_name.startswith('1'):
                solve(file_path)
                # get_tsv(file_path)
            else:
                scan_dir(file_path)

# 示例调用
scan_dir('E:/datasets')
