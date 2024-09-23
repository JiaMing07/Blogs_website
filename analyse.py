import os
import json
import matplotlib.pyplot as plt
import numpy as np


def fans_read():
    file_list = os.listdir("./data")
    read_list = []
    fans_list = []
    for i in range(0, len(file_list)):
        with open(f'./data/{file_list[i]}', 'r', encoding="utf-8") as f:
            data = json.load(f)
        if data['read'][-1] == 'k':
            hot = int(float(data['read'][0:-1]) * 1000)
        else:
            hot = int(data['read'])
        if data['like'][-1] == 'k':
            fans = int(float(data['like'][0:-1]) * 1000)
        else:
            fans = int(data['like'])
        if hot < 10000:
            if fans<100:
                read_list.append(hot)
                fans_list.append(fans)
    print(len(read_list))
    print(len(fans_list))
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    colors1 = '#00CED1'  # 点的颜色
    area = np.pi * 0.05 ** 0.05  # 点面积
    plt.xlabel('阅读量')
    plt.ylabel('点赞数')

    plt.scatter(read_list, fans_list, s=area, c=colors1, label='阅读量与点赞数的关系图')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    fans_read()
