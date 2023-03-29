import socket , click , multiprocessing

@click.command()
@click.option('--host', '-h', default='', help='Host IP to bind server to. Default is all available interfaces.')
@click.option('--port', '-p', default=8000, type=int, help='Port to bind server to. Default is 8000.')


def server(host, port):
    backlog = 5
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
    sock.bind((host, port))
    sock.listen(backlog)
    print(f"Server listening on {host}:{port}")
    
    while True:
        client, address = sock.accept()
        print(f"Accepted connection from {address[0]}:{address[1]}")
        
        #usar multiprocessing para aceptar conexiones en paralelo
        # recibir los parametros del cliente y tomar una decision
        #   segun los parametros que pase el cliente debe crear_partida()
        #   o Asignar_jugador() a una partida ya creada
        
        client.close()


def crear_partida():
    #instanciar partida
    while True: #esperar a que se llene de jugadores
        break
    pass
    
def asignar_jugador(): #ver si conviene que este aca, o que sea un metodo de la clase TF
    pass



if __name__ == '__main__':
    server()
