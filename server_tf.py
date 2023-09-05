import socket , click , multiprocessing as mp , pickle , os , queue , sys , time
from tutti_frutti import TuttiFrutti
from player import Player
import ai_api


class Server:
    
    def __init__(self,host,port,backlog):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.event = mp.Event()
        manager = mp.Manager()
        self.conections = manager.dict()
        self.wait_list = manager.list()
        self.set_socket()
        self.serve()
        
    def set_socket(self):
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        self.sock.bind((self.host, self.port))
        self.sock.listen(self.backlog)
        print(f"Server escuchando en > [{self.host}]:[{self.port}]")
        
        
    def serve(self):
        pid = os.getpid()
        while True:
            pid += 1
            client, address = self.sock.accept()                                                            # El server solo acepta la conexión
            print(f"Conexión aceptada > {address[0]}:{address[1]}")            
            mp.Process(target=self.handle,args=(client,pid,),daemon=True).start()
            

    def handle(self,client,pid):
        data = b'' + client.recv(4096)                                                                      # Espera a recibir los parametros de peticion del cliente
        pet = pickle.loads(data)
        self.conections[pet[0]] = client                                                                    # Dejamos un registro de todas las conexiones que recibe el server 
        # print(f"conns>>>{self.conections}")

        if len(pet) == 2:                                                                                   # Se quiere unir a una partida
            entry = (str(pet[0])+"#"+str(pet[1]))
            self.wait_list.append(entry)                                                   # Agrega una entrada a wait_list
            self.event.set()                                                                                   # Avisa a las partidas esperando
            
            time.sleep(15)
            if entry in self.wait_list:
                self.wait_list.remove(entry)
                client.sendall(f"Tiempo de espera terminado... Revisa el codigo ingresado e intenta nuevamente\nGAME OVER".encode())
                sys.exit()
            
            
        elif len(pet) == 4:                                                                                # QUiere crear una partida nueva
            code = str(pid)        
            client.sendall(f"El código de tu partida es ({code}). Usalo para invitar a tus amigos! ".encode())
            jugadores = self.esperar_jugadores(code,pet[0],pet[2])                                             # La partida no va a empezar hasta que este llena
            party = {}                                                                                             # Diccionario para pasarle al proceso de la partida cada usuario con su propia coneccion
            q = queue.Queue()
            
            
            tf = TuttiFrutti(q,pet[1])                                                       #Recibe :
            for nick in jugadores:
                player = Player(q,nick,self.conections[nick])
                tf.add_player(nick,player)                                                                # Usamos el nick del cliente para buscar su socket en el registro de conecciones 
                party[nick] = player                               
                                                                                                                   # Para luego pasarselo al Proceso que ejecutará la partida
            
            
            tf.create_tables(pet[3])
            for player in list(party.values()):
                player.join_match(tf)
                player.start_match()
            dict = tf.play()
            # points = ai_api.bard_query(dict)        
            points = ai_api.fake_ai()
            tf.game_over(points)
        sys.exit()
            # 
            #                                                                                                   # 2 cantidad de rondas
            #                                                                                                  # 3 cantidad de categorias
                
        
        
        
    def esperar_jugadores(self,code,owner,size):                                                            # Entran solo los procesos cuyo cliente quiera crear una partida
        lista = []                              
        lista.append(owner)                             
        while len(lista) != size:                                                                              # No salen del bucle de espera hasta que se llene la partida
            self.event.wait()                                                                                      # Espera hasta que un proceso actualice la lista de espera, osea que un cliente se quiere unir a una partida
            waiting = []
            for string in self.wait_list:
                if code in string:
                    waiting.append(string)
                    self.wait_list.remove(string)

            # waiting = [string for string in self.wait_list if code in string]                                              # Revisa la lista y guarda todas las peticiones con el codigo de mi partida
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
    Server(host,port,backlog)
    
def wait_for_proc(proc):
    proc.join()


if __name__ == '__main__':
    clic()
