import socket , click , multiprocessing , pickle , os , sys , mmap

class Server:
    
    def __init__(self,host,port,backlog):
        self.host = host
        self.port = port
        self.backlog = backlog
        # self.memoria = mmap.mmap(-1,100)
        # self.q = multiprocessing.Queue()
        self.conections = {}
        self.set_socket()
        self.serve()
        
    def set_socket(self):
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        self.sock.bind((self.host, self.port))
        self.sock.listen(self.backlog)
        print(f"Server listening on {self.host}:{self.port}")
        
    def serve(self):
        
        while True:
            client, address = self.sock.accept()
            print(f"Accepted connection from {address[0]}:{address[1]}")
            proc = multiprocessing.Process(target=self.handle,args=(client,))
            proc.start()
        
            
            #usar multiprocessing para aceptar conexiones en paralelo 
            #recibir los parametros del cliente y tomar una decision
            #   segun los parametros que pase el cliente debe crear_partida()
            #   o Asignar_jugador() a una partida ya creada
        

    def handle(self,client):
        # self.q.put(client)
        # print(f"MEMORIA: {self.memoria}")
        data = b'' + client.recv(4096)
        pet = pickle.loads(data)
        print(f"soy el nuevo proceso :D, mi PID es:{os.getpid()}")
        while True:
            client.sendall(pickle.dumps('Mensaje de prueba, mandame algo'))
            resp = pickle.loads(b'' + client.recv(4096))
            print(f"Me respondieron: {resp} :D")
            if resp == 'bye':
                break
        client.close()
        sys.exit()

@click.command()
@click.option('--host', '-h', default='', help='')
@click.option('--port', '-p', default=8000, type=int, help='')
@click.option('--backlog', '-l', default=5, type=int, help='')

def clic(host,port,backlog):
    servidor = Server(host,port,backlog)
    



def crear_partida():
    #instanciar partida
    while True: #esperar a que se llene de jugadores
        break
    pass
    
def asignar_jugador(): #ver si conviene que este aca, o que sea un metodo de la clase TF
    pass



if __name__ == '__main__':
    clic()
