'''
Author: ChocoboQJJ ChocoboQJJ@gmail.com
Date: 2024-01-03 17:25:30
Description: Json大文件拆分工具
'''
import json
import os
import zipfile
import time
from datetime import datetime

# 将文件打包成zip文件并删除原文件
def zip_files(files, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in files:
            zipf.write(file)
            os.remove(file)  # 删除文件
            
# 读取json文件
def read_json_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"源文件 {filename} 包含 {len(data)} 条数据")  # 打印数据条数
    return data

# 将数据拆分成多个部分，每部分的大小不超过max_size
def split_data(data, max_size=2*1024*1024):
    size = 0
    split_data = []
    current_data = []
    for item in data:
        item_size = len(json.dumps(item).encode('utf-8'))
        if size + item_size > max_size:
            split_data.append(current_data)
            current_data = [item]
            size = item_size
        else:
            current_data.append(item)
            size += item_size
    if current_data:
        split_data.append(current_data)
    return split_data

# 将拆分后的数据写入新的json文件
def write_json_files(split_data, base_filename):
    files = []
    for i, data in enumerate(split_data):
        filename = f"{base_filename}_{i}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)  # 设置ensure_ascii=False
        print(f"拆分后的文件 {filename} 包含 {len(data)} 条数据")  # 打印数据条数
        files.append(filename)
    return files  # 返回文件列表

# 拆分json文件并将拆分后的文件打包成zip文件
def split_json_file(filename, max_size):
    data = read_json_file(filename)
    split_data_list = split_data(data, max_size)
    base_filename, _ = os.path.splitext(filename)
    files = write_json_files(split_data_list, base_filename)
    zip_files(files, f"{base_filename}.zip")

# 处理目录下的所有json文件
def process_all_json_files(directory, max_size):
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            full_path = os.path.join(directory, filename)
            split_json_file(full_path, max_size)

# 主函数，处理命令行参数
def main():
    directory = input("请输入要处理的目录：")
    if not os.path.isdir(directory):
        print("输入的不是有效的目录，请重新运行脚本并输入有效的目录。")
        return

    max_size = input("请输入拆分后单个文件的期望大小(MB):")
    try:
        max_size = int(max_size) * 1024 * 1024  # 将大小从MB转换为字节
    except ValueError:
        print("输入的不是有效的数字，请重新运行脚本并输入有效的整数。")
        return

    start_time = time.time()  # 获取当前时间
    print(f"开始处理 {datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')}")

    process_all_json_files(directory, max_size)

    end_time = time.time()  # 获取当前时间
    print(f"处理完成 {datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')}")

    print(f"总计耗时: {end_time - start_time} 秒")

if __name__ == "__main__":
    main()