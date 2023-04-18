#!/usr/bin/python3
import socket, sys , click , pickle , time

@click.command()
@click.option('-h','host',default="localhost",help='')
@click.option('-n','--nickname',default='invitado',help="Ingresa tu nombre de usuario")
@click.option('-ipv4',is_flag=True, flag_value=True,help="Espicifiación para realizar la conexion mediante IPv4, si no se especifica se utilizará IPv6")
@click.option('-p','--port',default=5000,help="puerto del server donde a conectar")
@click.option('-m','--match',default= 0 ,help="Codigo de la partida a la que me quiero unir")
@click.option('-r','--rounds',default=3,help="Cantidad de las rondas de la partida")
@click.option('-c','--categories',default=2,help="Cantidad de categorias que tendrá la partida")
@click.option('-s','--size',default=2,help="Cantidad de jugadores")

def client(host,nickname,ipv4,port,match,rounds,categories,size):
    if ipv4 == True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    
    s.connect((host,int(port)))
    if  not match:
            send_pickle_msg(s,[nickname,rounds,size,categories])
    else:
            send_pickle_msg(s,(nickname,match))    

    while True:
        msg_in = recv_msg(s)
        print(msg_in)
        # print(f"PRINT>>>>{msg_in} -- ({'Ingres' in msg_in})")
        
        if 'Ingres' in msg_in:
            msg_out = input('> ')
            send_msg(s,msg_out)
            if msg_out == 'exit':
                break
        elif msg_in[-1] == "*":
            msg_out == 'ack'
            send_msg(s,msg_out)
            
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

    # data = b'' ; packet = b''
    # while (len(packet) == 1024 or packet == b''):
    #     packet = s.recv(1024)
    #     print(f"recibi>>> {packet}")
    #     print(f"len>>> {len(packet)}")
    #     data += packet
    # return pickle.loads(data)
    
    
if __name__ == '__main__':
    client()