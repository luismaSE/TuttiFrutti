#!/usr/bin/python3
import socket, sys , click , pickle

@click.command()
@click.option('-h','host',default="localhost",help='')
@click.option('-n','--nickname',default='invitado',help="Ingresa tu nombre de usuario")
@click.option('-ipv4',is_flag=True, flag_value=True,help="Espicifiación para realizar la conexion mediante IPv4, si no se especifica se utilizará IPv6")
@click.option('-p','--port',default=5000,help="puerto del server donde a conectar")
@click.option('-m','--match',default= 0 ,help="Codigo de la partida a la que me quiero unir")
@click.option('-r','--rounds',default=3,help="Cantidad de las rondas de la partida")
@click.option('-c','--categories',default=3,help="Cantidad de categorias que tendrá la partida")
@click.option('-s','--size',default=2,help="Cantidad de jugadores")

def client(host,nickname,ipv4,port,match,rounds,categories,size):
    if ipv4 == True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    
    s.connect((host,int(port)))
    if  not match:
        petition = pickle.dumps([nickname,rounds,size,categories])
    else:
        petition = pickle.dumps((nickname,match))
    s.sendall(petition)
    

    while True:
        msg_in = pickle.loads(b'' + s.recv(4096))
        print(msg_in)
        msg_out = input('> ')
        s.sendall(pickle.dumps(msg_out))
        if msg_out == 'exit':
            break
    s.close()
    sys.exit()
    
if __name__ == '__main__':
    client()