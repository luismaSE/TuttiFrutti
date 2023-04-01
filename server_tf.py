import socket , click , multiprocessing , pickle , os , sys , mmap , threading
from tutti_frutti import TuttiFrutti

class Server:
    
    def __init__(self,host,port,backlog):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.array = []
        self.conections = {}
        self.event = multiprocessing.Event()
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
        print(f"PID del padre; {os.getpid()}")        
        while True:
            array = multiprocessing.Array('c',[])
            client, address = self.sock.accept()
            print(f"Accepted connection from {address[0]}:{address[1]}")
            threading.Thread(target=self.handle,args=(client,array),daemon=True).start()      
            

    def handle(self,client,array):
        code = "777"
        data = b'' + client.recv(4096)
        pet = pickle.loads(data)
        self.conections[pet[0]] = client
        
        
        if len(pet) == 2: #Se quiere unir a una partida
            self.array.append((str(pet[0])+"#"+str(pet[1])))
            self.event.set()
        elif len(pet) == 4:
            jugadores = self.esperar_jugadores(code,pet[0],pet[2])
            party = {}
            for nick in jugadores:
                party[nick] = self.conections[nick]
            print(f"party>>{party}")
            tf = TuttiFrutti(party,pet[1],pet[2],pet[3])
                
        client.close()
        
        
    def esperar_jugadores(self,code,owner,size):
        lista = []
        lista.append(owner)
        while len(lista) != size:
            self.event.wait()
            waiting = [string for string in self.array if code in string]
            if len(waiting) != 0:
                for player in waiting:
                    nick , line_code = player.split('#') 
                    lista.append(nick)
            print(f"lista>>{lista}")
        return lista
  

@click.command()
@click.option('--host', '-h', default='', help='')
@click.option('--port', '-p', default=8000, type=int, help='')
@click.option('--backlog', '-l', default=5, type=int, help='')

def clic(host,port,backlog):
    servidor = Server(host,port,backlog)
    



# def crear_partida():
#     #instanciar partida
#     while True: #esperar a que se llene de jugadores
#         break
#     pass
    
# def asignar_jugador(): #ver si conviene que este aca, o que sea un metodo de la clase TF
#     pass



if __name__ == '__main__':
    clic()
