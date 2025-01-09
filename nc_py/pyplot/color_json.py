import os
import json

def get_color():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    # 获取父级路径
    parent_directory = os.path.dirname(current_directory)
    json_file = 'json/color.json'
    # 获unit.json文件
    file_path = os.path.join(parent_directory, json_file)
    with open(file_path, 'r') as file:
        unit_data = json.load(file)
        return unit_data
