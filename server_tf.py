import socket , click , multiprocessing as mp , pickle , os , sys , mmap , threading
from tutti_frutti import TuttiFrutti

class Server:
    
    def __init__(self,host,port,backlog):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.event = mp.Event()
        manager = mp.Manager()
        self.conections = manager.dict()
        self.array = manager.list()
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
        pid = os.getpid()
        while True:
            pid += 1
            client, address = self.sock.accept()                                                            # El server solo acepta la conexión
            print(f"Accepted connection from {address[0]}:{address[1]}")            
            mp.Process(target=self.handle,args=(client,pid,),daemon=True).start()
            

    def handle(self,client,pid):
        data = b'' + client.recv(4096)                                                                      # Espera a recibir los parametros de peticion del cliente
        pet = pickle.loads(data)
        self.conections[pet[0]] = client                                                                    # Dejamos un registro de todas las conexiones que recibe el server 
        # print(f"conns>>>{self.conections}")

        if len(pet) == 2:                                                                                   # Se quiere unir a una partida
            self.array.append((str(pet[0])+"#"+str(pet[1])))                                                   # Agrega una entrada al array
            self.event.set()                                                                                   # Avisa a las partidas esperando
        elif len(pet) == 4:                                                                                # QUiere crear una partida nueva
            code = str(pid)        
            client.sendall(pickle.dumps(f"El código de tu partida es ({code}). Usalo para invitar a tus amigos! "))
            jugadores = self.esperar_jugadores(code,pet[0],pet[2])                                             # La partida no va a empezar hasta que este llena
            party = {}                                                                                             # Diccionario para pasarle al proceso de la partida cada usuario con su propia coneccion
            for nick in jugadores:                               
                party[nick] = self.conections[nick]                                                         # Usamos el nick del cliente para buscar su socket en el registro de conecciones 
            # print(f"party>>{party}")                                                                           # Para luego pasarselo al Proceso que ejecutará la partida
            tf = TuttiFrutti(party,pet[1],pet[3])                                                        #Recibe :
            # tf.play()
            # tf.main()                                                                                                  # 2 cantidad de rondas
            #                                                                                                  # 3 cantidad de categorias
                
        
        
        
    def esperar_jugadores(self,code,owner,size):                                                            # Entran solo los procesos cuyo cliente quiera crear una partida
        lista = []                              
        lista.append(owner)                             
        while len(lista) != size:                                                                              # No salen del bucle de espera hasta que se llene la partida
            self.event.wait()                                                                                      # Espera hasta que un proceso actualice la lista de espera, osea que un cliente se quiere unir a una partida
            waiting = [string for string in self.array if code in string]                                              # Revisa la lista y guarda todas las peticiones con el codigo de mi partida
            if len(waiting) != 0:                               
                for player in waiting:                              
                    nick , line_code = player.split('#')                                
                    lista.append(nick)                                                                      # Ya sabemos el codigo, asi que solo nos interesa el nombre del jugador
        return lista
  

@click.command()
@click.option('--host', '-h', default='', help='')
@click.option('--port', '-p', default=8000, type=int, help='')
@click.option('--backlog', '-l', default=5, type=int, help='')

def clic(host,port,backlog):
    servidor = Server(host,port,backlog)
    
def wait_for_proc(proc):
    proc.join()


if __name__ == '__main__':
    clic()
