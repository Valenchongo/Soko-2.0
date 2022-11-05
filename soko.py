PARED = "#"
CAJA_OBJETIVO = "*"
VACÍO = " "

def crear_grilla(grilla):
    '''Crea una grilla a partir de la descripción del estado inicial.'''
    f = len(grilla)
    for i in range(0,f):
        grilla [i] =list(grilla[i])   
    return grilla

def dimensiones(grilla):
    '''Devuelve una tupla con la cantidad de columnas y filas de la grilla.'''
    filas = int(len(grilla))
    columnas = int(len(grilla[0]))
    return columnas,filas

def hay_pared(grilla, c, f):
    '''Devuelve True si hay una pared en la columna y fila (c, f).'''
    return grilla[f][c] == PARED
   
def hay_objetivo(grilla, c, f):
    '''Devuelve True si hay un objetivo en la columna y fila (c, f).'''
    return grilla[f][c] == "." or grilla[f][c] =="+" or grilla[f][c] ==CAJA_OBJETIVO
    
def hay_jugador(grilla, c, f):
    '''Devuelve True si el jugador está en la columna y fila (c, f).'''
    return grilla[f][c] =="@" or grilla[f][c] =="+"
  
def hay_caja(grilla, c, f):
    '''Devuelve True si hay una caja en la columna y fila (c, f).'''
    return grilla[f][c] == "$" or grilla[f][c] ==CAJA_OBJETIVO
  
def juego_ganado(grilla):
    '''Devuelve True si el juego está ganado.'''
    c,f=dimensiones(grilla)
    for i in range(0,f):
        fila = grilla[i]
        for p in range (0,c):
            if fila[p] == "." or fila[p] =="+":
                return False        
    return True

def Movimiento(grilla, pos_x, pos_y, direccion):
    '''Función que evalúa que hay en la posición en la cual el jugador se quiere mover para controlar todas las posibilidades que hay en el juego.'''
    grilla_2 = crear_grilla(grilla[:])
    pos_x_1,pos_x_2,pos_y_1,pos_y_2 = pos_x+direccion[1],pos_x+(direccion[1])*2,pos_y+direccion[0],pos_y+(direccion[0])*2
   
    if  hay_caja(grilla_2, pos_y_1, pos_x_1) and hay_objetivo(grilla_2, pos_y_1, pos_x_1):
        if hay_caja(grilla_2, pos_y_2, pos_x_2):
            return grilla_2
        if  grilla_2[pos_x_2][pos_y_2] == VACÍO or hay_objetivo(grilla_2, pos_y_2, pos_x_2):
            
            if hay_objetivo(grilla_2, pos_y, pos_x)  == False:    
                grilla_2[pos_x][pos_y] = VACÍO 
            else:grilla_2[pos_x][pos_y] = "." 
            grilla_2[pos_x_1][pos_y_1]  = "+" 
            if hay_objetivo(grilla_2, pos_y_2, pos_x_2) and not hay_caja(grilla_2, pos_y_2, pos_x_2):
             grilla_2[pos_x_2][pos_y_2]  = "*"
            else:
                grilla_2[pos_x_2][pos_y_2]  = "$"
            return grilla_2

        elif  grilla_2[pos_x_2][pos_y_2] == VACÍO:    
            grilla_2[pos_x_2][pos_y_2] = "$"               
            return grilla_2            

        elif  hay_objetivo(grilla_2, pos_y_2, pos_x_2): 
            grilla_2[pos_x_2][pos_y_2] = CAJA_OBJETIVO            
            return grilla_2    
            
        else:
            return grilla_2  

    elif hay_caja(grilla_2, pos_y_1, pos_x_1):          
        
        if hay_objetivo(grilla_2, pos_y_2, pos_x_2) and not hay_caja(grilla_2, pos_y_2, pos_x_2) or grilla_2[pos_x_2][pos_y_2] == VACÍO:
            if hay_objetivo(grilla_2, pos_y, pos_x)  == False:  
                grilla_2[pos_x][pos_y] = VACÍO
            else: grilla_2[pos_x][pos_y] = "." 
            grilla_2[pos_x_1][pos_y_1] = "@" 
        
        if hay_objetivo(grilla_2, pos_y_2, pos_x_2) and not hay_caja(grilla_2, pos_y_2, pos_x_2):
            grilla_2[pos_x_2][pos_y_2] = CAJA_OBJETIVO                                  
            return grilla_2
                                       
        elif grilla_2[pos_x_2][pos_y_2] == VACÍO: 
            grilla_2[pos_x_2][pos_y_2] = "$"                        
            return grilla_2
        else :
            return grilla_2   
            
    elif hay_objetivo(grilla_2, pos_y_1, pos_x_1):
        if hay_objetivo(grilla_2, pos_y, pos_x)  == False:
            grilla_2[pos_x][pos_y] = VACÍO 
        else:grilla_2[pos_x][pos_y] = "."  
        grilla_2[pos_x_1][pos_y_1] = "+"           
        return grilla_2
                    
    elif grilla_2[pos_x_1][pos_y_1] == VACÍO:
        if hay_objetivo(grilla_2, pos_y, pos_x) == False: 
            grilla_2[pos_x][pos_y] = VACÍO  
        else:
            grilla_2[pos_x][pos_y] = "."
        grilla_2[pos_x_1][pos_y_1] = "@"
        return grilla_2
    else:
        return grilla_2         
    
def mover(grilla, direccion):
    '''Mueve el jugador en la dirección indicada.'''
    c,f=dimensiones(grilla)
    for i in range(0,f):
        for p in range (0,c):
            if grilla[i][p] == "@" or grilla[i][p] == "+" :               
                pos_x, pos_y = i,p
                break
    nueva_grilla = Movimiento(grilla , pos_x , pos_y , direccion)
    return nueva_grilla
                      