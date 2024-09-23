import os
import json
import matplotlib.pyplot as plt
import numpy as np


def python_article():
    file_list = os.listdir("./data")
    print(len(file_list))
    dic = {}
    for i in range(0, len(file_list)):
        with open(f'./data/{file_list[i]}', 'r', encoding="utf-8") as f:
            data = json.load(f)
        if data['author_pic'][12:18] == 'python':
            year = data['pub_date'][0:4]
            if year in dic:
                tmp = dic[year]
                dic[year] = tmp + 1
            else:
                dic[year] = 0
    print(dic['2019'])
    year_list = []
    num_list = []
    for y, num in dic.items():
        year_list.append(y)
        num_list.append(num)
    print(year_list)
    print(num_list)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.xlabel('年份')
    plt.ylabel('文章数')
    plt.plot(year_list, num_list)
    plt.show()


if __name__ == '__main__':
    python_article()
