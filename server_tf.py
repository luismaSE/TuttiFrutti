import socket , click , multiprocessing as mp , pickle , os , queue , sys , time
from tutti_frutti import TuttiFrutti
from player import Player
import ai_api
import json
import socketserver , threading


# lista de dependencias a instalar para ejecutar el server
# click
# request
# bardapi 


class Server:
    
    def __init__(self,port,backlog):
        # self.host = host
        self.port = port
        self.backlog = backlog
        self.event = mp.Event()
        manager = mp.Manager()
        self.conections = manager.dict()
        self.matches = manager.dict()
        self.wait_list = manager.list()
        self.set_socket()
        
    def set_socket(self):
        # HOST = None
        for res in socket.getaddrinfo(None, self.port, socket.AF_UNSPEC, socket.SOCK_STREAM):
            print("RES> ",res)
            family, socktype, proto, canonname, sockaddr = res
            # print("family",family)
            # print("tipo",socktype)
            # print("proto",proto)
            # print("canon",canonname)
            # print("dir",sockaddr)
            threading.Thread(target=self.server, args=(family,sockaddr),daemon=False).start()
    
    
    def server(self, family,sockaddr):
        self.sock = socket.socket(family, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((sockaddr[0],sockaddr[1]))
        self.sock.listen(self.backlog)
        print(f"Server escuchando en {sockaddr[0]} > {sockaddr[1]}")
        self.serve()

        # while True:
        #     client, address = self.sock.accept()
        #     print(f"Conexión desde {sockaddr[0]} > {address}")
            
            
        
        # direcciones = []
        # direcciones.append(socket.getaddrinfo(self.host,self.port,socket.AF_INET,1)[0])
        # direcciones.append(socket.getaddrinfo(self.host,self.port,socket.AF_INET6,1)[0])
        # print(direcciones)
        # threading.Thread(target=self.s_ipv4,args=(direcciones[0][4][0],self.port),daemon=False).start()

    # def s_ipv4(self,host,inet,port):
    #     self.sock4 = socket.socket(inet, socket.SOCK_STREAM)
    #     self.sock4.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #     self.sock4.bind((host, port))
    #     self.sock4.listen(self.backlog)
    #     print(f"Server escuchando en > [{host}]:[{port}]")
    #     self.serve_ipv4()
    
    # def s_ipv6(self,host,port):        
    #     self.sock6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    #     self.sock6.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #     self.sock6.bind((host, port))
    #     self.sock6.listen(self.backlog)
    #     print(f"Server escuchando en IPv6 > [{host}]:[{port}]")
    #     self.serve_ipv6()
        
    def serve(self,):
        pid = os.getpid()
        try:
            while True:
                pid += 1
                client, address = self.sock.accept()                                                            # El server solo acepta la conexión
                print(f"Conexión aceptada > {address[0]}:{address[1]}")            
                mp.Process(target=self.handle,args=(client,pid,),daemon=True).start()
        except KeyboardInterrupt:
            print("Servidor apagado.")
        
        except Exception as e:
            print(f"Error: {e}")
            
    # def serve_ipv6(self):
    #     pid = os.getpid()
    #     try:
    #         while True:
    #             pid += 1
    #             client, address = self.sock6.accept()                                                            # El server solo acepta la conexión
    #             print(f"Conexión IPv6 aceptada > {address[0]}:{address[1]}")            
    #             mp.Process(target=self.handle,args=(client,pid,),daemon=True).start()
    #     except KeyboardInterrupt:
    #         print("Servidor apagado.")
        
    #     except Exception as e:
    #         print(f"Error: {e}")
    
    
        
    

    def handle(self,client,pid):
        nick = get_msg(client)
        self.conections[nick] = client                                                                    # Dejamos un registro de todas las conexiones que recibe el server 
        client.sendall(f"Bienvenido {nick}, vamos a jugar TuttiFrutti!\nIngresa (1) si quieres crear una partida nueva\nIngresa (2) si quieres ver la lista de partidas a las que puedes unirte\n".encode())
        op = int(client.recv(1024).decode())
        while op != 1 and op != 2:
            client.sendall("Opción invalida, intentalo nuevamente".encode())
            op = int(client.recv(1024).decode())
            
            
        if op == 1:                                                                                # QUiere crear una partida nueva
            code = str(pid)        
            size,cats,rounds = self.build_match(client)
            self.matches[code] = nick
            
            jugadores = self.esperar_jugadores(code,nick,size)                                             # La partida no va a empezar hasta que este llena
            party = {}                                                                                             # Diccionario para pasarle al proceso de la partida cada usuario con su propia coneccion
            q = queue.Queue()
            
            tf = TuttiFrutti(q,rounds)                                                       #Recibe :
            for nick in jugadores:
                player = Player(q,nick,self.conections[nick])
                tf.add_player(nick,player)                                                                # Usamos el nick del cliente para buscar su socket en el registro de conecciones 
                party[nick] = player                               
                                                                                                                   # Para luego pasarselo al Proceso que ejecutará la partida
            tf.create_tables(cats)
            for player in list(party.values()):
                player.join_match(tf)
                player.start_match()
            dict = tf.play()
            prompt = ai_api.create_prompt(dict)
            points = ai_api.bard_query(prompt)      
            tf.game_over(points)
            sys.exit()
        
            
        elif op == 2:                                                                                   # Se quiere unir a una partida
            self.show_list(client)
            code = client.recv(1024).decode()
            entry = (nick+"#"+str(code))
            self.wait_list.append(entry)                                                   # Agrega una entrada a wait_list
            self.event.set()                                                                                   # Avisa a las partidas esperando
            
            time.sleep(15)
            if entry in self.wait_list:
                self.wait_list.remove(entry)
                client.sendall(f"Tiempo de espera terminado... Revisa el codigo ingresado e intenta nuevamente\nGAME OVER".encode())
                sys.exit()
    
    def show_list(self,client):
        msg = 'Entendido! Estas son las partidas que estan disponibles, ingresa el código de la partida a la que deseas unirte\n'
        i = 1
        for key,value in list(self.matches.items()):
            msg += f'Partida {i} - Dueño: {value} - Código: {key}\n'
            i += 1
        client.sendall(msg.encode())

    
    def build_match(self,client):
        size = None; cats = None ; rounds = None
        client.sendall("Perfecto, Vamos a crear tu partida!".encode())
        while size == None:
            client.sendall("Porfavor ingresa cuantos jugadores quieres que participen (se permiten desde 2 hasta 5 jugadores)".encode())
            input = get_msg(client)
            if 2 <= int(input) <= 5:
                size = int(input)
        while cats == None:
            client.sendall("Porfavor ingresa cuantas categorias quieres que hayan (se permiten desde 2 hasta 5 categorias".encode())
            input = get_msg(client)
            if 2 <= int(input) <= 5:
                cats = int(input)
        while rounds == None:
            client.sendall("Porfavor ingresa cuantas rondas quieres que se jueguen (se permiten desde 2 hasta 5 rondas)".encode())
            input = get_msg(client)
            if 2 <= int(input) <= 5:
                rounds = int(input)
        client.sendall("Listo! Ahora esperaremos hasta que los demás jugadores se unan".encode())    
        return size,cats,rounds   
    
        
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

            if len(waiting) != 0:                               
                for player in waiting:                              
                    nick , line_code = player.split("#")                                
                    lista.append(nick)                                                                      # Ya sabemos el codigo, asi que solo nos interesa el nombre del jugador
        del self.matches[code]
        return lista
    
    

def get_msg(client):
    return client.recv(1024).decode(errors='ignore')
  

@click.command()
# @click.option("--host", "-h", default="localhost", help="Dirección IPv4 deseada para el host")
@click.option("--port", "-p", default=8000, type=int, help="")
@click.option("--backlog", "-l", default=5, type=int, help="")

def clic(port,backlog):
    Server(port,backlog)
    
def wait_for_proc(proc):
    proc.join()


if __name__ == "__main__":
    clic()
