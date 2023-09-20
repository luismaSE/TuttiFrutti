import requests
import json
from bardapi import Bard, SESSION_HEADERS

# def fake_ai():
#   list = [2,1,2,0,2,1,2,2,0,0,2,1]
#   return list


def bard_query(prompt):
    token = "awhrFDMkcSrGtIx1zFUjVcMeiT70uTdEEqnY-yWv1c4LaL7DPtLsEMaoLeNfXJTQ42TNDQ."
    session = requests.Session()
    session.headers = SESSION_HEADERS
    session.cookies.set("__Secure-1PSID", token)
    session.cookies.set("__Secure-1PSIDTS", "sidts-CjIBSAxbGee6lxF9HZeLoF6KvmzHdXtvuve-RjH6cPpK93-hPvjeGrz_LoY5xAzI_lCSfBAA")
    session.cookies.set("__Secure-1PSIDCC", "APoG2W_TOFxtYgY8cyrmoMybrQnnIZG6zu4Sa2Ok8aORTZV5wMe-MZHI1n9i2DHKKGKkvwvclg")
    bard = Bard(token=token, session=session)
    resp = bard.get_answer(prompt)["content"]
    print(resp)
    list = resp.split("@")
    points = json.loads(list[1])
    print(f"Lista\n{points}")
    return points
    
    
def check_word(points):
    diccionario = json.loads(dic)
    jugadores = list(diccionario.keys())
    categorias = list(diccionario[jugadores[0]].keys())
    rondas = len(diccionario[jugadores[0]][categorias[0]])
    print("jugadores>",jugadores)
    print("cats>",categorias)
    print("rondas>",rondas)
    
    puntajes=[]
    i = 0
    for jugador in jugadores:
        for categoria in categorias:
            for ronda in range(rondas):
                
                palabra = diccionario[jugador][categoria][ronda]
                if points[i]:
                    for otros in jugadores:
                        if otros != jugador:
                            if palabra == diccionario[otros][categoria][ronda]:
                                puntajes.append(1)
                            else:
                                puntajes.append(3)
                else:
                    puntajes.append(0)
                i+= 1
    print('puntajes_simples>',puntajes)
    return puntajes
                                
                      
        
def create_prompt(diccionario):
    jugadores = list(diccionario.keys())
    categorias = list(diccionario[jugadores[0]].keys())
    rondas = len(diccionario[jugadores[0]][categorias[0]])
    print("jugadores>",jugadores)
    print("cats>",categorias)
    print("rondas>",rondas)
    
    texto = """
Coloca 1 o 0 según la pregunta sea verdadera o falsa:
(si la palabra contiene errores automaticamente pone 0)\n
"""
    
    for jugador in jugadores:
        for categoria in categorias:
            for ronda in range(rondas):
                palabra = diccionario[jugador][categoria][ronda].upper()
                texto += "La palabra "+palabra+" pertenece a la categoria "+categoria.upper()+"?\n"
    
    
    texto += """
Evalua cada afirmación una por una y luego devuelve una lista en formato python con los puntajes, respetando el orden de las preguntas.
La lista debe estar entre signos arroba (@), de la siguiente forma:
"
@
[lista de puntajes]
@ 
"
No escribas codigo, solo quiero el resultado
"""

    print(texto)     
    return texto   
        
                
                                
                                
                    





if __name__ == "__main__":
    dic = json.loads("""{"Luisma": {"verbos": ["gigante", "pintar", "negar"], "objetos": ["gaita", "piñatha", "nadar"]}, "Juan": {"verbos": ["gritar", "pintar", "nadar"], "objetos": ["gancho", "piñata", "nido"]}}""")
    prompt = create_prompt(dic)
    bard_query(prompt)
    # gpt_query(dic)








# EJEMPLO DE PROMPT FINAL
"""
Coloca 1 o 0 según la pregunta sea verdadera o falsa:
(si la palabra contiene errores automaticamente pone 0)

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

Evalua cada afirmación una por una y luego devuelve una lista en bash con los puntajes, respetando el orden de las preguntas.
La lista debe estar entre signos arroba (@), de la siguiente forma:
"
@
[lista de puntajes]
@ 
"

"""