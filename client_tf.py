#!/usr/bin/python3
import socket, sys
import click

@click.command()
@click.option('-h','host',default="localhost",help='')
@click.option('-p','--port',default=5000,help="puerto del server donde a conectar")
@click.option('-m','--match',default=None,help="Codigo de la partida a la que me quiero unir")
@click.option('-r','--rounds',default=3,help="Cantidad de las rondas de la partida")
@click.option('-c','--categories',default=3,help="Cantidad de categorias que tendrá la partida")
@click.option('-s','--size',default=2,help="Cantidad de jugadores")

def client(h,p,m,r,c,s):
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.connect((h,int(p)))

    while True:
        msg1 = input('> ')
        s.send(msg1.encode('ascii'))
        if msg1 == 'exit':
            break
        msg2 = s.recv(1024).decode('ascii')
        print(msg2)
    s.close()
    sys.exit()
    
if __name__ == '__main__':
    client()