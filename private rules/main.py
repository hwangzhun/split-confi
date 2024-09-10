import os
import json
import requests

# Json 文件路径
json_file_path = os.path.join(os.path.dirname(__file__), 'rules.json')

def load_json(json_file_path):
    """加载 JSON 文件"""
    with open(json_file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# 加载 JSON 数据
json_data = load_json(json_file_path)

# 获取上层目录路径并指向 rules 文件夹
rules_dir = os.path.join(os.path.dirname(__file__), '..', 'rules')

# 如果目录不存在，则创建它
os.makedirs(rules_dir, exist_ok=True)

# 遍历 JSON 列表
for service in json_data:
    service_name = service['name']
    service_type = service['type']

    # 生成文件名：Service Name + type
    output_file = f"{service_name}.{service_type}"
    output_path = os.path.join(rules_dir, output_file)  # 保存到上层目录的 rules 文件夹

    with open(output_path, 'w', encoding='utf-8') as outfile:
        # 遍历 links 并下载每个链接的内容
        for link in service['links']:
            link_name = link['name']
            link_url = link['url']
            
            try:
                response = requests.get(link_url)
                response.raise_for_status()  # 检查请求是否成功
                
                # 将远程文件内容写入新的文件
                outfile.write(f"# {link_name} content from {link_url}\n")  # 添加注释，标明来源
                outfile.write(response.text)
                outfile.write("\n\n")  # 添加换行分隔不同链接的内容
                
                print(f"Downloaded and written content from {link_url}")
            
            except requests.exceptions.RequestException as e:
                print(f"Error downloading {link_url}: {e}")

    print(f"All content written to: {output_path}")