import click , sys , socket , concurrent.futures , subprocess as sp

@click.command()
@click.option('-p',default=5000,help='Puerto del servidor')
# @click.option('-c',default='t',help='(t) Para que el servidor utilice hilos o  (p) para que utilice procesos')

class Server:
    
    def __init__(self):
        self.host = "localhost"
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=2)
        print('Iniciando server...\nEsperando a un cliente...')                               
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM,) as server:
            server.bind((host,p))
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.listen(5)
            while True:
                clientsocket = server.accept()
                executor.submit(self.handle,clientsocket)
                
                
    def handle(self):
        pass
                
if __name__ == "__main__":
    servidor = Server()