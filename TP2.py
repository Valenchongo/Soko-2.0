import soko
import gamelib

ANCHO_VENTANA = 600
ALTO_VENTANA = 600

def cargar_nivel(archivo,nivel_titulo):
    """Esta funcion permite cargar cada nivel del juego"""
    with open(archivo) as n:
        nivel = []
        linea = n.readline()
        linea = linea.rstrip("\n")
        lvl = linea
        lvl= lvl.split(" ")
        lvl = int(lvl[1])
        nivel_titulo = nivel_titulo.split(" ")
        nivel_titulo = int(nivel_titulo[1])
        siguiente_lvl = ""
        linea = n.readline()

        if linea[0] != " " and linea[0] != "#":
            linea = n.readline()  
             
        linea= linea.rstrip("\n")
        linea_con_mas_elementos = 0
        while nivel_titulo != lvl:  

            while linea != "":
                nivel.append(linea)
                linea = n.readline()
                linea = linea.rstrip("\n")

                if linea == "":
                   lvl = n.readline()
                   linea = lvl  
                   lvl= lvl.split(" ")
                   lvl = int(lvl[1])
                   break
                
        if lvl == nivel_titulo: 
            nivel = []
            cortar = False

            while linea != "":   

                while lvl != 1 and cortar == False:                  
                    lvl = linea
                    lvl = lvl.split(" ")
                    lvl = int(lvl[1])
                    linea = n.readline()
                    linea = linea.rstrip("\n")
                    cortar = True
                linea = linea.rstrip("\n")    
                nivel.append(linea)
                linea = n.readline()

                if linea != "":
                    linea= linea.rstrip("\n")
            nivel = soko.crear_grilla(nivel)

            for i in range (0,len(nivel)):
                if len(nivel[i]) > linea_con_mas_elementos:
                        linea_con_mas_elementos = len(nivel[i])
            for i in range (0,len(nivel)):
                diferencia_de_elementos = linea_con_mas_elementos - len(nivel[i])
                for c in range (0,diferencia_de_elementos):
                    nivel[i].append("X")                         
        linea = n.readline() 
        siguiente_lvl = linea
        return nivel,siguiente_lvl                

def juego_mostrar_nuevo_nivel(nivel):
    """Funcion creada para cargar y dibujar en la pantalla un nuevo nivel """
    juego = cargar_nivel("niveles.txt",nivel)[0]
    mostrar_juego_actualizado(juego,nivel)

def mostrar_juego_actualizado(juego,nivel):
    """Funcion que permite actualizar el dibujo del juego en la pantalla"""
    columnas,filas = soko.dimensiones(juego)
    ANCHO_VENTANA = columnas*64-6
    ALTO_VENTANA = filas*64+29
    gamelib.resize(ANCHO_VENTANA,ALTO_VENTANA)
    gamelib.draw_text(nivel,ANCHO_VENTANA/2,30)   
    
    pos_y=40
    for i in range (0,filas):     
        pos_x=0
        for c in range (0, columnas):
            gamelib.draw_image("img/ground.gif",pos_x,pos_y)               
            if soko.hay_pared(juego,c,i):
                gamelib.draw_image("img/wall.gif",pos_x,pos_y)
            elif soko.hay_caja(juego,c,i) and soko.hay_objetivo(juego,c,i):
                gamelib.draw_image("img/box.gif",pos_x,pos_y)
                gamelib.draw_image("img/goal.gif",pos_x,pos_y)
            elif soko.hay_caja(juego,c,i):
                gamelib.draw_image("img/box.gif",pos_x,pos_y)
            elif soko.hay_jugador(juego,c,i):
                gamelib.draw_image("img/player.gif",pos_x,pos_y)
            elif soko.hay_jugador(juego,c,i) and soko.hay_objetivo(juego,c,i):
                gamelib.draw_image("img/player.gif",pos_x,pos_y) 
                gamelib.draw_image("img/goal.gif",pos_x,pos_y)                       
            elif soko.hay_objetivo(juego,c,i):
                gamelib.draw_image("img/goal.gif",pos_x,pos_y)  
             
            pos_x =(c*64)+60
        pos_y = (i*64)+100   

def juego_acualizar(juego,tecla,nivel):
    """funcion que permite actualizar el juego dependiendo de la tecla que se use"""
    with open("teclas.txt") as f:
        comando_correcto = False
        juego_ganado = False
        nueva_grilla = []
        siguiente_nivel = ""
        linea = f.readline()
        linea = linea.rstrip("\n").split("=")
        tecla_texto = linea[0]
        direccion = list(linea[1])
        direccion.remove("(")
        direccion.remove(")") 
        while linea != [""] and direccion[0]!="R" and direccion[0]!="P":
            if direccion[2] == "-":
                direccion_x = int(direccion[0])
                direccion_y = int(direccion[2]+direccion[3])
            elif direccion[0] == "-" :
                direccion_x = int(direccion[0]+direccion[1])
                direccion_y = int(direccion[3]) 
            else:
                direccion_y = int(direccion[2])
                direccion_x = int(direccion[0])  
            direccion = []
            direccion.append(direccion_x)
            direccion.append(direccion_y)     
            direccion = tuple(direccion)
            if tecla == tecla_texto:
                    comando_correcto = True
                    nueva_grilla = soko.mover(juego,direccion)    
                    gamelib.play_sound('sounds/walk.wav') 
                    if soko.juego_ganado(nueva_grilla) == True:
                        juego_ganado = True
                        gamelib.play_sound('sounds/win.wav')
                        nueva_grilla = cargar_nivel("niveles.txt",nivel)[0]
                        siguiente_nivel = cargar_nivel("niveles.txt",nivel)[1]
                        break
                    else:
                        siguiente_nivel = nivel   
            linea = f.readline()
            if linea != [""] and direccion:
                linea = linea.rstrip("\n").split("=") 
                direccion = list(linea[1])

                if direccion[0]!="R" and direccion[0]!="P":
                    direccion.remove("(")
                    direccion.remove(")")                   
                    tecla_texto = linea[0]
    if tecla != "r" and tecla != "Escape" and comando_correcto == False:
        return juego,nivel,juego_ganado
                
    if tecla == "r":
        gamelib.play_sound('sounds/restart.wav')
        nueva_grilla = cargar_nivel("niveles.txt",nivel)[0]
        return nueva_grilla,nivel,juego_ganado            
                
    return nueva_grilla,siguiente_nivel,juego_ganado 

def main():
    # Inicializar el estado del juego
    juego = cargar_nivel("niveles.txt","Level 1")[0]
    nivel = "level 1"
    juego_ganado = False
    gamelib.resize(ANCHO_VENTANA, ALTO_VENTANA)
    while gamelib.is_alive():
        gamelib.draw_begin()
        if juego_ganado:
            juego_mostrar_nuevo_nivel(nivel)
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