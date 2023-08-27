import requests
import json
import ast
from bardapi import Bard, SESSION_HEADERS

def fake_ai():
  list = [2,2,2,2,2,2,2,2,2,2,2,2]
  return list

def api_query(dict):
    
    resp = """
```python
#
{"Luisma": {"aves": {"zorro": 0, "golondrina": 2, "ardilla": 2}, "colores": {"zian": 0, "gris": 2, "amarillo": 2}}, "Juan": {"aves": {"ZORRO": 0, "gato": 1, "aguila": 2}, "colores": {"zrojo": 0, "gris": 2, "anaranjado": 2}}}
#
["Luisma","Juan"]
#
["aves","colores"]
#
["zorro","golondrina","ardilla","zian","gris","amarillo","ZORRO","gato","aguila","zrojo","gris","anaranjado"]
#
[0,2,2,0,2,2,0,1,2,2,2,0]
#
```

Para obtener este resultado, primero creé una fun"""

    
#     session = requests.Session()
#     token = "aQhrFPxh0Aa_5Uc0WnBHpc0nhAHC-HGdW238wppzk_83IiE4BYNy5ft1xW_jAx3Cxv16zA."
#     session.cookies.set("__Secure-1PSID", token)
#     session.cookies.set( "__Secure-1PSIDCC", "APoG2W9nKPJN7wm-fxy3UFu0B0oIYXlI35w_3ePffwpbn1HwR7b99JpEW6sxWmQwAbXfBxYf")
#     session.cookies.set("__Secure-1PSIDTS", "sidts-CjIBSAxbGX4eK6sbC6yAsCS1wR0IPcIEd3rrDY3_kUXelVI0her43HnIXhV3LqJOB2Y9thAA")
#     session.headers = SESSION_HEADERS

#     bard = Bard(token, session=session,conversation_id="c_1f04f704a788e6e4", timeout=30)

#     texto = dict+"""
# Dado este diccionario, agrega los siguientes puntajes:
# 2 si la palabra pertenece a la categoría y no se repitió,
# 1 si la palabra pertenece a la categoría pero se repitió en la misma categoría y turno,
# 0 si la palabra no pertenece a la categoría,
# 0 si tiene errores ortográficos.

# Una vez terminada la lista, modifica el diccionario, agregando los puntajes correspondientes y separa los datos ,respetando su orden, en 4 listas: jugadores, categorias, respuestas, puntajes

# SOLO RESPONDE EL DICCIONARIO MODIFICADO ESCRITO EN PYTHON CON FORMATO JSON Y LAS LISTAS ENTRE SIGNOS "#", NADA DE CODIGO, NADA DE EXPLICACIONES


# EJEMPLO:
#     {'jugador1': {'colores': ['Gris', 'turquesa', 'hugo'], 'animales': ['gato', 'tomate', 'helefante']}, 'jugador2': {'colores': ['gris','-','halamo'], 'animales': ['ganzo','tiburon', '-']}}
    
#     RESPUESTA ESPERADA DEL EJEMPLO:
    
#     #
#     {"jugador1": {"colores": {"Gris":1, "turquesa":2, "hugo":0},"animales": {"gato":2, "tomate":0, "helefante":0}}, "jugador2": {"colores": {"gris":1,"-":0,"halamo":0},"animales": {"ganzo":2,"tiburon":2, "-":0}}}
#     #
#     ["jugador1","jugador2"]
#     #
#     ["colores","animales"]
#     #
#     ["Gris","turquesa","hugo","gato","tomate","helefante","gris","-","halamo","ganzo","tiburon","-"]
#     #
#     [1,2,0,2,0,0,1,0,0,2,2,0]
#     #
#
#     FIN DE LA RESPUESTA
#     """
#     resp = bard.get_answer(texto)["content"]
#     print(resp)
    list = resp.split('#')
    players = json.loads(list[2])
    cats = json.loads(list[3])
    words = json.loads(list[4])
    points = json.loads(list[5])
    print(f"{players}\n{cats}\n{words}\n{points}")
    return points
    

if __name__ == "__main__":
    dic = "{'Luisma': {'aves': ['zorro', 'golondrina', 'ardilla'], 'colores': ['zian', 'gris', 'amarillo']}, 'Juan': {'aves': ['ZORRO', 'gato', 'aguila'], 'colores': ['zrojo', 'gris', 'anaranjado']}}"
    api_query(dic)





'''
Dado el siguiente diccionario, agrega los siguientes puntajes:
2 si la palabra pertenece a la categoría y no se repitió,
1 si la palabra pertenece a la categoría pero se repitió en la misma categoría y turno,
0 si la palabra no pertenece a la categoría,
0 si tiene errores ortográficos.
SOLO RESPONDE EL DICCIONARIO MODIFICADO EN FORMATO JSON, NADA DE CODIGO, NADA DE EXPLICACIONES

Diccionario:
{'Luisma': {'aves': ['zorro', 'golondrina', 'ardilla'], 'colores': ['zian', 'gris', 'amarillo']}, 'Juan': {'aves': ['ZORRO', 'gato', 'aguila'], 'colores': ['zrojo', 'gris', 'anaranjado']}}

EJEMPLO:
    {'jugador1': {'colores': ['Gris', 'turquesa', 'hugo'], 'animales': ['gato', 'tomate', 'helefante']}, 'jugador2': {'colores': ['gris','-','halamo'], 'animales': ['ganzo','tiburon', '-']}}
    
    RESPUESTA ESPERADA DEL EJEMPLO:
    #
    {"jugador1": {"colores": {"Gris":1, "turquesa":2, "hugo":0},"animales": {"gato":2, "tomate":0, "helefante":0}}, "jugador2": {"colores": {"gris":1,"-":0,"halamo":0},"animales": {"ganzo":2,"tiburon":2, "-":0}}}
    #

'''









'''
Diccionario:
{'Luisma': {'aves': ['zorro', 'golondrina', 'ardilla'], 'colores': ['zian', 'gris', 'amarillo']}, 'Juan': {'aves': ['ZORRO', 'gato', 'aguila'], 'colores': ['zrojo', 'gris', 'anaranjado']}}


Dado este diccionario, agrega los siguientes puntajes:
2 si la palabra pertenece a la categoría y no se repitió,
1 si la palabra pertenece a la categoría pero se repitió en la misma categoría y turno,
0 si la palabra no pertenece a la categoría,
0 si tiene errores ortográficos.

Una vez terminada la lista, modifica el diccionario, agregando los puntajes correspondientes y separa los datos en orden en 4 listas: jugadores, categorias, respuestas, puntajes

SOLO RESPONDE EL DICCIONARIO MODIFICADO ESCRITO EN BASH, CON FORMATO JSON ENTRE SIGNOS "#", NADA DE CODIGO, NADA DE EXPLICACIONES


EJEMPLO:
    {'jugador1': {'colores': ['Gris', 'turquesa', 'hugo'], 'animales': ['gato', 'tomate', 'helefante']}, 'jugador2': {'colores': ['gris','-','halamo'], 'animales': ['ganzo','tiburon', '-']}}
    
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
    
''' 