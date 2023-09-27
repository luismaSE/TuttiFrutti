#!/usr/bin/python3
import socket, sys , click , pickle , time,  re

@click.command()
@click.option('-h','host',default="::",help='')
@click.option('-n','--nickname',default='invitado',help="Ingresa tu nombre de usuario")
@click.option('-p','--port',default=5000,help="puerto del server donde a conectar")

    
def client(host,nickname,port):
    if re.match(r"(\d{1,3}\.){3}\d{1,3}",host) :
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.connect((host,int(port)))
    send_pickle_msg(s,nickname)    
    while True:
        msg_in = recv_msg(s)
        print(msg_in)
        
        if 'ngres' in msg_in:
            msg_out = input('> ')
            send_msg(s,msg_out)
            if msg_out == 'exit':
                break
        elif msg_in[-1] == "*":
            msg_out == 'ack'
            send_msg(s,msg_out)
        elif 'GAME OVER' in msg_in:
            break
    s.close()
    sys.exit()



def send_pickle_msg(s,msg):
    s.sendall(pickle.dumps(msg))
    
def send_msg(s,msg):
    s.sendall(msg.encode())
        
def recv_pickle_msg(s):
    return pickle.loads(s.recv(1024))

def recv_msg(s):
    return s.recv(1024).decode()
    
    
if __name__ == '__main__':
    client()