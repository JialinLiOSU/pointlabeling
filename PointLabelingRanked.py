### Point labeling for ranked points
'''
Point Labeling Experiment Main Process
package geom and indexing is from Ningchuan xiao(cxiao@gmail.com)
'''

import sys
sys.path.append("E:\\pyLibs")
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

# point_generate_random(num_points,num_pixel)
with open('E:\\pyLibs\\pointlabeling\\ranked labeling.pickle','rb') as file:
    point_list=pickle.load(file)
    pass

label_list=[]
x_list=[]
y_list=[]

for p in point_list:
    label_list.append(p.label)
    x_list.append(p.x)
    y_list.append(p.y)

x_max=max(x_list)
x_min=min(x_list)
y_max=max(y_list)
y_min=min(y_list)
x_range=x_max-x_min
y_range=y_max-y_min

# set up the figure window for drawing
fig = plt.figure() # how to get the size of figure

# Calculate the size of bbox for each label
width_list=[]
height_list=[]
for label in label_list:
    renderer1 = fig.canvas.get_renderer()
    txt1 = fig.text(1.5, 1.5, label, fontsize=11, fontname='Arial')
    bbox1 = txt1.get_window_extent(renderer1)  # search this function to see the relationship
    width_list.append(bbox1.width)
    height_list.append(bbox1.height) 

print(len(height_list))

axe_x_min=0
axe_x_max=x_range
axe_y_min=0
axe_y_max=x_range
range_axe=[axe_x_min,axe_x_max,axe_y_min,axe_y_max]

left, bottom, width, height = 0, 0, 1, 1
ax1 = plt.Axes(fig, [0., 0., 1., 1.])
# ax1.set_axis_off()
fig.add_axes(ax1)
# ax1 = fig.add_axes([left, bottom, width, height])

# coordinate of the first point in verticle line
num_pixel_x=800 # the ratio of pixel number by fig size is 100
num_pixel_y=400
num_points=len(point_list)
# generate the point list and add them on ax1

print(point_list[0].LabelPos)
for i in range(num_points):
    point_list[i].width=width_list[i]
    point_list[i].height=height_list[i]


# build the balanced kd tree of point list for searching later
point_list_tree=point_list.copy()
BalKdTree=kdtree2(point_list_tree)

# tree_print(BalKdTree)
# ax1.scatter([0], [0],s=2880000,
#             color='black', marker='.', alpha=1)
ax1.scatter([p.x for p in point_list], [p.y for p in point_list],s=72,
            color='grey', marker='.', alpha=1)

# add texts and patches for the bbox to the figure
for p in point_list:
    renderer1 = fig.canvas.get_renderer()
    location=get_location(p)
    rect_elements = coord_label(p)

    txt1 = fig.text( (rect_elements[0]-x_min)/x_range, (rect_elements[1]-y_min)/y_range, p.label, horizontalalignment=location[0], 
                verticalalignment=location[1], fontsize=11, fontname='Arial')

    # width = txt1.get_bbox_patch().get_extents().width
    bbox1 = txt1.get_window_extent(renderer1) # search this function to see the relationship
    rect1 = Rectangle([bbox1.x0, bbox1.y0], bbox1.width, bbox1.height,
                color=[0, 0, 0], fill=False)
    fig.patches.append(rect1)
rect_list=fig.patches

# overlap=OverlapArea(rect_list[0],rect_list[1])
# be consistent with the pixel coordinate
# ax1.set_ylim([axe_x_min, axe_x_max])
# ax1.set_xlim([axe_y_min, axe_y_max])
# ax1.set_aspect(1)
ax1.margins(0)
ax1.axis("off")

plt.show()