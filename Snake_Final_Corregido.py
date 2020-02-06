import pygame
import math
import random
import tkinter as tk
from tkinter import messagebox



class cubo(object):   # Características del cubo
    columnas = 20
    anchura = 500

    def __init__(self, start, direccx = 1, direccy = 0, color=(255, 24, 77)):
        self.posicion = start
        self.direccx = 1
        self.direccy = 0
        self.color = color

    def movimiento(self, direccx, direccy):
        self.direccx = direccx
        self.direccy = direccy
        self.posicion = (self.posicion[0] + self.direccx, self.posicion[1] + self.direccy)

    def dibujar(self, superficie, ojos=False):
        dist = self.anchura // self.columnas
        i = self.posicion[0]
        j = self.posicion[1]

        pygame.draw.rect(superficie, self.color, (i * dist + 1, j * dist + 1, dist - 2, dist - 2))

        if ojos:            # OJOS DE LA SERPIENTE.
            centro = dist // 2
            radio = 3
            ojo1 = (i *  dist + centro - radio, j * dist + 8)
            ojo2 = (i * dist + dist - radio * 2, j * dist + 8)
            pygame.draw.circle(superficie, (255, 0, 0), ojo1, radio)  #COLOR DE OJOS
            pygame.draw.circle(superficie, (58, 12, 140), ojo2, radio)

class snake(object):
    cuerpo = []
    giros = {}

    def __init__(self, color, posicion):
        self.color = color
        self.cabeza = cubo(posicion)
        self.cuerpo.append(self.cabeza)
        self.direccx = 0
        self.direccy = 1

    def movimiento(self):               # Movimiento de la serpiente.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.direccx = -1
                    self.direccy = 0
                    self.giros[self.cabeza.posicion[:]] = [self.direccx, self.direccy]
                elif keys[pygame.K_RIGHT]:
                    self.direccx = 1
                    self.direccy = 0
                    self.giros[self.cabeza.posicion[:]] = [self.direccx, self.direccy]
                elif keys[pygame.K_UP]:
                    self.direccx = 0
                    self.direccy = -1
                    self.giros[self.cabeza.posicion[:]] = [self.direccx, self.direccy]
                elif keys[pygame.K_DOWN]:
                    self.direccx = 0
                    self.direccy = 1
                    self.giros[self.cabeza.posicion[:]] = [self.direccx, self.direccy]

        for i, c in enumerate(self.cuerpo):
            p = c.posicion[:]
            if p in self.giros:
                giro = self.giros[p]
                c.movimiento(giro[0], giro[1])
                if i == len(self.cuerpo) - 1:
                    self.giros.pop(p)
            else:
                if c.direccx == -1 and c.posicion[0] <= 0: c.posicion = (c.columnas-1, c.posicion[1])
                elif c.direccx == 1 and c.posicion[0] >= c.columnas-1: c.posicion = (0,c.posicion[1])
                elif c.direccy == 1 and c.posicion[1] >= c.columnas-1: c.posicion = (c.posicion[0], 0)
                elif c.direccy == -1 and c.posicion[1] <= 0: c.posicion = (c.posicion[0],c.columnas-1)
                else: c.movimiento(c.direccx,c.direccy)

    def reset(self, posicion):
        self.cabeza = cubo(posicion)
        self.cuerpo = []
        self.cuerpo.append(self.cabeza)
        self.giros = {}
        self.direccx = 0
        self.direccy = 1

    def agregarCubo(self):
        cola = self.cuerpo[-1]
        dx, dy = cola.direccx, cola.direccy

        if dx == 1 and dy == 0:
            self.cuerpo.append(cubo((cola.posicion[0] - 1, cola.posicion[1])))
        elif dx == -1 and dy == 0:
            self.cuerpo.append(cubo((cola.posicion[0] + 1, cola.posicion[1])))
        elif dx == 0 and dy == 1:
            self.cuerpo.append(cubo((cola.posicion[0], cola.posicion[1] - 1)))
        elif dx == 0 and dy == -1:
            self.cuerpo.append(cubo((cola.posicion[0], cola.posicion[1] + 1)))

        self.cuerpo[-1].direccx = dx
        self.cuerpo[-1].direccy = dy

    def dibujar(self, superficie):
        for i, c in enumerate(self.cuerpo):
            if i == 0:
                c.dibujar(superficie, True)  # Este True simplimente le dibuja ojos a la cabeza de nuestra serpiente.
            else:
                c.dibujar(superficie)

def dibujarMalla(anchura, columnas, superficie):
    espSeparacion = anchura // columnas

    x = 0
    y = 0
    for l in range(columnas):
        x = x + espSeparacion
        y = y + espSeparacion
        pygame.draw.line(superficie, (255, 255, 255), (x, 0), (x, anchura))  # Color (RGB) de las líneas de la malla.
        pygame.draw.line(superficie, (255, 255, 255), (0, y), (anchura, y))


def redibujarVentana(superficie):
    global columnas, anchura, s, comida

    superficie.fill((153, 217, 234))  # Acá podemos cambiar el color del fondo del juego (en RGB).
    s.dibujar(superficie)
    comida.dibujar(superficie)
    dibujarMalla(anchura, columnas, superficie)
    pygame.display.update()


def comidaRandom(columnas, item):
    posiciones = item.cuerpo

    while True:
        x = random.randrange(columnas)
        y = random.randrange(columnas)

        if len(list(filter(lambda z: z.posicion == (x, y), posiciones ))) > 0: #Esta función evita que aparezca comida sobre la serpiente.
            continue
        else:
            break
    return (x, y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)

    try:
        root.destroy()
    except:
        pass

def configuracion():
    global columnas, anchura, s, comida
    anchura = 500
    columnas = 20  # Si queremos modificar la dificultad del juego, podemos disminuir el valor de esta variable.
    ventana = pygame.display.set_mode((anchura, anchura))
    s = snake((255, 24, 77), (10, 10))  # El primer paréntesis es el código RGB del color de la serpiente.
    comida = cubo(comidaRandom(columnas, s), color= (239, 221, 5))                                     
    flag = True
    clock = pygame.time.Clock()  # Esta función limita los fps a los que nuestro juego corre.

    while flag:
        pygame.time.delay(50)  # Entre más bajo sea el time delay, más rápido se moverá nuestra serpiente.
        clock.tick(10)         # Esta función limita los fps de nuestro juego. Entre menor sea el número más lento
        s.movimiento()         # se moverá la serpiente.
        if s.cuerpo[0].posicion == comida.posicion:
            s.agregarCubo()
            comida = cubo(comidaRandom(columnas, s), color=(239, 221, 5))
        for x in range(len(s.cuerpo)):
            if s.cuerpo[x].posicion in list(map(lambda z: z.posicion, s.cuerpo[x + 1:])):
                print("Puntaje: ", len(s.cuerpo))
                message_box("F por ti :(", "¡Inténtalo de nuevo!")
                s.reset((10,10))
                break

        redibujarVentana(ventana)


configuracion()
#GG!
