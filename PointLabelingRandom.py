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
from matplotlib.font_manager import FontProperties
from PIL import ImageFont, ImageDraw
import random
from indexing.kdtree1 import *
from indexing.kdtree2a import *
from indexing.bst import *
from matplotlib.patches import BoxStyle
import pickle
import copy

label_list=['Adams','Allen','Ashland','Ashtabula','Athens',\
            'Auglaize','Belmont','Brown','Butler','Carroll','Champaign',\
            'Clark','Clermont','Clinton','Columbiana','Coshocton','Crawford',\
            'Cuyahoga','Darke','Defiance','Delaware','Erie','Fairfield','Fayette',\
            'Franklin','Fulton','Gallia','Geauga','Greene','Guernsey','Hamilton',\
            'Hancock','Hardin','Harrison','Henry','Highland','Hocking','Holmes','Huron',\
            'Jackson','Jefferson','Knox','Lake','Lawrence','Licking','Logan','Lorain','Lucas','Madison','Mahoning']
# set up the figure window for drawing
fig = plt.figure(figsize=(6, 6))

# Calculate the size of bbox for each label
width_list=[]
height_list=[]
for label in label_list:
    renderer1 = fig.canvas.get_renderer()
    txt1 = fig.text(1.5, 1.5, label, fontsize=11, fontname='Arial')
    bbox1 = txt1.get_window_extent(renderer1) # search this function to see the relationship
    width_list.append(bbox1.width)
    height_list.append(bbox1.height) 

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

# point_generate_random(num_points,num_pixel)
with open('x_list_file.pickle','rb') as file:
    x_list=pickle.load(file)
with open('y_list_file.pickle','rb') as file:
    y_list=pickle.load(file)
point_list=[]
for i in range(num_points):
    point_list.append(PointWithLabel(x_list[i], y_list[i]))
    

print(point_list[0].LabelPos)
for i in range(num_points):
    point_list[i].label=label_list[i]
    point_list[i].width=width_list[i]
    point_list[i].height=height_list[i]

print([point_list[i].label for i in range(num_points)])
# build the balanced kd tree of point list for searching later
point_list_tree=point_list.copy()
BalKdTree=kdtree2(point_list_tree)
print([point_list[i].label for i in range(num_points)])
# tree_print(BalKdTree)
# ax1.scatter([0], [0],s=2880000,
#             color='black', marker='.', alpha=1)
ax1.scatter([p.x for p in point_list], [p.y for p in point_list],s=72,
            color='grey', marker='.', alpha=1)


# Step 1: move the labels outside of the map into the map
# and move the labels overlapped with features to less desirable position
for i in range(num_points):
    # overlapped with feature or map boundary
    rect_label=get_rect(point_list[i])
    found=[]
    rect_for_tree=[[rect_label._x,rect_label._x+rect_label._width],[rect_label._y,rect_label._y+rect_label._height]]
    range_query_orthogonal(BalKdTree, rect_for_tree, found)

    if IsInMap(point_list[i], range_axe)==False or len(found)>0:
        point_list[i]=move_label_in(point_list[i],range_axe,BalKdTree) # how to avoid moving it out again? If not overlap with other feature then fix it
        point_list[i].fixed=True
        print(point_list[i].LabelPos)
    pass
            
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
        # if point_list[i].fixed==True:
        #     continue
        for j in range(num_points):
            if i==j:
                continue
            rect1=get_rect(point_list[i])
            rect2=get_rect(point_list[j])

            area=OverlapArea(rect1,rect2)
            if area>0 : # Ai and Aj overlap
                if point_list[i].fixed==False and point_list[j].fixed==False:
                    id_moved=get_id_moved(i,j,point_list)
                    # id_moved_list.append(id_moved) # why other case do not append moved id
                elif point_list[i].fixed==True and point_list[j].fixed==False:
                    id_moved=j
                elif point_list[i].fixed==False and point_list[j].fixed==True:
                    id_moved=i
                else:
                    print("i is ",i)
                    print("j is ",j)
                    if i==10:
                        print(point_list[i].label)
                    id_moved=min(i,j)
                    
                id_moved_list.append(id_moved)
                move_label_position(id_moved,point_list,BalKdTree,range_axe)
                print(point_list[id_moved_list[-1]].LabelPos)
            get_better_position(j, point_list,BalKdTree,range_axe)
        get_better_position(i, point_list,BalKdTree,range_axe)

        # identify whether point_list[i] overlapped with other labels and features and boundary
        if point_list[i].LabelPos==1:
            point_list[i].fixed=True #some problems
            rect1=get_rect(point_list[i])
            for j in range(num_points):
                if i==j:
                    continue
                rect2=get_rect(point_list[j])
                is_overlapped=IsOverlapped(rect1, rect2)
                if is_overlapped==True:
                    point_list[i].fixed = False
                    break
            if point_list[i].fixed == False:
                    continue
            # overlapped with feature or map boundary
            found=[]
            rect=[[rect1._x,rect1._x+rect1._width],[rect1._y,rect1._y+rect1._height]]
            range_query_orthogonal(BalKdTree, rect, found)
            if len(found)>0 or \
                (len(found)>0 or rect[0][0]<range_axe[0] or rect[0][1]>range_axe[1] or rect[1][0]<range_axe[2] or rect[1][1]>range_axe[3]):
                point_list[i].fixed=False
        if IsInMap(point_list[i], range_axe)==False:
            point_list[i]=move_label_in(point_list[i],range_axe,BalKdTree)

    # fix the label without overlaps in desirable position

    # get the total weight and area of the point list
    totalweight,totalarea=get_TotalWeiAre(point_list)
    totalweight_list.append(totalweight)
    totalarea_list.append(totalarea)
    counter=len(totalweight_list)

    # if counter==3:
    #     break

    # the ending condition for while loop
    if counter>2:
        if totalweight_list[-1]>=totalweight_list[-2] and totalarea_list[-1]>=totalarea_list[-2] :
            print("counter is: ", counter)
            break
    pass

# add texts and patches for the bbox to the figure
for p in point_list:
    renderer1 = fig.canvas.get_renderer()
    location=get_location(p)
    rect_elements = coord_label(p)

    txt1 = fig.text( rect_elements[0]/num_pixel, rect_elements[1]/num_pixel, p.label, horizontalalignment=location[0], 
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