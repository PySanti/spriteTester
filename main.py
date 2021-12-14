import pygame
from pygame.locals import *
import os
from os import DirEntry, system as terminal
from sys import argv
pygame.init()

def isAnimationPath(animation_path):
    """
        Retorna True en caso de que la ruta de la animacion sea un directorio y tenga unicamente archivos con extension 
        .jpg y .png
    """
    if not os.path.isdir(animation_path):
        return False
    else:
        for element in os.listdir(animation_path):
            elementPath = f"{animation_path}/{element}"
            if os.path.isfile(elementPath):
                extension = elementPath[-4:len(elementPath)]
                if not extension in [".png", ".jpg"]:
                    return False
            else:
                return False
    return True
def getAnimationSpriteNumber(sprite_name):
    start_index = None
    end_index   = None
    for letter in sprite_name:
        try:
            letter = int(letter)
            if (start_index == None):
                start_index = sprite_name.index(str(letter))
        except ValueError:
            if (start_index != None) and (end_index == None):
                end_index = sprite_name.index(str(letter))
                break

    if (start_index != None) and (end_index == None):
        end_index = len(sprite_name)

    if (start_index == None):
        print(f"Error, el archivo > {sprite_name} < no tiene un identificador de sprite ... ")
        quit(-1)

    elif (start_index != None ) and (end_index != None):
        return int(sprite_name[start_index:end_index])
def getImageReady(path, size, colorkey, has_alpha_pixels):
    image = pygame.image.load(path)
    image = pygame.transform.scale(image, size)

    if has_alpha_pixels:
        image.convert_alpha()
    else:
        image.set_colorkey(colorkey)
        image.convert()
    return image
def getAnimationSprites(animation_data):
    """
        Retorna una lista con todos los sprites de la carpeta en el
    """
    animation_path = animation_data["animation path"]
    current_littlest_number = 10
    spriteList = os.listdir(animation_path)
    for sprite in spriteList:
        spriteNumber = getAnimationSpriteNumber(sprite)
        if  spriteNumber <= current_littlest_number:
            current_littlest_number = spriteNumber
    current_target  = current_littlest_number
    current_index   =   0
    animationList   = []
    while current_target < (len(spriteList) +1):
        if str(current_target) in spriteList[current_index]:
            imagePath = f"{animation_path}/{spriteList[current_index]}"
            image = getImageReady(imagePath, animation_data["size"], animation_data["colorkey"], animation_data["has_alpha_pixels"])
            animationList.append(image)
            current_target += 1
            current_index = 0
        else:
            current_index += 1
    return animationList
def refreshTerminalData(command_word, animation_data, input, current_advertencia, current_changing_feature, last_input, current_last_comand):
    terminal("clear")
    print(f"""   \n\n\t\tUso de comandos: {command_word} (caracteristica)   \n\t\tCaracteristicas disponibles: \n""")
    for key,value in animation_data.items():
        if key != "has_alpha_pixels":
            print(f"\t\t ~ {key:30} :    {value}")

    print("\n\n\n\n\t\t Historial de comandos :\n")
    if (len(last_input) > 0):
        for command in last_input:
            print(f"\t\t -> {command}" if last_input.index(command) == current_last_comand else f"\t\t  {command}")


    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    if current_advertencia != None:
        print(f"\t{current_advertencia}")
    if current_changing_feature != None:
        print(f"\t{current_changing_feature} : {input}")
    else:
        print(f"\t-> {input}")
def numberList(sep, tested_str, number_count):
    """
        Funcion creada para testear cadenas del formato: numero(separador)numero(separador)
        
        En caso de que "tested_str" cumpla con el formato, la funcion retornara una lista con los numeros, en caso contrario, retornara False
    """
    new_feature = tested_str.split(sep)
    if len(new_feature) != number_count:
        return False
    else:
        try:
            for i in range(0, number_count):
                new_feature[i] = int(new_feature[i])
        except:
            return False
        else:
            return new_feature
def isCommand(tested_command, command_word, animation_data):
    """
        Retorna la "feature" del comando en caso de que el comando sea valido, False en caso contrario ... 
    """
    if (command_word in tested_command) and (tested_command != command_word):
        feature = tested_command.split(command_word)[1]
        try:
            animation_data[feature]
        except KeyError:
            return False
        else:
            return feature
    else:
        return False
def moveCurrentHistorialElement(historial, current_index, direction):
    if direction == "left":
        current_index -= 1
        if current_index < 0:
            current_index = len(historial) - 1
    else:
        current_index += 1
        if current_index > (len(historial) - 1):
            current_index = 0
    return current_index
ANIMATION_DATA = {
        "animation path" : "test/megaman/shooting_running_right/",
        "size" : [130,100],
        "has_alpha_pixels" : True,
        "colorkey" : None,
        "fps" : 6,
        "background color" : (0,0,0)
}

terminal("clear")
if len(argv) != 2:
    print("\n\tError, se debe pasar por la entrada del programa la ruta de la carpeta de animacion ... \n\t\t\t\t\t\t\t\t Ex: python3 main.py ../Desktop/AnimationFolder")
    quit(-1)
else:
    if (not isAnimationPath(argv[1])) and (argv[1] != "-p"):
        print("Error, la carpeta de animacion debe tener unicamente archivos con extension '.jpg' o '.png'")
        quit(-1)
    elif argv[1] != "-p":
        ANIMATION_DATA["animation path"] = argv[1]


WINDOW_SIZE             =   [1000, 800]
WINDOW                  =   pygame.display.set_mode(WINDOW_SIZE, RESIZABLE)
EXIT                    =   False
CLOCK                   =   pygame.time.Clock()
ANIMATION_LIST          =   getAnimationSprites(ANIMATION_DATA)
CURRENT_FRAME           =   0
CURRENT_INDEX           =   0
INPUT                   =   ""
CHANGING_FEATURE        =   None
BACKSPACE_PRESSED       =   False
CURRENT_BACKSPACE_FRAME =   0
BACKSPACE_FPS           =   5
CURRENT_ADVERTENCIA     =   None
LAST_INPUT              =   []
COMMAND_WORD            =   "cambiar "
CURRENT_REUSE_COMMAND_INDEX   =   0
HISTORIAL_COMMANDS      =   {"right" : K_DOWN, "left" : K_UP, "remove" : K_DELETE} # right para aumentar el indice y left para disminuirlo

refreshTerminalData(COMMAND_WORD, ANIMATION_DATA, INPUT, CURRENT_ADVERTENCIA, CHANGING_FEATURE, LAST_INPUT, CURRENT_REUSE_COMMAND_INDEX)

while not EXIT:
    WINDOW.fill(ANIMATION_DATA["background color"])
    WINDOW.blit(ANIMATION_LIST[CURRENT_INDEX], [WINDOW_SIZE[0]//2 - ANIMATION_DATA["size"][0]//2, WINDOW_SIZE[1]//2 - ANIMATION_DATA["size"][1]//2] )

    # actualizacion de animacion
    if CURRENT_FRAME == ANIMATION_DATA["fps"]:
        CURRENT_FRAME = 0
        CURRENT_INDEX += 1
        if CURRENT_INDEX > len(ANIMATION_LIST)-1:
            CURRENT_INDEX  = 0
    else:
        CURRENT_FRAME += 1

    # administracion de eventos
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            EXIT = True
        if event.type == KEYDOWN:
            if  event.key not in [K_BACKSPACE, K_RETURN, HISTORIAL_COMMANDS["right"], HISTORIAL_COMMANDS["left"], HISTORIAL_COMMANDS["remove"]]:
                INPUT += (event.unicode)
                refreshTerminalData(COMMAND_WORD, ANIMATION_DATA, INPUT, CURRENT_ADVERTENCIA, CHANGING_FEATURE, LAST_INPUT, CURRENT_REUSE_COMMAND_INDEX)
            elif (event.key == K_BACKSPACE) and (len(INPUT) > 0):
                BACKSPACE_PRESSED = True
            elif (event.key == K_RETURN):
                if CHANGING_FEATURE == None:
                    feature = isCommand(INPUT, COMMAND_WORD, ANIMATION_DATA)
                    if feature != False:
                        CHANGING_FEATURE = feature
                    else:
                        CURRENT_ADVERTENCIA = f"Error, comando invalido. Revisar guia"
                else:
                    if   CHANGING_FEATURE == "animation path":
                        if isAnimationPath(INPUT):
                            ANIMATION_DATA["animation path"] = INPUT
                            ANIMATION_LIST = getAnimationSprites(ANIMATION_DATA)
                            CURRENT_FRAME = 0
                            CURRENT_INDEX = 0
                            CURRENT_ADVERTENCIA = "Exito !"
                        else:
                            CURRENT_ADVERTENCIA = f"Error, el animation path debe ser un directorio en el que todos los elementos sean archivos con extension '.jpg' o '.png' ..." 
                    elif CHANGING_FEATURE == "size":
                        new_size = numberList(",", INPUT, 2)
                        if new_size == False:                          
                            CURRENT_ADVERTENCIA = f"Error, el valor '{INPUT}' para la caracteristica 'size' es invalido. El formato debe ser: x,y"
                        else:
                            ANIMATION_DATA["size"]  = new_size
                            ANIMATION_LIST          = getAnimationSprites(ANIMATION_DATA)
                            CURRENT_FRAME           = 0
                            CURRENT_INDEX           = 0
                            CURRENT_ADVERTENCIA     = "Exito !"
                    elif CHANGING_FEATURE == "colorkey":
                        new_colorkey = numberList(",", INPUT, 3)
                        if new_colorkey == False:                          
                            if INPUT == "None":
                                ANIMATION_DATA["colorkey"]  = None
                                ANIMATION_DATA["has_alpha_pixels"]  = True
                                ANIMATION_LIST          = getAnimationSprites(ANIMATION_DATA)
                                CURRENT_FRAME           = 0
                                CURRENT_INDEX           = 0
                                CURRENT_ADVERTENCIA     = "Exito !"
                            else:
                                CURRENT_ADVERTENCIA = f"Error, el valor '{INPUT}' para la caracteristica 'colorkey' es invalido. El formato debe ser: x,y,z. Tambien puede usarse el valor 'None'"
                        else:
                            ANIMATION_DATA["colorkey"]  = new_colorkey
                            ANIMATION_DATA["has_alpha_pixels"]  = False
                            ANIMATION_LIST          = getAnimationSprites(ANIMATION_DATA)
                            CURRENT_FRAME           = 0
                            CURRENT_INDEX           = 0
                            CURRENT_ADVERTENCIA     = "Exito !"
                    elif CHANGING_FEATURE == "fps":
                        new_fps = None
                        try:
                            new_fps = int(INPUT)
                        except:
                            CURRENT_ADVERTENCIA = f"Error, el valor para fps '{INPUT}' es invalido. El valor debe ser numerico ..."
                        else:
                            ANIMATION_DATA["fps"] = new_fps
                            CURRENT_FRAME = 0
                            CURRENT_INDEX = 0
                            CURRENT_ADVERTENCIA     = "Exito !"
                    elif CHANGING_FEATURE == "background color":
                        new_bc = numberList(",", INPUT, 3)
                        if new_bc == False:
                            CURRENT_ADVERTENCIA = f"Error, el valor '{INPUT}' para la caracteristica 'background color' es invalido. El formato debe ser: x,y,z"
                        else:
                            ANIMATION_DATA["background color"]  = new_bc
                            CURRENT_ADVERTENCIA     = "Exito !"

                    CHANGING_FEATURE = None
                if not INPUT in LAST_INPUT:
                    LAST_INPUT.append(INPUT[:])
                INPUT = ""
                refreshTerminalData(COMMAND_WORD, ANIMATION_DATA, INPUT, CURRENT_ADVERTENCIA, CHANGING_FEATURE, LAST_INPUT, CURRENT_REUSE_COMMAND_INDEX)
            elif (event.key == HISTORIAL_COMMANDS["right"]) or (event.key == HISTORIAL_COMMANDS["left"]):
                if len(LAST_INPUT) > 0:
                    direction = "right" if event.key == HISTORIAL_COMMANDS["right"] else "left"
                    CURRENT_REUSE_COMMAND_INDEX = moveCurrentHistorialElement(LAST_INPUT, CURRENT_REUSE_COMMAND_INDEX, direction)
                    INPUT = LAST_INPUT[CURRENT_REUSE_COMMAND_INDEX][:]
                    refreshTerminalData(COMMAND_WORD, ANIMATION_DATA, INPUT, CURRENT_ADVERTENCIA, CHANGING_FEATURE, LAST_INPUT, CURRENT_REUSE_COMMAND_INDEX)
                else:
                    CURRENT_ADVERTENCIA = f"Error, la lista de comandos reutilizables esta vacia ..."
            elif (event.key == HISTORIAL_COMMANDS["remove"]):
                if len(LAST_INPUT) > 0:
                    LAST_INPUT.pop(CURRENT_REUSE_COMMAND_INDEX)
                    if CURRENT_REUSE_COMMAND_INDEX == len(LAST_INPUT):
                        CURRENT_REUSE_COMMAND_INDEX -= 1
                else:
                    CURRENT_ADVERTENCIA = "Error, no hay comandos en el historial para eliminar ... "
                if len(LAST_INPUT) > 0:
                    INPUT = LAST_INPUT[CURRENT_REUSE_COMMAND_INDEX][:]
                else:
                    INPUT = ""
                refreshTerminalData(COMMAND_WORD, ANIMATION_DATA, INPUT, CURRENT_ADVERTENCIA, CHANGING_FEATURE, LAST_INPUT, CURRENT_REUSE_COMMAND_INDEX)
        if event.type == KEYUP and event.key == K_BACKSPACE:
            BACKSPACE_PRESSED = False
        if event.type == WINDOWRESIZED:
            WINDOW_SIZE = [event.x, event.y]


    # actualizacion de informacion de backspace
    if BACKSPACE_PRESSED:
        if CURRENT_BACKSPACE_FRAME == BACKSPACE_FPS:
            CURRENT_BACKSPACE_FRAME = 0
            INPUT = INPUT[0:len(INPUT)-1]
            refreshTerminalData(COMMAND_WORD, ANIMATION_DATA, INPUT, CURRENT_ADVERTENCIA, CHANGING_FEATURE, LAST_INPUT, CURRENT_REUSE_COMMAND_INDEX)

        else:
            CURRENT_BACKSPACE_FRAME += 1
    else:
        CURRENT_BACKSPACE_FRAME = BACKSPACE_FPS




    pygame.display.update()
    CLOCK.tick(60)



pygame.quit()
