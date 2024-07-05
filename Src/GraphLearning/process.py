# -*- encoding = utf-8 -*-
"""
@description: Using Javalang to process the properties of relevant classes in the dataset
@date: 2024/1/10
@File : process.py
@Software : PyCharm
"""
import csv
import os
import re
import shutil

import javalang
import numpy as np
import pandas as pd


def copy_file(src, dst, path):
    for f in os.listdir(path+"\\source"):
        if f == dst:
            return
    shutil.copy(os.path.join(path, src), os.path.join(path+"\\source", dst))


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        return content

def get_source_file(path):
    with open(path + '\\extract_range.csv', 'r') as er:
        ls = er.read().split('\n')
        rgs = [x for x in ls[0].split(',')]
        class_name = rgs[0]
        return class_name + '.java'


def get_target_file(path):
    with open(path + '\\target_range.csv', 'r') as er:
        ls = er.read().split('\n')
        rgs = [x for x in ls[0].split(',')]
        class_name = rgs[0]
        return class_name + '.java'

all = 0
# Using Javalang to obtain the method/field code range in each class
def solve(file_path):
    datas = pd.DataFrame({
        'id': pd.Series([], dtype=np.int64),
        'filename':  pd.Series([], dtype='str'),
        'class-entity': pd.Series([], dtype='str'),
        'c_st': pd.Series([], dtype=np.int64),
        'c_ed': pd.Series([], dtype=np.int64),
        'e_st': pd.Series([], dtype=np.int64),
        'e_ed': pd.Series([], dtype=np.int64),
        'tag': pd.Series([], dtype=np.int64),
        'label': pd.Series([], dtype=np.int64)
    }, columns=['id', 'filename', 'class-entity', 'c_st', 'c_ed', 'e_st', 'e_ed', 'tag', 'label'])
    # Tag 1 represents field, tag 2 represents method
    # print(file_path)
    # Reading Java file content
    idx = 0
    def split(path, idx, filename):
        global all
        data = pd.DataFrame({
            'id': pd.Series([], dtype=np.int64),
            'filename':  pd.Series([], dtype='str'),
            'class-method': pd.Series([], dtype='str'),
            'c_st': pd.Series([], dtype=np.int64),
            'c_ed': pd.Series([], dtype=np.int64),
            'e_st': pd.Series([], dtype=np.int64),
            'e_ed': pd.Series([], dtype=np.int64),
            'tag': pd.Series([], dtype=np.int64),
            'label': pd.Series([], dtype=np.int64)
        }, columns=['id', 'filename', 'class-entity', 'c_st', 'c_ed', 'e_st', 'e_ed', 'tag', 'label'])
        java_file = read_file(path)

        # 解析Java代码
        try:
            tree = javalang.parse.parse(java_file)
        except javalang.parser.JavaSyntaxError as e:
            print(f"A syntax error occurred while parsing Java code：{e}")
            all += 1
            return data, idx, False
        code = java_file.split('\n')
        codes = [''] + code
        have_target = False
        with open(file_path + '\\target_range.csv', 'r') as er:
            ls = er.read().split('\n')
            rgs = [x for x in ls[0].split(',')]
            target_class = rgs[0]
            lines = [int(x) for x in ls[1].split(',')]
        no_class_name = '-1'
        # Filter out methods and fields from class members
        for path, node in tree.filter(javalang.tree.TypeDeclaration):
            # Find class declaration
            # print(path, node.body)
            if isinstance(node, javalang.tree.ClassDeclaration) or isinstance(node, javalang.tree.InterfaceDeclaration) or isinstance(node, javalang.tree.EnumDeclaration):
                # Traverse class members
                enc = node.body.declarations if isinstance(node, javalang.tree.EnumDeclaration) else node.body
                c_st = node.position.line
                c_ed = c_st
                l, r = 0, 0
                for i in range(c_st, len(codes)):
                    l += codes[i].count('{')
                    r += codes[i].count('}')
                    if l == r and l != 0:
                        c_ed = i
                        break
                for member in enc:
                    # Find method declaration
                    no_class = node.name
                    if no_class_name == '-1':
                        no_class_name = no_class
                    if no_class == target_class:
                        have_target = True
                    if isinstance(member, javalang.tree.MethodDeclaration) or isinstance(member, javalang.tree.ConstructorDeclaration):
                        no_entity = member.name
                        start_line = member.position.line
                        end_line = member.position.line
                        l, r = 0, 0
                        for i in range(start_line, len(codes)):
                            l += codes[i].count('{')
                            r += codes[i].count('}')
                            if l == r and l != 0:
                                end_line = i
                                break
                        flag = 0
                        with open(file_path + '\\extract_range.csv', 'r') as er:
                            ls = er.read().split('\n')
                            rgs = [x for x in ls[0].split(',')]
                            class_name = rgs[0]
                            method_name = rgs[-1]
                            rgs = [int(x) for x in ls[1].split(',')]
                            if method_name == no_entity and ((rgs[0] >= start_line and rgs[1] <= end_line) or (
                                    rgs[0] <= start_line and rgs[1] >= end_line)):
                                flag = 1
                        if have_target and ((lines[0] >= start_line and lines[1] <= end_line) or (
                                    lines[0] <= start_line and lines[1] >= end_line)):
                            continue
                        new_row = {'id': idx, 'filename': filename, 'class-entity': no_class + '-' + no_entity, 'c_st': c_st, 'c_ed': c_ed, 'e_st': start_line, 'e_ed': end_line, 'tag': 2, 'label': flag}
                        data.loc[len(data)] = new_row
                        idx += 1
                    elif isinstance(member, javalang.tree.FieldDeclaration):
                        no_entity = member.declarators[0].name
                        start_line = member.position.line
                        end_line = member.position.line
                        lc = 0
                        rc = 0
                        for i in range(start_line, len(codes)):
                            lc += len(re.findall('{', codes[i]))
                            rc += len(re.findall('}', codes[i]))
                            if re.search(';', codes[i]) and lc == rc:
                                end_line = i
                                break
                        new_row = {'id': idx, 'filename': filename, 'class-entity': no_class + '-' + no_entity, 'c_st': c_st, 'c_ed': c_ed, 'e_st': start_line, 'e_ed': end_line,
                                   'tag': 1, 'label': 0}
                        # data = data.append(new_row, ignore_index=True)
                        data.loc[len(data)] = new_row
                        idx += 1

        return data, idx, have_target, no_class_name

    is_empty = True
    have_target = False
    dir = file_path + "\\source"
    for f in os.listdir(dir):
        if f == 'source.java':
            f_path = os.path.join(dir, f)
            os.remove(f_path)
        elif f == 'target.java':
            f_path = os.path.join(dir, f)
            os.remove(f_path)
    for root, dirs, files in os.walk(dir):
        for filename in files:
            if filename.endswith(".java"):
                is_empty = False
                data, idx, target_tag, _ = split(os.path.join(root, filename), idx, filename)
                datas = pd.concat([datas, data], ignore_index=True)
                if target_tag:
                    have_target = True
    if is_empty:
        datas, idx, _, no_class = split(file_path + "\\" + get_source_file(file_path), idx, get_source_file(file_path))
        copy_file(get_source_file(file_path), get_source_file(file_path), file_path)
    if not have_target:
        data, idx, _, no_class = split(file_path + "\\" + get_target_file(file_path), idx, get_target_file(file_path))
        datas = pd.concat([datas, data], ignore_index=True)
        copy_file(get_target_file(file_path), get_target_file(file_path), file_path)
    datas.to_csv(file_path + '\\graph_node.csv', sep=',', header=False, index=False, encoding='utf-8')
    datas.drop(datas.index, inplace=True)


# Recursive scanning dataset
def scan_dir(path):
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if os.path.isdir(file_path):
            if file_name.startswith('1') or file_name.startswith('2'):
                solve(file_path)
            else:
                scan_dir(file_path)


scan_dir('E:\\dataset\\train')
print(all)