'''
Point Labeling Experiment Main Process
package geom and indexing is from Ningchuan xiao(cxiao@gmail.com)
'''
import sys
sys.path.append("E:\\pylibs")
from geom.point import *
from pointlabeling.SimPointExperiment import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.text import *
from matplotlib.patches import Rectangle
from PIL import ImageFont, ImageDraw
import random
from indexing.kdtree1 import *
from indexing.kdtree2a import *
from indexing.bst import *
from matplotlib.patches import BoxStyle

# point1=PointWithLabel(1,1,'test')
# point2=point1
# point2.label='changed'
# print(point2.label)
# print(point1.label)


font = ImageFont.truetype("arial.ttf", 11)

size1=font.getsize("Adams")
size2=font.getsize("adams")

label_list=['Adams','Allen','Ashland','Ashtabula','Athens',\
            'Auglaize','Belmont','Brown','Butler','Carroll','Champaign',\
            'Clark','Clermont','Clinton','Columbiana','Coshocton','Crawford',\
            'Cuyahoga','Darke','Defiance','Delaware','Erie','Fairfield','Fayette',\
            'Franklin','Fulton','Gallia','Geauga','Greene','Guernsey','Hamilton',\
            'Hancock','Hardin','Harrison','Henry','Highland','Hocking','Holmes','Huron',\
            'Jackson','Jefferson','Knox','Lake','Lawrence','Licking','Logan','Lorain','Lucas','Madison','Mahoning']
# set up the figure window for drawing
fig = plt.figure(figsize=(6, 6))
axe_x_min=0
axe_x_max=600
axe_y_min=0
axe_y_max=600
range_axe=[axe_x_min,axe_x_max,axe_y_min,axe_y_max]

left, bottom, width, height = 0, 0, 1, 1
ax1 = fig.add_axes([left, bottom, width, height])

# coordinate of the first point in verticle line
num_pixel=600 # the ratio of pixel number by fig size is 100
x = num_pixel/2 # put the line of points in the center of fig
y = 70
num_points=50
# generate the point list and add them on ax1
point_list = point_generate_vertical(x, y, 3, 3, num_points)
print(point_list[0].LabelPos)
for i in range(num_points):
    point_list[i].label=label_list[i]
# build the balanced kd tree for searching later
print(point_list[0].label)
BalKdTree=kdtree2(point_list)
# tree_print(BalKdTree)
# ax1.scatter([0], [0],s=2880000,
#             color='black', marker='.', alpha=1)
ax1.scatter([p.x for p in point_list], [p.y for p in point_list],s=72,
            color='grey', marker='.', alpha=1)

# Based on the point_list generated to calculate the final label placement
# step 2: find overlapped agents Ai and Aj
# generate the list of rectangle for the points

totalweight_list=[]
totalarea_list=[]
id_moved_list=[]

while True:
    #label_rect_list=get_rect_list(point_list)
    # use tree to calculate the overlap with feature and boundary
    for i in range(num_points):
        for j in range(i,num_points):
            if i==j:
                continue
            rect1=get_rect(point_list[i])
            rect2=get_rect(point_list[j])
            # area=OverlapArea(label_rect_list[i],label_rect_list[j])
            area=OverlapArea(rect1,rect2)
            if area>0: # Ai and Aj overlap
                id_moved=get_id_moved(i,j,point_list)
                id_moved_list.append(id_moved)
                move_label_position(id_moved,point_list,BalKdTree,range_axe)
                print(point_list[id_moved_list[-1]].LabelPos)
                # label_rect_list=get_rect_list(point_list)
                
    # try whether get back to more desirable position

    get_better_position(point_list,BalKdTree)

    # fix the label without overlaps in desirable position
    


    # get the total weight and area of the point list
    totalweight,totalarea=get_TotalWeiAre(point_list)
    totalweight_list.append(totalweight)
    totalarea_list.append(totalarea)
    counter=len(totalweight_list)

    # the ending condition for while loop
    if counter>2:
        if totalweight_list[-1]==totalweight_list[-2] and totalarea_list[-1]==totalarea_list[-2] and \
            totalweight_list[-3]==totalweight_list[-2] and totalarea_list[-3]==totalarea_list[-2]:
            break
    pass

# add texts and patches for the bbox to the figure
for p in point_list:
    # if p==point_list[2]:
        # p.LabelPos=1
        size = font.getsize(p.label)
        rect_elements = coord_label(p)
        # p.LabelPos=8
        # coord_label() is in SimPointExperiment.py
        # To calculate the coordinate of label in different positions
        
        renderer1 = fig.canvas.get_renderer()
        location=get_location(p)
        txt1 = fig.text( rect_elements[0]/ num_pixel, rect_elements[1] /
                    num_pixel, p.label, horizontalalignment=location[0], 
                    verticalalignment=location[1], fontsize=11, fontname='Arial')
       

        # width = txt1.get_bbox_patch().get_extents().width

        bbox1 = txt1.get_window_extent(renderer1) # search this function to see the relationship
        rect1 = Rectangle([bbox1.x0, bbox1.y0], bbox1.width, bbox1.height,
                      color=[0, 0, 0], fill=False)
        fig.patches.append(rect1)
rect_list=fig.patches

# overlap=OverlapArea(rect_list[0],rect_list[1])
# be consistent with the pixel coordinate
ax1.set_ylim([axe_x_min, axe_x_max])
ax1.set_xlim([axe_y_min, axe_y_max])

plt.show()