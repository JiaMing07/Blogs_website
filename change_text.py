import os
import json

def replace_case(old, new, text):
    index = text.lower().find(old.lower())
    if index == -1:
        return text
    return replace_case(old, new, text[:index] + new + text[index + len(old):])


def change_text():
    '''
    更换text中的JavaScript，以防止被标上Java标签
    :return:
    '''
    file_list1 = os.listdir("./data")
    file_list2 = os.listdir("./datas")
    for i in range (0, len(file_list1)):
        file1 = file_list1[i]
        file2 = file_list2[i]
        with open(f"./data/{file1}", 'r', encoding = "utf-8") as f1:
            old_data = json.load(f1)
        with open(f"./datas/{file2}", 'r', encoding = "utf-8") as f2:
            new_data = json.load(f2)
        text = old_data['text']
        text = replace_case("JavaScript", "Jav1Script", text)
        new_data['text'] = text
        f = open(f'./datas/{file2}', "w+", encoding="utf-8")
        json.dump(new_data, f, ensure_ascii=False, indent=4)
        f.close()


if __name__ == '__main__':
    change_text()