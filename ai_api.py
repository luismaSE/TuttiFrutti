import requests
import openai
import json
import ast
from bardapi import Bard, SESSION_HEADERS

def fake_ai():
  list = [2,1,2,0,2,1,2,2,0,0,2,1]
  return list


def gpt_query(dict):
    
    text = dict+"""
Dado este diccionario, agrega los siguientes puntajes:
2 si la palabra pertenece a la categoría y no se repitió,
1 si la palabra pertenece a la categoría pero se repitió en la misma categoría y turno,
0 si la palabra no pertenece a la categoría,
0 si tiene errores ortográficos.

Una vez terminada la lista, modifica el diccionario, agregando los puntajes correspondientes y devolve una lista con los puntajes de cada respuesta

SOLO RESPONDE LA LISTA EN PYTHON CON FORMATO JSON Y LA LISTA ENTRE SIGNOS "#", NADA DE CODIGO, NADA DE EXPLICACIONES


EJEMPLO:
    {"jugador1": {"colores": ["Gris", "turquesa", "hugo"], "animales": ["gato", "tomate", "helefante"]}, "jugador2": {"colores": ["gris","-","halamo"], "animales": ["ganzo","tiburon", "-"]}}
    
    
    el analisis es el siguiente:
    {"jugador1": {"colores": {"Gris":1, "turquesa":2, "hugo":0},"animales": {"gato":2, "tomate":0, "helefante":0}}, "jugador2": {"colores": {"gris":1,"-":0,"halamo":0},"animales": {"ganzo":2,"tiburon":2, "-":0}}}
    
    POR LO QUE LA RESPUESTA ESPERADA DEL EJEMPLO ES:

    #
    [1,2,0,2,0,0,1,0,0,2,2,0]
    #

    FIN DE LA RESPUESTA
    """
    
    openai.api_key = KEY
    response = openai.Completion.create(model="gpt-3.5-turbo",
                                        prompt=text,
                                        max_tokens=1
                                        )
    answer = response.choices[0].text.strip()
    list = answer.split("#")
    scores = json.loads(list[1])
    print(scores)
    

















def bard_query(dict):
    session = requests.Session()
    token = "aghrFI0keluxvThUsfVYRsgikTD6kHUIfmxl4K_WS4Ng_RfqMCMP90w-uMobYAAh6jaa4g."
    session.cookies.set("__Secure-1PSID", token)
    session.cookies.set( "__Secure-1PSIDCC", "APoG2W9nKPJN7wm-fxy3UFu0B0oIYXlI35w_3ePffwpbn1HwR7b99JpEW6sxWmQwAbXfBxYf")
    session.cookies.set("__Secure-1PSIDTS", "sidts-CjIBSAxbGX4eK6sbC6yAsCS1wR0IPcIEd3rrDY3_kUXelVI0her43HnIXhV3LqJOB2Y9thAA")
    session.headers = SESSION_HEADERS

    bard = Bard(token, session=session,conversation_id="c_1f04f704a788e6e4", timeout=30)

    texto = dict+"""
NO ESCRIBAS CODIGO. SOLO RESPONDE LA LISTA EN PYTHON CON FORMATO JSON Y LA LISTA ENTRE SIGNOS "#"
Dado este diccionario, agrega los siguientes puntajes:
2 si la palabra pertenece a la categoría y no se repitió,
1 si la palabra pertenece a la categoría pero se repitió en la misma categoría y turno,
0 si la palabra no pertenece a la categoría,
0 si tiene errores ortográficos.

Agrega los puntajes correspondientes y devolve una lista con los puntajes de cada respuesta

EJEMPLO:
    Diccionario de entrada:
    {"jugador1": {"colores": ["Gris", "turquesa", "hugo"], "animales": ["gato", "tomate", "helefante"]}, "jugador2": {"colores": ["gris","-","halamo"], "animales": ["ganzo","tiburon", "-"]}}
    
    Diccionario con puntajes:
    {"jugador1": {"colores": {"Gris":1, "turquesa":2, "hugo":0},"animales": {"gato":2, "tomate":0, "helefante":0}}, "jugador2": {"colores": {"gris":1,"-":0,"halamo":0},"animales": {"ganzo":2,"tiburon":2, "-":0}}}
    
    RESPUESTA ESPERADA DEL EJEMPLO:
    
    "puntajes"
    #
    [1,2,0,2,0,0,1,0,0,2,2,0]
    #
    
    FIN DE LA RESPUESTA
    """
    resp = bard.get_answer(texto)["content"]
    print(resp)
    list = resp.split("#")
    points = json.loads(list[1])
    # cats = json.loads(list[3])
    # words = json.loads(list[4])
    # points = json.loads(list[5])
    print(f"\n{points}")
    return points
    
    
    
def calcular_puntos(dic):
    diccionario = json.loads(dic)
    jugadores = list(diccionario.keys())
    categorias = list(diccionario[jugadores[0]].keys())
    rondas = len(diccionario[jugadores[0]][categorias[0]])
    print("jugadores>",jugadores)
    print("cats>",categorias)
    print("rondas>",rondas)
    
    puntajes=[]
    
    for jugador in jugadores:
        for categoria in categorias:
            for ronda in range(rondas):
                
                palabra = diccionario[jugador][categoria][ronda]
                if revisar_palabra(categoria,palabra):
                    for otros in jugadores:
                        if otros != jugador:
                            if palabra == diccionario[otros][categoria][ronda]:
                                puntajes.append(1)
                            else:
                                puntajes.append(2)
                else:
                    puntajes.append(0)
                                
                                
                    
    

def revisar_palabra(categoria,palabra):
    respuesta = False
    #LA IA debe revisar si "palabra pertenece a categoria"
    #Si es verdad Devuelve respuesta=True, 
    #caso contrario devuelve respuesta=False
    return respuesta
    
        
def calcular_puntos(dic):
    diccionario = json.loads(dic)
    jugadores = list(diccionario.keys())
    categorias = list(diccionario[jugadores[0]].keys())
    rondas = len(diccionario[jugadores[0]][categorias[0]])
    print("jugadores>",jugadores)
    print("cats>",categorias)
    print("rondas>",rondas)
    
    puntajes=[]
    texto = ""
    
    for jugador in jugadores:
        for categoria in categorias:
            for ronda in range(rondas):
                palabra = diccionario[jugador][categoria][ronda].upper()
                texto += "La palabra "+palabra+" pertenece a la categoria "+categoria.upper()+"?\n"
    print(texto)        
        
                
                                
                                
                    
    

def revisar_palabra(categoria,palabra):
    respuesta = False
    #LA IA debe revisar si "palabra pertenece a categoria"
    #Si es verdad Devuelve respuesta=True, 
    #caso contrario devuelve respuesta=False
    return respuesta

if __name__ == "__main__":
    dic = """{"Luisma": {"verbos": ["gigante", "pintar", "negar"], "objetos": ["gaita", "piñatha", "nadar"]}, "Juan": {"verbos": ["gritar", "pintar", "nadar"], "objetos": ["gancho", "piñata", "nido"]}}"""
    # bard_query(dic)
    # gpt_query(dic)
    calcular_puntos(dic)







































"""
Dado el siguiente diccionario, agrega los siguientes puntajes:
2 si la palabra pertenece a la categoría y no se repitió,
1 si la palabra pertenece a la categoría pero se repitió en la misma categoría y turno,
0 si la palabra no pertenece a la categoría,
0 si tiene errores ortográficos.
SOLO RESPONDE EL DICCIONARIO MODIFICADO EN FORMATO JSON, NADA DE CODIGO, NADA DE EXPLICACIONES

Diccionario:
{"Luisma": {"aves": ["zorro", "golondrina", "ardilla"], "colores": ["zian", "gris", "amarillo"]}, "Juan": {"aves": ["ZORRO", "gato", "aguila"], "colores": ["zrojo", "gris", "anaranjado"]}}

EJEMPLO:
    {"jugador1": {"colores": ["Gris", "turquesa", "hugo"], "animales": ["gato", "tomate", "helefante"]}, "jugador2": {"colores": ["gris","-","halamo"], "animales": ["ganzo","tiburon", "-"]}}
    
    RESPUESTA ESPERADA DEL EJEMPLO:
    #
    {"jugador1": {"colores": {"Gris":1, "turquesa":2, "hugo":0},"animales": {"gato":2, "tomate":0, "helefante":0}}, "jugador2": {"colores": {"gris":1,"-":0,"halamo":0},"animales": {"ganzo":2,"tiburon":2, "-":0}}}
    #

"""









"""
Diccionario:
{"Luisma": {"aves": ["zorro", "golondrina", "ardilla"], "colores": ["zian", "gris", "amarillo"]}, "Juan": {"aves": ["ZORRO", "gato", "aguila"], "colores": ["zrojo", "gris", "anaranjado"]}}


Dado este diccionario, agrega los siguientes puntajes:
2 si la palabra pertenece a la categoría y no se repitió,
1 si la palabra pertenece a la categoría pero se repitió en la misma categoría y turno,
0 si la palabra no pertenece a la categoría,
0 si tiene errores ortográficos.

Una vez terminada la lista, modifica el diccionario, agregando los puntajes correspondientes y separa los datos en orden en 4 listas: jugadores, categorias, respuestas, puntajes

SOLO RESPONDE EL DICCIONARIO MODIFICADO ESCRITO EN BASH, CON FORMATO JSON ENTRE SIGNOS "#", NADA DE CODIGO, NADA DE EXPLICACIONES


EJEMPLO:
    {"jugador1": {"colores": ["Gris", "turquesa", "hugo"], "animales": ["gato", "tomate", "helefante"]}, "jugador2": {"colores": ["gris","-","halamo"], "animales": ["ganzo","tiburon", "-"]}}
    
    RESPUESTA ESPERADA DEL EJEMPLO:
    
    #
    {"jugador1": {"colores": {"Gris":1, "turquesa":2, "hugo":0},"animales": {"gato":2, "tomate":0, "helefante":0}}, "jugador2": {"colores": {"gris":1,"-":0,"halamo":0},"animales": {"ganzo":2,"tiburon":2, "-":0}}}
    #
    jugadores = ["jugador1","jugador2"]
    #
    categorias = ["colores","animales"]
    #
    palabras = ["Gris","turquesa","hugo","gato","tomate","helefante","gris","-","halamo","ganzo","tiburon","-"]
    #
    puntajes =[1,2,0,2,0,0,1,0,0,2,2,0]
    #
    
""" 












"""
dic = "{"Luisma": {"verbos": ["gigante", "pintar", "negar"], "objetos": ["gaita", "piñatha", "nadar"]}, "Juan": {"verbos": ["gritar", "pintar", "nadar"], "objetos": ["gancho", "piñata", "nido"]}}"
NO ESCRIBAS CODIGO. SOLO RESPONDE LA LISTA EN PYTHON CON FORMATO JSON Y LA LISTA ENTRE SIGNOS "#"
Dado este diccionario, agrega los siguientes puntajes:
2 si la palabra pertenece a la categoría y no se repitió,
1 si la palabra pertenece a la categoría pero se repitió en la misma categoría y turno,
0 si la palabra no pertenece a la categoría,
0 si tiene errores ortográficos.

Agrega los puntajes correspondientes y devolve una lista con los puntajes de cada respuesta

EJEMPLO:
    Diccionario de entrada:
    {"jugador1": {"colores": ["Gris", "turquesa", "hugo"], "animales": ["gato", "tomate", "helefante"]}, "jugador2": {"colores": ["gris","-","halamo"], "animales": ["ganzo","tiburon", "-"]}}
    
    Diccionario con puntajes:
    {"jugador1": {"colores": {"Gris":1, "turquesa":2, "hugo":0},"animales": {"gato":2, "tomate":0, "helefante":0}}, "jugador2": {"colores": {"gris":1,"-":0,"halamo":0},"animales": {"ganzo":2,"tiburon":2, "-":0}}}
    
    RESPUESTA ESPERADA DEL EJEMPLO:
    
    "puntajes"
    #
    [1,2,0,2,0,0,1,0,0,2,2,0]
    #
    
    FIN DE LA RESPUESTA
"""






# "Procesa el siguiente diccionario de respuestas de los participantes de una partida de Tutti Frutti:"+ dict+"""
# Debes seguir las siguientes reglas para asignar puntajes a cada palabra en la lista de respuestas:

#     Asigna un puntaje de 2 si la palabra pertenece a la categoría y no se repitió en la misma categoría y turno.
#     Asigna un puntaje de 1 si la palabra pertenece a la categoría pero se repitió en la misma categoría y turno.
#     Asigna un puntaje de 0 si la palabra no pertenece a la categoría.
#     Asigna un puntaje de 0 si la palabra tiene errores ortográficos.

# Devuelve una lista de números que representen los puntajes de cada palabra en el mismo orden en que aparecen en el diccionario de respuestas. La lista resultante debe cumplir con las reglas mencionadas anteriormente
# """





"""
Procesa el siguiente diccionario de respuestas de los participantes de una partida de Tutti Frutti:
{"Luisma": {"bebida": ["onda", "esspreso", "sprite"], "comida": ["osobuco", "ensalada", "sandia"]}, "Juan": {"bebida": ["ostia", "eeeee", "seven up"], "comida": ["ozobuco", "espinaca", "sandia"]}}

Debes seguir las siguientes reglas para asignar puntajes a cada palabra en la lista de respuestas:

    Asigna un puntaje de 2 si la palabra pertenece a la categoría y no se repitió en la misma categoría y turno.
    Asigna un puntaje de 1 si la palabra pertenece a la categoría pero se repitió en la misma categoría y turno.
    Asigna un puntaje de 0 si la palabra no pertenece a la categoría.
    Asigna un puntaje de 0 si la palabra tiene errores ortográficos.

No quiero que escribas el codigo que haga esta tarea
Solo devuelve el diccionario modificado con los puntajes y la lista números que representen los puntajes de cada palabra en el mismo orden en que aparecen en el diccionario de respuestas.
SEPARADOS POR SIGNOS NUMERAL (#)
La lista resultante debe cumplir con las reglas mencionadas anteriormente.

EJEMPLO:
ENTRADA:
"{"Jugador1": {"verbos": ["gigante", "pintar", "negar"], "objetos": ["gaita", "piñatha", "nadar"]}, "Jugador2": {"verbos": ["gritar", "pintar", "nadar"], "objetos": ["gancho", "piñata", "nido"]}}"

SALIDA: 
"
#
"{"Jugador1: {"verbos": {"gigante":0, "pintar":1, "negar":2}, "objetos": {"gaita":2, "piñatha":0, "nadar":0}}, "Jugador2": {"verbos": {"gritar":2, "pintar":1, "nadar":2}, "objetos": {"gancho":2, "piñata":2, "nido":2]}}"
#
[0,1,2,2,0,0,2,1,2,2,2,2]
#
"
"""




"""
Tengo un programa para jugar TuttiFrutti en python, pero no puedo verificar si las respuestas ingresadas pertenecen a la categoria que corresponde. 
Necesito que vos cumplas esa funcion.
Sigue la ejeccuión de este codigo y realiza la tarea que le correspondería a la función revisar_palabra()
dic = {"Luisma": {"bebida": ["onda", "esspreso", "sprite"], "comida": ["osobuco", "ensalada", "sandia"]}, "Juan": {"bebida": ["ostia", "eeeee", "seven up"], "comida": ["ozobuco", "espinaca", "sandia"]}}


def calcular_puntos(dic):
    diccionario = json.loads(dic)
    jugadores = list(diccionario.keys())
    categorias = list(diccionario[jugadores[0]].keys())
    rondas = len(diccionario[jugadores[0]][categorias[0]])
    print("jugadores>",jugadores)
    print("cats>",categorias)
    print("rondas>",rondas)
    
    puntajes=[]
    
    for jugador in jugadores:
        for categoria in categorias:
            for ronda in range(rondas):
                
                palabra = diccionario[jugador][categoria][ronda].lower()
                if revisar_palabra(categoria,palabra):
                    for otros in jugadores:
                        if otros != jugador:
                            if palabra == diccionario[otros][categoria][ronda].lower():
                                puntajes.append(1)
                            else:
                                puntajes.append(2)
                else:
                    puntajes.append(0)
    return puntajes
                                
                                
                    
    

def revisar_palabra(categoria,palabra):
    respuesta = False
    #LA IA debe revisar si "palabra pertenece a categoria"
    #Si es verdad Devuelve respuesta=True, 
    #caso contrario devuelve respuesta=False
    return respuesta
    
    
mostra el output del codigo
"""


"""
Coloca 1 o 0 según la pregunta sea verdadera o falsa:

La palabra GIGANTE pertenece a la categoria VERBOS?
La palabra PINTAR pertenece a la categoria VERBOS?
La palabra NEGAR pertenece a la categoria VERBOS?
La palabra GAITA pertenece a la categoria OBJETOS?
La palabra PIÑATHA pertenece a la categoria OBJETOS?
La palabra NADAR pertenece a la categoria OBJETOS?
La palabra GRITAR pertenece a la categoria VERBOS?
La palabra PINTAR pertenece a la categoria VERBOS?
La palabra NADAR pertenece a la categoria VERBOS?
La palabra GANCHO pertenece a la categoria OBJETOS?
La palabra PIÑATA pertenece a la categoria OBJETOS?
La palabra NIDO pertenece a la categoria OBJETOS?

Devuelve una lista con los puntajes, respetando el orden de las preguntas
"""