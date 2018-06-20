### Read shape file of populated cities in the US to get the data for labeling
import sys
sys.path.append('E:\\pylibs\\mapping')
from shapex import *

fname="E:\\pyLibs\\pointlabeling\\data\\ne_10m_populated_places_simple\\Populated_places_US_mainland_Projected.shp"
shp=shapex(fname)
print("number of points",len(shp))
print(shp.schema)

import sys
sys.path.append('E:\\pylibs')
from geom.point import *
from pointlabeling.SimPointExperiment import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.text import *
from matplotlib.patches import Rectangle
from matplotlib.font_manager import FontProperties
from PIL import ImageFont, ImageDraw
import random
from indexing.kdtree1 import *
from indexing.kdtree2a import *
from indexing.bst import *
from matplotlib.patches import BoxStyle
import pickle
import copy

### point information needed
scalerank_list=[]
name_list=[]
lon_list=[]
lat_list=[]

for p in shp:
    scalerank=p['properties']['scalerank']
    if scalerank<=6:          # get the data of cities ranking from 0 to 6
        scalerank_list.append(scalerank)
        name_list.append(p['properties']['name'])
        lon_list.append(p['geometry']['coordinates'][0])
        lat_list.append(p['geometry']['coordinates'][1])
    pass

point_list=[]
for i in range(len(name_list)):
    point_list.append(PointWithLabel(lon_list[i], lat_list[i],label=name_list[i],priority=scalerank_list[i]))

f = open('E:\\pyLibs\\pointlabeling\\ranked labeling.pickle', 'wb')
pickle.dump(point_list, f)
f.close()
