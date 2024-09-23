import os
import json
import matplotlib.pyplot as plt
import numpy as np


def get_dic(file_list, str):
    dic= {}
    num = 0
    cnt = 0
    for i in range(0, len(file_list)):
        with open(f'./data/{file_list[i]}', 'r', encoding="utf-8") as f:
            data = json.load(f)
        if data['author_pic'][12:12+len(str)] == str:
            num = num + 1
            year = data['pub_date'][0:4]
            if year == '2021':
                print(year)
                cnt = cnt + 1
    return cnt


def compare():
    file_list = os.listdir("./data")
    python_num = get_dic(file_list, 'python')
    java_num = get_dic(file_list, 'Java')
    javascript_num = get_dic(file_list, 'JavaScript')
    php_num = get_dic(file_list, 'PHP')
    name_list = ['Python', 'Java', 'JavaScript', 'PHP']
    num_list = [python_num, java_num, javascript_num, php_num]
    print(num_list)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.xlabel('名称')
    plt.ylabel('文章数')
    plt.bar(name_list, num_list,label='2021年有关不同语言的文章数目')
    plt.legend()
    plt.show()


def count_num(str):
    num = 0
    cnt = 0
    file_list = os.listdir("./data")
    print(len(file_list))
    for i in range(0, len(file_list)):
        with open(f'./data/{file_list[i]}', 'r', encoding="utf-8") as f:
            data = json.load(f)
        if data['author_pic'][12:12 + len(str)] == str:
            num = num + 1
    return num

if __name__ == '__main__':
    compare()
    search_list = ["python", "C1", "C2", "Java", "JavaScript", "PHP", "SQL", "Rust", 'Golang']
    for i in range(0,9):
        print(count_num(search_list[i]))
