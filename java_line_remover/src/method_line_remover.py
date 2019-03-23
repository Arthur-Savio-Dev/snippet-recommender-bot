import re
import pandas as pd
import pcre
from find_removable_lines import *
from find_removable_blocks import *


def print_method_lines(method_lines):
    for i in method_lines:
        print(i)


def pre_process_method(lines):
    lines = lines.split('\n')
    lines = filter(lambda x: not re.match(r'^\s*$', x), lines)  # remove whitespaces after line
    lines = filter(lambda x: not re.match(r'^[\t]*[ ]*//', x), lines)  # remove lines that only have comments
    lines = list(lines)
    for i in range(len(lines)):
        lines[i] = re.sub(r'[ ]*//.*', '', lines[i])  # remove comments like "line of code // comment"
        lines[i] = re.sub(r'[ ]+$', '', lines[i])  # remove spaces after each line
    return lines


def add_method_by_method_lines(methods, current_method, method_lines):
    method = ''
    for i in method_lines:
        method += i + '\n'
    current_method.at['codes'] = method
    methods = methods.append(current_method)
    return methods


def generate_incomplete_method(methods, current_method, method_lines, removable_indexes):
    new_method_lines = []
    method_lines_size = len(method_lines)
    for i in range(method_lines_size):
        if i not in removable_indexes:
            new_method_lines.append(method_lines[i])
    methods = add_method_by_method_lines(methods, current_method, new_method_lines)
    return methods


def main():
    get_removable_line_blocks_indexes('test')
    df = pd.read_csv('./result.csv')
    methods = df.head(1)
    methods = methods.drop('id', axis=1)
    for index, row in methods.iterrows():
        method = row['codes']
        method_lines = pre_process_method(method)
        removable_indexes = get_removable_line_indexes(method_lines)
        removable_indexes_list = get_removable_indexes_variances(removable_indexes)
        current_method = methods.loc[index]
        methods = methods.drop(index)
        methods = add_method_by_method_lines(methods, current_method, method_lines)
        for i in removable_indexes_list:
            methods = generate_incomplete_method(methods, current_method, method_lines, i)
    methods = methods.reset_index()
    methods = methods.drop('index', axis=1)
    methods.to_csv('results_test.csv')


main()
