import Image
import ImageDraw
import numpy as np
from sys import argv
import time
 
VERTICAL = 1
HORIZONTAL = 0
MAXIMA = 1
MINIMA = 0
 
#size = 20 #images
size = 35 #texto
 
def Obtener_puntos(vector, type = MAXIMA):
  pos = []
  maximo = max(vector)
  minimo = min(vector)
  umbral = (maximo + minimo)/2
  for i in range(1, len(vector) - 1):
    if type == MAXIMA:
      if (vector[i] > vector[i-1]) and (vector[i] > vector[i+1]):
        pos.append(i)
        if vector[i] > umbral: pos.append(i)
  
    elif type == MINIMA:
      if (vector[i] < vector[i-1]) and (vector[i] < vector[i+1]): 
        pos.append(i)
        if vector[i] > umbral: pos.append(i)
  return pos
 
def binarize(img, umbral):
  width, height = img.size
  pixels = img.load()
  out = Image.new('RGB', (width, height))
  out_pix = out.load()
  for i in range(width):
    for j in range(height):
      r, g, b = pixels[i, j]
      if r > umbral:
        out_pix[i, j] = (255, 255, 255)
      else:
        out_pix[i, j] = (0, 0, 0)
  return out
 
def Histogramas(img, orientation = VERTICAL):
  tmp = img.copy()
  pixels = np.array(tmp.convert('L'))
  if orientation == VERTICAL:
    return [sum(x) for x in zip(*pixels)]
  else:
    return [sum(x) for x in pixels]
 
def verify_area(img, (x1, y1), (x2, y2)):
  width, height = img.size
  pixels = img.load()
  area = abs(x2 - x1) * abs(y2 - y1)
  cont = 0
  for x in range(x1, x2):
    for y in range(y1, y2):
      if x > 0 and x < width  and y > 0 and y < height:
        if pixels[x, y] == (0, 0, 0):
          cont += 1
  if cont > area * 0.2:
    return True
  else:
    return False
 
def Pintar(bw, vertical, horizontal, lines=False):
  width, height = bw.size
  img = Image.open(argv[1])
  draw = ImageDraw.Draw(img)
  c = 0
  grid = []
  for i in range(width):
    grid.append([])
    for j in range(height):
        grid[i].append(0)

  for j in horizontal:
    for i in vertical: 
      (x1, y1), (x2, y2) = (i-(size/2), j-(size/2)), (i+(size/2), j+(size/2))
      if verify_area(bw, (x1, y1), (x2, y2)):
        c+= 1
        grid[x1][y1] = 1
        draw.rectangle([(x1, y1), (x2, y2)], outline='yellow')
  img.save('puntos.png', 'PNG')  
  draw = ImageDraw.Draw(bw)  
  for j in vertical:
    draw.line(((j, 0), (j, height)), (255, 0, 0))
  for i in horizontal:  
    draw.line(((0, i), (width, i)), (0, 255, 0))
  bw.save('lineas.png', 'PNG')
  print 'listo'
  return  grid,width,height

def Ablandar(x,window_len=11,window='hanning'):
  s=np.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
  width=eval('np.'+window+'(window_len)')
  y=np.convolve(width/width.sum(), s, mode='valid')
  return y

#def matriz(img):

def met(grid,ancho,alto):
  a1 = 0
  a12 = alto/3  
  a2 = a12
  a23 = alto/3 + alto/3
  #a3 = a23
  #a34 = altura
  lugar = 0
  arreglo = [[0,0,0],[0,0,0]]
  cons = 0
  contr = 0
  i = 0
  j = 0

  #while i < ancho:
   #while j < alto:
  for i in range(ancho):
    for j in range(alto):
        if grid[i][j] == 1:
            if 0 < j < alto/3 and 0 < i < ancho/2:
              arreglo[0][0] = 1
            if 0 < j < alto/3 and ancho/2 < i < ancho:
              arreglo[1][0] = 1
            if alto/3 < j < alto/3 + alto/3 and 0 < i < ancho/2:
              arreglo[0][1] = 1
            if alto/3 < j < alto/3 + alto/3 and ancho/2 < i < ancho:
              arreglo[1][1] = 1
            if alto/3+alto/3 < j < alto and 0 < i < ancho/2:
              arreglo[0][2] = 1
            if alto/3+alto/3 < j < alto and ancho/2 < i < ancho:
              arreglo[1][2] = 1
    #for i in range(ancho):
    #    arreglo.append([])
    #    for j in range(alto):
    #        if grid[i][j] == 1:
    #        if j == cosaf:
    #            cosai = cosaf
    #            cosaf = cosaf + cosaf
  return arreglo

def traduccion(arreglo):
  file = open('braille.txt', 'r')
  file2 = open('asci.txt', 'r')
  nuevo = []

  for i in range(len(arreglo)):
    for j in range(len(arreglo[i])):
      nuevo.append(str(arreglo[i][j]))
  nuevo = "".join(nuevo)
  cont = 0
  cos = 0
  print "valor del arreglo : ",nuevo
  for line in file:
    #print line
    con = 0
    for i in range(len(line)-1):
      if line[i] != nuevo[i]:
        con = 1
    if con == 0:
      cos = cont
    cont = cont + 1
  cont = 0
  for line in file2:
    if cont == cos:
      print "valor de la letra: ",line
    cont = cont + 1

if __name__ == "__main__":
  tiempoi = time.time()
  img = Image.open(argv[1]).convert('RGB')
  img = binarize(img, 90) #images
  #img = binarize(img, 110)
  #img = binarize(img, 148) #texto
  vertical = Histogramas(img, VERTICAL)
  horizontal = Histogramas(img, HORIZONTAL)
  horizontal = list(Ablandar(np.array(horizontal)))
  vertical = list(Ablandar(np.array(vertical)))
  grid,anch,alt = Pintar(img, Obtener_puntos(vertical, type = MINIMA), Obtener_puntos(horizontal, type = MINIMA))
  #for i in range(anch):
  #  for j in range(alt):
  #      if grid[i][j] == 1:
  #          print "a un punto"
  arreglo = met(grid,anch,alt)
  print arreglo
  traduccion(arreglo)
  tiempof = time.time()
  tiempot = tiempof - tiempoi
  print 'Se tardo: ', tiempot 
