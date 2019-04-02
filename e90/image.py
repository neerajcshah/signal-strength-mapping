from PIL import Image
import psutil
import sys
import math
import json
import time
import utm
import numpy as np
from scipy.spatial import distance

# MIN_LAT = 39.902725 
# MAX_LAT = 39.908450
# MAX_LON = -75.349260
# MIN_LON = -75.35727

MIN_LAT = 39.902541
MAX_LAT = 39.909508
MAX_LON = -75.351278
MIN_LON = -75.357601

MIN_EAST, MAX_NORTH, _, _ = utm.from_latlon(MIN_LAT, MIN_LON)
MAX_EAST, MIN_NORTH, _, _ = utm.from_latlon(MAX_LAT, MAX_LON)

EAST_LEN = MAX_EAST - MIN_EAST
NORTH_LEN = MAX_NORTH - MIN_NORTH

DRAW_DOTS=True

MAX_X = 1000
MAX_Y = 1000

# USE UTM TO NORTHINGS/EASTINGS
# USE NUMPY FOR VECTORIZED CODE TO MAKE IT FASTER
# USE NUMPY TO TAPER OFF THE 


### Create layer function: Build the map
def createLayer(fname):
  print("Processing")
  points = process(fname)
  # convert dbm to magnitude
  points = [[dbmToScale(dbm), SSID, float(lat), float(lon)] for (dbm, SSID, lat, lon) in points if lat != 'n/a'] 

  x = []
  y = []
  f = []
  for i in range(len(points)):
    e,n,_,_ = utm.from_latlon(points[i][2],points[i][3])
    points[i][2] = e
    points[i][3] = n
    x.append(points[i][2])
    y.append(points[i][3])
    f.append(points[i][0])

  '''
  for i in range(len(points)):
    print(points[i])
  '''

  '''
  # run through pixels
  pixels = np.zeros((MAX_X, MAX_Y))
  xyrng = np.arange(MAX_X)
  xgrid, ygrid = np.meshgrid(xyrng, xyrng)
  e, n = pixel_to_en(xgrid,ygrid)
  pixels = gaussian(points, e, n)
  '''


  xyrng = np.linspace(0, MAX_X, MAX_X)
  xgrid, ygrid = np.meshgrid(xyrng, xyrng)
  dnm = np.zeros_like(xgrid)
  num = np.zeros_like(ygrid)

  x_y_f = np.array([x,y,f],dtype=np.float32)

  weight = np.zeros((len(xgrid),len(ygrid),len(f)))
  weight = 10000.*np.exp(-(np.square((xgrid.transpose() - x_y_f[0]).transpose()) + np.square((ygrid.transpose() - x_y_f[1]).transpose()))/(2.0*std_dev**2))

  dnm = np.sum(weight, axis=0)
  num = np.sum((weight.transpose() * x_y_f[2]).transpose(), axis=0)

  pixels = np.where(dnm < 1e-20, 0, num/dnm)

  '''
  for x in range(MAX_X):
    for y in range(MAX_Y):
      e, n = pixel_to_en(x,y)
      pixels[x,y] = gaussian(points, e, n)
  '''

  I = Image.new('RGBA', (MAX_X, MAX_Y))
  I.putalpha(64)
  IM = I.load()
  for x in range(MAX_X):
      for y in range(MAX_Y):
          IM[x,y] = color(pixels[x,y])
  if DRAW_DOTS:
      for _, _, e, n in points:
          x, y = en_to_pixel(e, n)
          if 0 <= x < MAX_X and 0 <= y < MAX_Y:
              IM[x,y] = (0,0,0)
              # print("Writing point at : %d %d" %(x,y))

  out_fname = fname + ".phantom." + str(MAX_X)
  I.save(out_fname + ".png", "PNG")


### Read points and build a 'points' array of quadruples
def process(fname):
  points = []
  with open(fname) as f:
    data = json.load(f)
    for item in data['JsonData']:
      min_dbm = float('-inf')
      for wifi in item['wifi']:
        if (wifi['SSID'] == 'eduroam' and float(wifi['DBM']) > min_dbm):
          min_dbm = float(wifi['DBM'])
          
      points.append((min_dbm, 'eduroam', item['Latitude'], item['Longitude']))
    
  return points

### points = [(dbm, ssid, lat, long)]

std_dev = 2
gaussian_a = 1.0/(math.sqrt(2*math.pi*std_dev**2))
gaussian_const = -1/(2.0*std_dev**2)

### Gaussian function: Interpolate intermediary points
def gaussian(points, e, n):
  num = 0
  dnm = 0
  c = 0

  for magnitude,_,mE,mN in points:
    weight = math.exp(distance_squared(e,n,mE,mN) * gaussian_const)
    num += magnitude * weight
    dnm += weight

  if dnm < 1e-20:
    return None
  else:
    return num/dnm
    

def color(val):
    stride = 2

    if val is None:
        return (255,255,255,0)

    colors = [(255, 0, 0),
              (255, 91, 0),
              (255, 127, 0),
              (255, 171, 0),
              (255, 208, 0),
              (255, 240, 0),
              (255, 255, 0),
              (218, 255, 0),
              (176, 255, 0),
              (128, 255, 0),
              (0, 255, 0),
              (0, 255, 255),
              (0, 240, 255),
              (0, 213, 255),
              (0, 171, 255),
              (0, 127, 255),
              (0, 86, 255),
              (0, 0, 255),
              ]

    colors = colors[::-1]

    print(val)
    for i in range(len(colors)-1, -1, -1):
        if val >= i*stride:
          return colors[i]
    return colors[-1]


def pixel_to_en(x,y):

    east = (float(x)/MAX_X)*EAST_LEN + MIN_EAST
    north = (float(y)/MAX_Y)*NORTH_LEN + MIN_NORTH
    
    return east, north

def en_to_pixel(east,north):

    x = int(((east-MIN_EAST)/EAST_LEN)*MAX_X)
    y = int(((north-MIN_NORTH)/NORTH_LEN)*MAX_Y)

    return x,y

def distance_squared(x1,y1,x2,y2):
    return (x1-x2)**2 + (y1-y2)**2

def distance(x1,y1,x2,y2):
    return math.sqrt(distance_squared(x1,y1,x2,y2))

def dbmToScale(dbm):
  ### Return scales dbm so that it is real/positive
  return dbm + 100

createLayer('public/wifi_gps_data.json')
