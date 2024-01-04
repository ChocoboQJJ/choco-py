'''
Author: ChocoboQJJ ChocoboQJJ@gmail.com
Date: 2024-01-04 09:30:57
Description: json文件路径深层检索工具
'''
import os
import json
import re

def find_json_files(directory):
    json_files = []
    json_count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                relative_path = os.path.relpath(os.path.join(root, file), directory).replace('\\', '/')
                json_files.append(relative_path)
                json_count += 1
    print(f"json文件数量: {json_count}")
    return json_files

def save_to_json(json_files, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_files, f, ensure_ascii=False)
    print(f"地址路径数量: {len(json_files)}")
    print(f"输出文件所在位置: {os.path.abspath(output_file)}")

# 主函数，处理命令行参数
def main():
    directory = input("请输入目录路径: ")  # 获取用户输入的目录路径
    while not os.path.exists(directory):
        print("路径不存在，请重新输入")
        directory = input("请输入目录路径: ")

    output_file = input("请输入输出文件名: ")  # 获取用户输入的输出文件名
    while re.search(r'[\\/:*?"<>|]', output_file):
        print("文件名包含非法字符，请重新输入")
        output_file = input("请输入输出文件名: ")
    if not output_file.endswith('.json'):
        output_file += '.json'

    json_files = find_json_files(directory)
    save_to_json(json_files, output_file)

if __name__ == '__main__':
    main()