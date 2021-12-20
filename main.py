from types import resolve_bases
import pygame
from pygame.locals import *
import os
from os import DirEntry, system as terminal
from sys import argv
pygame.init()

#    Cosas por hacer:
#        Quitar comandos, agregar modificacion directa
#        Revisar fugas y documentaciones post refactor
#        testear bien bien el programa (probar cada parte del programa)



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
    """
        Retorna el numero de identificacion del sprite en la animacion. Necesario para el ordenado almacenamiento de los sprites
    """
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
def getImageReady(path, size, colorkey, has_alpha_pixels, rotated):
    """
        Carga la imagen de "path" y le asigna las caracteristicas pasadas por parametro
    """
    image = pygame.image.load(path)
    image = pygame.transform.scale(image, size)

    if has_alpha_pixels:
        image.convert_alpha()
    else:
        image.set_colorkey(colorkey)
        image.convert()
    if rotated:
        image = pygame.transform.flip(image, True, False)
    return image
def getAnimationSprites(animation_data):
    """
        Retorna una lista con todos los sprites de la carpeta en el
    """
    animation_path = animation_data["animation_path"]
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
            image = getImageReady(imagePath, animation_data["size"], animation_data["colorkey"], animation_data["has_alpha_pixels"], animation_data["rotated"])
            animationList.append(image)
            current_target += 1
            current_index = 0
        else:
            current_index += 1
    return animationList
def refreshTerminalData(animation_data, input_manager):
    """
        Actualiza la informacion de la terminal, con las instrucciones, el historial y la entrada
    """
    terminal("clear")
    print("\n\t Uso de comandos: 'feature' 'value'\n")
    for key,value in animation_data.items():
        if key != "has_alpha_pixels":
            print(f"\t ~ {key:30} :    {value}")

    print("\n\n\n\n\t\t Historial de comandos :\n")
    if (len(input_manager.historial) > 0):
        for command in input_manager.historial:
            print(f"\t -> {command}" if input_manager.historial.index(command) == input_manager.current_historial_index else f"\t  {command}")


    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    if input_manager.current_advertencia != None:
        print(f"\t{input_manager.current_advertencia}")
    print(f"\t-> {input_manager.data}")
def numberList(sep, tested_str, number_count):
    """
        Funcion creada para testear cadenas del formato: numero(separador)numero(separador)...
        
        En caso de que "tested_str" cumpla con el formato, la funcion retornara una lista con los numeros, en caso contrario, retornara False
    """
    number_list = tested_str.split(sep)
    if len(number_list) != number_count:
        return False
    else:
        try:
            for i in range(0, number_count):
                number_list[i] = int(number_list[i])
        except:
            return False
        else:
            return number_list
def commandCheck(tested_command,  animation_data):
    """
        Rrevisa el comando pasado por parametro, y comprueba que este compuesto por feature + " " + value. 
        
        En cuyo caso retornara un diccionario con las claves "feature" y "value", en caso contrario retornara False
    """
    try:
        data = tested_command.split(" ")
        data = [i for i in data if i != ""]
        feature, value  = data
        animation_data[feature]
    except (KeyError, ValueError, TypeError):
        return False
    else:
        return {"feature" : feature, "value" : value}
def argvTesting(argv):
    """
        Comprueba la validez del argumento pasado por la entrada al programa
    """
    terminal("clear")
    if len(argv) != 2:
        print("\n\tError, se debe pasar por la entrada del programa la ruta de la carpeta de animacion ... \n\t\t\t\t\t\t\t\t Ex: python3 main.py ../Desktop/AnimationFolder")
        quit(-1)
    else:
        if (not isAnimationPath(argv[1])):
            if (argv[1] != "-p"):
                print("Error, la carpeta de animacion debe tener unicamente archivos con extension '.jpg' o '.png'")
                quit(-1)
        else:
            ANIMATION_DATA["animation_path"] = argv[1]

class AnimationManager:
    """
        Clase creada para la administracion de las animaciones
    """
    def __init__(self,animation_data):
        self.current_index      = 0
        self.current_frame      = 0
        self.frames_per_image   = animation_data["fps"]
        self.animation_list     =   getAnimationSprites(animation_data)
    def currentSprite(self):
        """
            Retorna el sprite actual de la animacion
        """
        return self.animation_list[self.current_index]
    def update(self):
        """
            Actualiza los valores de la animacion
        """
        if self.current_frame == self.frames_per_image:
            self.current_frame = 0
            self.current_index += 1
            if self.current_index > (len(self.animation_list) - 1) :
                self.current_index = 0
        else:
            self.current_frame += 1
    def resetData(self, animation_data):
        """
            Vuelve a solicitar la lista de sprites a la funcion "getAnimationSprites", ademas resetea los valores de la animacion
        """
        self.__init__(animation_data)
class InputManager:
    def __init__(self):
        self.data = ""
        self.remove_frame = 0
        self.remove_count_limit = 7
        self.backspace_pressed  =  False
        self.current_advertencia = None
        # pueden haber dos tipos de entrada : 
        #                                              1- "command input" 
        #                                              2- "feature value input"
        self.historial          = []
        self.current_historial_index = 0
    def add(self, letter):
        """
            Agrega la letra pasada por parametro a la entrada
        """
        self.data += letter
    def animationPathInput(self, animation_data, animation_manager, value):
        if isAnimationPath(value):
            if animation_data["animation_path"] != value:
                animation_data["animation_path"]            = value
                self.current_advertencia                    = "Exito !"
                animation_manager.resetData(animation_data)
            else:
                self.current_advertencia                 = "No hay cambios !"
        else:
            self.current_advertencia = f"Error, el animation path debe ser un directorio en el que todos los elementos sean archivos con extension '.jpg' o '.png' ..."
    def sizeInput(self, animation_data, animation_manager, value):
        new_size = numberList(",", value, 2)
        if not new_size:                          
            self.current_advertencia = f"Error, el valor '{value}' para la caracteristica 'size' es invalido. El formato debe ser: x,y"
        else:
            if new_size != animation_data["size"]:
                animation_data["size"]       = new_size
                self.current_advertencia     = "Exito !"
                animation_manager.resetData(animation_data)
            else:
                self.current_advertencia                 = "No hay cambios !"
    def rotatedInput(self, animation_data, animation_manager, value):
        if not value in ["True", "False"]:
            self.current_advertencia = "Error, el valor de 'rotated' debe ser 'True' o 'False'"
        else:
            value = True if value == "True" else False
            if value != animation_data["rotated"]:
                animation_data["rotated"] = value
                animation_manager.resetData(animation_data)
                self.current_advertencia                 = "Exito !"
            else:
                self.current_advertencia = "No hay cambios !"
    def colorkeyInput(self, animation_data, animation_manager, value):
        new_colorkey = numberList(",", value, 3)
        if not new_colorkey:                          
            if value == "None":
                if animation_data["colorkey"] != None:
                    animation_data["colorkey"]          = None
                    animation_data["has_alpha_pixels"]  = True
                    animation_manager.resetData(animation_data)
                    self.current_advertencia                 = "Exito !"
                else:
                    self.current_advertencia                 = "No hay cambios !"
            else:
                self.current_advertencia = f"Error, el valor '{value}' para la caracteristica 'colorkey' es invalido. El formato debe ser: x,y,z. Tambien puede usarse el valor 'None'"
        else:
            if new_colorkey != animation_data["colorkey"]:
                animation_data["colorkey"]               = new_colorkey
                animation_data["has_alpha_pixels"]       = False
                animation_manager.resetData(animation_data)
                self.current_advertencia                 = "Exito !"
            else:
                self.current_advertencia = "No hay cambios !"
    def fpsInput(self, animation_data, animation_manager, value):
        new_fps = None
        try:
            new_fps = int(value)
        except ValueError:
            self.current_advertencia = f"Error, el valor para fps '{value}' es invalido. El valor debe ser numerico ..."
        else:
            if new_fps != animation_data["fps"]:
                animation_data["fps"]               = new_fps
                animation_manager.current_frame     = animation_manager.current_index = 0
                animation_manager.frames_per_image  = new_fps
                self.current_advertencia     = "Exito !"
            else:
                self.current_advertencia = "No hay cambios !"
    def backgroundColorInput(self, animation_data, value):
        new_bc = numberList(",", value, 3)
        if not new_bc :
            self.current_advertencia = f"Error, el valor '{value}' para la caracteristica 'background color' es invalido. El formato debe ser: x,y,z"
        else:
            animation_data["background_color"]  = new_bc
            self.current_advertencia                 = "Exito !"
    def enter(self, animation_data, animation_manager):
        """
            Metodo creado para la administracion y modularizacion de las acciones en caso de presionar el enter
        """
        command = commandCheck(self.data, animation_data)
        if command:
            feature = command["feature"]
            value = command["value"]
            if   feature == "animation_path":
                self.animationPathInput(animation_data, animation_manager, value)
            elif feature == "size":
                self.sizeInput(animation_data, animation_manager, value)
            elif feature == "colorkey":
                self.colorkeyInput(animation_data, animation_manager, value)
            elif feature == "fps":
                self.fpsInput(animation_data, animation_manager, value)
            elif feature == "background_color":
                self.backgroundColorInput(animation_data, value)
            elif feature == "rotated":
                self.rotatedInput(animation_data, animation_manager, value)
        else:
            self.current_advertencia = f"Error, comando invalido. Revisar guia"
        if not self.data in self.historial:
            self.historial.append(self.data[:])
        self.reset()
    def updateBackspace(self):
        """
            Actualiza el valor del frame del backspace, recordar que el backspace debe tener un contador de accion (de modo que el backspace no tenga
            efecto hasta despues de cierto tiempo) dada la rapidez con la que suceden las iteaciones. Tambien para que el usuario puede eliminar
            de manera continua sin soltar el backspace.

            El metodo retorna True en caso de que se haya eliminado realmente la ultima letra de la lista, False en caso contrario
        """
        if self.backspace_pressed:
            if self.remove_frame ==  self.remove_count_limit:
                self.remove_frame = 0
                self.data = self.data[:len(self.data)-1]
                return True
            else:
                self.remove_frame += 1
                return False
        else:
            self.remove_frame = self.remove_count_limit
            return False
    def reset(self):
        """
            Limpia el valor de la entrada
        """
        self.data = ""
    def updateHistorial(self, direction):
        """
            Actualiza la posicion del usuario relativamente a la tecla que este presione
        """
        if len(self.historial) > 0:
            if direction == "left":
                self.current_historial_index -= 1
                if self.current_historial_index < 0:
                    self.current_historial_index = len(self.historial) - 1
            else:
                self.current_historial_index += 1
                if self.current_historial_index > (len(self.historial) - 1):
                    self.current_historial_index = 0
            self.data = self.historial[self.current_historial_index][:]
        else:
            self.current_advertencia = f"Error, la lista de comandos reutilizables esta vacia ..."
    def removeCurrentHistorialElement(self):
        """
            Elimina el elemento del historial en el cual se este parado
        """
        if len(self.historial) > 0:
            self.historial.pop(self.current_historial_index)
            if self.current_historial_index == len(self.historial):
                self.current_historial_index -= 1
        else:
            self.current_advertencia = "Error, no hay comandos en el historial para eliminar ... "
        if len(self.historial) > 0:
            self.data = self.historial[self.current_historial_index][:]
        else:
            self.reset()

ANIMATION_DATA = {
        "animation_path"    : "test/megaman/shooting_running_right/",
        "size"              : [130,200],
        "has_alpha_pixels"  : True,
        "colorkey"          : None,
        "fps"               : 6,
<<<<<<< HEAD
        "background_color"  : (0,0,0),
        "rotated"           : False}
=======
        "background_color"  : (100,100,100)}
>>>>>>> df1e2443918d2f92a483e50254d521bbd089cf31

argvTesting(argv)
WINDOW_SIZE                     =   [1000, 800]
WINDOW                          =   pygame.display.set_mode(WINDOW_SIZE, RESIZABLE)
EXIT                            =   False
CLOCK                           =   pygame.time.Clock()
ANIMATION_MANAGER               =   AnimationManager(ANIMATION_DATA)
InputManager_                   =   InputManager()
HISTORIAL_COMMANDS              =   {"right" : K_DOWN, "left" : K_UP, "remove" : K_DELETE} # right para aumentar el indice y left para disminuirlo
COMMAND_KEYS                    =   [K_DOWN, K_UP, K_DELETE, K_RETURN, K_BACKSPACE]

refreshTerminalData(ANIMATION_DATA, InputManager_)

while not EXIT:
    WINDOW.fill(ANIMATION_DATA["background_color"])
    WINDOW.blit(ANIMATION_MANAGER.currentSprite(), [WINDOW_SIZE[0]//2 - ANIMATION_DATA["size"][0]//2, WINDOW_SIZE[1]//2 - ANIMATION_DATA["size"][1]//2] )

    # actualizacion de animacion
    ANIMATION_MANAGER.update()

    # administracion de eventos
    for event in pygame.event.get():
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            EXIT = True
        if (event.type == KEYDOWN or event.type == KEYUP) and (event.key == K_BACKSPACE):
            InputManager_.backspace_pressed = (event.type == KEYDOWN)
        if event.type == KEYDOWN:
            if  event.key not in COMMAND_KEYS:
                InputManager_.add(event.unicode)
            elif (event.key == K_RETURN):
                InputManager_.enter(ANIMATION_DATA, ANIMATION_MANAGER)
            elif (event.key == HISTORIAL_COMMANDS["right"]) or (event.key == HISTORIAL_COMMANDS["left"]):
                InputManager_.updateHistorial("right" if event.key == HISTORIAL_COMMANDS["right"] else "left")
            elif (event.key == HISTORIAL_COMMANDS["remove"]):
                InputManager_.removeCurrentHistorialElement()
            refreshTerminalData(ANIMATION_DATA, InputManager_)
        if event.type == WINDOWRESIZED:
            WINDOW_SIZE = [event.x, event.y]

    if InputManager_.updateBackspace():
        refreshTerminalData(ANIMATION_DATA, InputManager_)


    pygame.display.update()
    CLOCK.tick(60)



pygame.quit()
