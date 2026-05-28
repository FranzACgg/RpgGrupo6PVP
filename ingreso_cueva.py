import random
#Ingreso a la cueva desde el mapa de prado
posJugador = 0
simbolo_pos_jugador = ""
simbolo_salida = "O"
#Crear un mapa la mitad de grande que el original, con una camara que siga al personaje y que sea mas largo que ancho 

simbolos_entorno = {
    "simbolo_calaveras" : "💀",
    "simbolo_huesos" : "𐂯 ",
    "simbolo_rocas"  :"🗿",
    "simbolo_pico" : "⛏️",
}    
    
simbolos_del_mapa = {
    "simbolo_camino" : "▓", 
    "simbolo_pared" : "🪨"
}

def creacion_visualizacion_pantalla():
    #Se crea una pantalla modificada que muestra un tamanio mucho menor al mapa de prado acoplandoce a un tamanio rectangular mas largo que ancho


if posJugador == [12,10] and simbolo_salida == "O":
    #El jugador entra por la izquierda en medio de la cueva un paso por delante del simbolo que se crea detras
    #Medidas de referencia
    posJugador = [15,2]
    pos_simbolo_salida = [15,1]
    simbolos_dentro_cueva = [simbolo_salida,pos_simbolo_salida]
    print(simbolos_dentro_cueva)

def crearDecoraciones():
    for i in range(20):
        eleccion =  random.choice(simbolos_entorno.keys)
        ubicacion = mapa[random.randint(2,fila-2),random.randint(2,columna-2)]
        mapa(ubicacion) = eleccion

inicializar_goblins()
simbolo_cofre = "🪎"

def simbolosPrincipales():
    #Crear solo un camino el cual este por debajo del personaje p y que este entrecorado, osea sea recto hasta llegar a la otra pared
    #Crear paredes que delimiten el mapa
    #Al final del camino hay un cofre

def interaccionCofre():
    #Cuando se habra el cofre habra un sistema de elecicon osea con el random choice y elijira entre las pociones / armaduras, etc disponibles
    # Y te preguntara si quieres agregarlo al inventario si la respuesta es si se agrega al inventario