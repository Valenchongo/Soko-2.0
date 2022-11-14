import soko
import gamelib

ANCHO_VENTANA = 600
ALTO_VENTANA = 600

def guardar_niveles_y_teclas (ruta_archivo_niveles,ruta_archivo_teclas):
    try:
        with open(ruta_archivo_niveles) as archivo:
            linea = archivo.readline()
            linea = linea.rstrip("\n")
            niveles=[]
            contador = 0
            while linea != "":
                if linea[0] == "L":
                    nivel = []
                    nivel.append(contador)
                    while linea != "":
                        linea = archivo.readline()
                        linea = linea.rstrip("\n")
                        if linea != "" :
                            if linea[0]!= "#" and linea[0]!=" ":
                                linea = archivo.readline()
                                linea = linea.rstrip("\n")                    
                            nivel.append(linea)
                    contador+=1
                    niveles.append(nivel)
                    linea = archivo.readline()
                    linea = linea.rstrip("\n")
    except:
        raise ValueError("No se encontro el archivo de niveles")

    try:
        with open(ruta_archivo_teclas) as archivo:
            linea = archivo.readline()
            linea = linea.rstrip("\n")
            diccionario_teclas = {}
            while linea != "": 
                lista = linea.split("=")
                if diccionario_teclas.get(lista[1].strip(),"?") == "?":
                    diccionario_teclas.update({lista[1].strip():[lista[0].rstrip()]})
                else:
                    claves = diccionario_teclas.get(lista[1].strip()) 
                    claves.append(lista[0].rstrip())
                    diccionario_teclas.update({lista[1].strip():claves})
                linea = archivo.readline()
    except:
        raise ValueError("No se encontro el archivo de teclas")

        
    return niveles,diccionario_teclas

def llenar_espacios_grilla(nivel):
    """esta funcion se encarga de llenar los espacios vacios que tiene la grilla"""
    linea_con_mas_elementos = 0
    for i in range (0,len(nivel)):
        if len(nivel[i]) > linea_con_mas_elementos:
                linea_con_mas_elementos = len(nivel[i])
    for i in range (0,len(nivel)):
        diferencia_de_elementos = (linea_con_mas_elementos - len(nivel[i]))
        espacios_vacios = diferencia_de_elementos*" "
        nivel[i] = nivel[i]+espacios_vacios 

    return nivel        

def cargar_nivel(nivel):
    """Esta funcion permite cargar cada nivel del juego"""
    niveles = guardar_niveles_y_teclas("niveles.txt","teclas.txt")[0]
    if nivel == 155:
        print("Pasaste todos los niveles!")
        raise SystemExit    
    nivel_cargado = niveles[nivel]
    nivel_cargado.pop(0)
    nivel_cargado = llenar_espacios_grilla(nivel_cargado)
    nivel_cargado = soko.crear_grilla(nivel_cargado)
    siguiente_lvl = nivel+1
    return nivel_cargado,siguiente_lvl                

def mostrar_siguiente_nivel(nivel):
    """Funcion creada para cargar y dibujar en la pantalla un nuevo nivel """
    juego = cargar_nivel(nivel)[0]
    mostrar_juego_actualizado(juego,nivel)

def mostrar_juego_actualizado(juego,nivel):
    """Funcion que permite actualizar el dibujo del juego en la pantalla"""
    columnas,filas = soko.dimensiones(juego)
    ancho_caja = 64
    ANCHO_VENTANA = columnas*ancho_caja-6
    ALTO_VENTANA = filas*ancho_caja+29
    gamelib.resize(ANCHO_VENTANA,ALTO_VENTANA)
    gamelib.draw_text( f"Nivel : {nivel+1}",ANCHO_VENTANA/2,30)   
    
    pos_y=40
    for i in range (0,filas):     
        pos_x=0
        for c in range (0, columnas):
            gamelib.draw_image("img/ground.gif",pos_x,pos_y)               
            if soko.hay_pared(juego,c,i):
                gamelib.draw_image("img/wall.gif",pos_x,pos_y)
            if soko.hay_caja(juego,c,i):
                gamelib.draw_image("img/box.gif",pos_x,pos_y)
            if soko.hay_jugador(juego,c,i):
                gamelib.draw_image("img/player.gif",pos_x,pos_y)
            if soko.hay_objetivo(juego,c,i):
                gamelib.draw_image("img/goal.gif",pos_x,pos_y) 

            pos_x =(c*ancho_caja)+60

        pos_y = (i*ancho_caja)+100   

def juego_acualizar(juego,tecla,nivel):
    """funcion que permite actualizar el juego dependiendo de la tecla que se use"""
    diccionario_teclas = guardar_niveles_y_teclas("niveles.txt","teclas.txt")[1]
    comando_correcto = False
    juego_ganado = False
    reiniciar = False
    salir = False
    nueva_grilla = []
    siguiente_nivel = ""
    teclas_y_valores = list(diccionario_teclas.items())
    for i in range (0,len(teclas_y_valores)):
        if tecla in teclas_y_valores[i][1]:
            direccion = teclas_y_valores[i][0]
            comando_correcto = True
            break

    if comando_correcto:    
        if direccion == "NORTE":
            direccion = (0,-1)
        elif direccion == "OESTE":
            direccion = (-1,0)                
        elif direccion == "SUR":
            direccion = (0,1)
        elif direccion == "ESTE":
            direccion = (1,0)
        elif direccion == "REINICIAR":
            reiniciar = True
        elif direccion == "SALIR" :
            salir = True
    else:
        return juego,nivel,juego_ganado
     
    if comando_correcto == True and salir is False and reiniciar is False:     
        nueva_grilla = soko.mover(juego,direccion)    
        gamelib.play_sound('sounds/walk.wav') 
        if soko.juego_ganado(nueva_grilla) == True:
            juego_ganado = True
            gamelib.play_sound('sounds/win.wav')
            nueva_grilla = cargar_nivel(nivel)[0]
            siguiente_nivel = cargar_nivel(nivel)[1]
        else:
            siguiente_nivel = nivel 

    if  salir:
        print("Gracias por jugar soko_2.0")
        raise SystemExit    
         
    if reiniciar :
        gamelib.play_sound('sounds/restart.wav')
        nueva_grilla = cargar_nivel(nivel)[0]
        return nueva_grilla,nivel,juego_ganado   
        
    return nueva_grilla,siguiente_nivel,juego_ganado 

def main():
    # Inicializar el estado del juego
    juego = cargar_nivel(0)[0]
    juego_ganado = False
    nivel = 0
    gamelib.resize(ANCHO_VENTANA, ALTO_VENTANA)
    while gamelib.is_alive():
        gamelib.draw_begin()
        if juego_ganado:           
            mostrar_siguiente_nivel(nivel)
        else:
            mostrar_juego_actualizado(juego,nivel)
        # Dibujar la pantalla
        gamelib.draw_end()

        ev = gamelib.wait(gamelib.EventType.KeyPress)
        if not ev:
            break

        tecla = ev.key
        # Actualizar el estado del juego, según la `tecla` presionada
        juego_ganado = juego_acualizar(juego,tecla,nivel)[2]
        nivel = juego_acualizar(juego,tecla,nivel)[1]
        juego = juego_acualizar(juego,tecla,nivel)[0]        
gamelib.init(main)
