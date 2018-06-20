'''
    Provide basic functions for Simulated point feature experiments
    including generating simulated point data in a coordinate range
    drawing selected labeling placements

    The point class is from Ningchuan Xiao(cxiao@gmail.com)

    Author:
    Jialin Li
    jialin.li.osu@gmail.com
    Date:
    2/6/2018
'''
import random
import numpy as np
import sys
sys.path.append("E:\\pylibs")
from geom.point import *
from math import sqrt
from matplotlib.patches import Rectangle
from PIL import ImageFont, ImageDraw
from indexing.kdtree1 import *
from indexing.kdtree2a import *
from indexing.bst import *
import copy

class PointWithLabel:
    '''
    A class for points in Cartesian coordinate systems.
    including the coordinate of the point(x,y), label,label position and priority
    LabelPos can be the integer from 1-8, indicating 8 places surrounding the point
    '''
    def __init__(self, x, y, label='test', LabelPos=1, priority=1, credit=0, width=None, height=None, fixed=False, radius=None):
        self.x = x
        self.y = y
        self.label = label
        self.LabelPos = LabelPos
        self.priority = priority
        self.credit = credit
        self.width=width
        self.height=height
        self.fixed=fixed
        self.radius = radius

    def __getitem__(self, i):
        if i == 0:
            return self.x
        if i == 1:
            return self.y
        return None

    def __len__(self):
        return 2

    def __eq__(self, other):
        if isinstance(other, PointWithLabel):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def isvalid(self):
        if not isinstance(self.x, (int, float)) \
                or not isinstance(self.y, (int, float)):
            return False
        return True

    def __str__(self):
        '''NaP: Not a point'''
        if not self.isvalid():
            return 'NaP'
        if isinstance(self.x, (int)):
            fmtstr = '({0}, '
        else:
            fmtstr = '({0:.1f}, '
        if isinstance(self.y, (int)):
            fmtstr += '{1})'
        else:
            fmtstr += '{1:.1f})'
        return fmtstr.format(self.x, self.y)

    def __repr__(self):
        return self.__str__()

    def distance(self, other):
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        pass
    pass

def get_ax_size(ax):
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width, height = bbox.width, bbox.height
    width *= fig.dpi
    height *= fig.dpi
    return width, height
    
def IsInMap(point,range_axe):
    '''
    identify whether the point is in the map region and overlap with features
    '''
    rect1 = get_rect(point)
    # overlapped with feature or map boundary
    rect=[[rect1._x,rect1._x+rect1._width],[rect1._y,rect1._y+rect1._height]]
    if rect[0][0]<range_axe[0] or rect[0][1]>range_axe[1] or rect[1][0]<range_axe[2] or rect[1][1]>range_axe[3]:
        return False
    else:
        return True

# step 1: adjust the labels out of the axe range
# def move_label_in(point,range_axe):
#     '''
#     if the label is not in the map, move the label to other positions to make it in
#     '''
#     point_temp = copy.deepcopy(point)
#     for i in range(point_temp.LabelPos+1,8):
#         is_in_map=IsInMap(point_temp, range_axe)
#         if is_in_map==False:
#             point_temp.LabelPos=i
#         else:
#             point_temp.credit+=1
#             break
#     if is_in_map==True:
#         point.LabelPos=point_temp.LabelPos
#         point.credit=point_temp.credit
#     return point

def move_label_in(point,range_axe,BalKdTree):
    '''
    if the label is not in the map, move the label to other positions to make it in
    '''
    point_temp = copy.deepcopy(point)
    point_temp.LabelPos=point_temp.LabelPos+1
    point_temp.credit=point_temp.credit+1
    for i in range(point_temp.LabelPos,8):
        is_in_map=IsInMap(point_temp, range_axe)
        rect1 = get_rect(point_temp)
        found=[]
        rect=[[rect1._x,rect1._x+rect1._width],[rect1._y,rect1._y+rect1._height]]
        range_query_orthogonal(BalKdTree, rect, found)
        if is_in_map==False or len(found)>0:
            point_temp.LabelPos=point_temp.LabelPos+1
            point_temp.credit+=1
        else:
            break
    if IsInMap(point_temp, range_axe)==True:
        point.LabelPos=point_temp.LabelPos
        point.credit=point_temp.credit
    return point

def point_generate_random(num_points,num_pixel):
    '''
    gererate simulated random points given the number of points and range of pixels
    here, x and y are screen coordinate
    the generated points will be save in local address
    '''
    point_list=[]
    x_list = [num_pixel*random.random() for i in range(num_points)]
    y_list = [num_pixel*random.random() for i in range(num_points)]
    file_x=open('x_list_file.pickle','wb')
    pickle.dump(x_list,file_x)
    file_x.close()

    file_y=open('y_list_file.pickle','wb')
    pickle.dump(y_list,file_y)
    file_x.close()

font = ImageFont.truetype("arial.ttf", 11)

def get_location(PointWithLabel):
    location_list=['top','bottom','left','right','center']
    if PointWithLabel.LabelPos==1:
        horizon=location_list[2]
        verticle=location_list[1]
    elif PointWithLabel.LabelPos==2:
        horizon=location_list[3]
        verticle=location_list[1]
    elif PointWithLabel.LabelPos==3:
        horizon=location_list[3]
        verticle=location_list[0]
    elif PointWithLabel.LabelPos==4:
        horizon=location_list[2]
        verticle=location_list[0]
    elif PointWithLabel.LabelPos==5:
        horizon=location_list[2]
        verticle=location_list[4]
    elif PointWithLabel.LabelPos==6:
        horizon=location_list[4]
        verticle=location_list[1]
    elif PointWithLabel.LabelPos==7:
        horizon=location_list[3]
        verticle=location_list[4]
    elif PointWithLabel.LabelPos==8:
        horizon=location_list[4]
        verticle=location_list[0]
    else:
        horizon='error'
        verticle='error'
    return [horizon,verticle]


def coord_label(point_label):
    '''
    Get the coordinate, width and height of a label for point based on label position
    input:
    point_label the object of Class PointWithLabel
    output:
    coord_x and coord_y are the coordinate of lowerleft point of text
    '''
    coord_x=0
    coord_y=0
    if point_label.LabelPos == 1:
        coord_x = point_label.x+4
        coord_y = point_label.y+4
    elif point_label.LabelPos == 2:
        coord_x = point_label.x - 4
        coord_y = point_label.y + 4
    elif point_label.LabelPos == 3:
        coord_x = point_label.x - 4
        coord_y = point_label.y - 4
    elif point_label.LabelPos == 4:
        coord_x = point_label.x + 4
        coord_y = point_label.y - 4
    elif point_label.LabelPos == 5:
        coord_x = point_label.x + 4
        coord_y = point_label.y
    elif point_label.LabelPos == 6:
        coord_x = point_label.x
        coord_y = point_label.y + 4
    elif point_label.LabelPos == 7:
        coord_x = point_label.x - 4
        coord_y = point_label.y
    elif point_label.LabelPos == 8:
        coord_x = point_label.x 
        coord_y = point_label.y - 4
    return [coord_x, coord_y, point_label.width, point_label.height] 


def get_rect_list(point_list):
    '''
    based on a set of points to generate the list of rectangles for their labels
    '''
    rect_list = []
    for point in point_list:
        rect=get_rect(point)
        rect_list.append(rect)
    return rect_list

def get_rect(point):
    '''
    based on a point to generate the rectangle of its label
    '''
    rect_elements=coord_label(point)
    if point.LabelPos==2:
        rect_elements[0]=rect_elements[0]-rect_elements[2]
    elif point.LabelPos==3:
        rect_elements[0]=rect_elements[0]-rect_elements[2]
        rect_elements[1]=rect_elements[1]-rect_elements[3]
    elif point.LabelPos==4:
        rect_elements[1]=rect_elements[1]-rect_elements[3]
    elif point.LabelPos==5:
        rect_elements[1]=rect_elements[1]-rect_elements[3]/2
    elif point.LabelPos==6:
        rect_elements[0]=rect_elements[0]-rect_elements[2]/2
    elif point.LabelPos==7:
        rect_elements[0]=rect_elements[0]-rect_elements[2]
        rect_elements[1]=rect_elements[1]-rect_elements[3]/2
    elif point.LabelPos==8:
        rect_elements[0]=rect_elements[0]-rect_elements[2]/2
        rect_elements[1]=rect_elements[1]-rect_elements[3]
    
    rect=Rectangle([rect_elements[0], rect_elements[1]], rect_elements[2], rect_elements[3])
    return rect

def point_generate_vertical(x, y, radius, interval, number):
    '''
    gererate simulated point data given the coordinate of first point, radius, interval and number of points
    here, x and y are screen coordinate
    '''
    point_list=[]
    x_list = [x for i in range(number)]
    y_list = [y + (radius * 2 + interval) * i for i in range(number)]
    for i in range(number):
        point_list.append(PointWithLabel(x_list[i], y_list[i]))
    return point_list


def OverlapArea(rect_1, rect_2):
    '''
    Calculate the overlapping area of the two rectangles
    '''
    range_r1 = [rect_1.xy[0], rect_1.xy[1], rect_1.xy[0] +
                rect_1._width, rect_1.xy[1] + rect_1._height]
    range_r2 = [rect_2.xy[0], rect_2.xy[1], rect_2.xy[0] +
                rect_2._width, rect_2.xy[1] + rect_2._height]

    if range_r2[0] > range_r1[2] or range_r2[2] < range_r1[0] or range_r2[1] > range_r1[3] or range_r2[3] < range_r1[1]:
        area = 0
    else:
        wid = min(rect_1._width, rect_2._width)
        hei = min(rect_1._height, rect_2._height)
        area = min(min(abs(range_r2[0] - range_r1[2]), abs(range_r2[2] - range_r1[0])), wid) * min(
            min(abs(range_r2[1] - range_r1[3]), abs(range_r2[3] - range_r1[1])), hei)
    return area

def IsOverlapped(rect_1, rect_2):
    '''
    Identify whether two rectangles overlap
    '''
    range_r1 = [rect_1.xy[0], rect_1.xy[1], rect_1.xy[0] +
                rect_1._width, rect_1.xy[1] + rect_1._height]
    range_r2 = [rect_2.xy[0], rect_2.xy[1], rect_2.xy[0] +
                rect_2._width, rect_2.xy[1] + rect_2._height]

    if range_r2[0] > range_r1[2] or range_r2[2] < range_r1[0] or range_r2[1] > range_r1[3] or range_r2[3] < range_r1[1]:
        return False
    else:
        return True

def get_id_moved(i,j,point_list):
    '''
    based on the two possible point index i and j, get the one should be moved
    '''
    if point_list[i].priority==point_list[j].priority:
        if point_list[i].credit==point_list[j].credit:
            # select Ai Aj randomly
            # id_moved=random.choice([i,j]) 
            id_moved=j
        else:
            if point_list[i].credit>point_list[j].credit:
                id_moved=j
            else:
                id_moved=i
    else:
        if point_list[i].priority>point_list[j].priority:
            id_moved=j
        else:
            id_moved=i
    return id_moved

def move_label_position(id_moved,point_list,BalKdTree,range_axe):
    '''
    According to the id of point label position to be moved, move the label position
    Then, if new label is overlapped with a feature or map boundary, move again
    '''
    found=[]
    # based on the id of point label position needed to be moved, conduct moving
    if point_list[id_moved].LabelPos!=8:
        point_list[id_moved].LabelPos+=1 
        point_list[id_moved].credit+=1

        # overlapped with feature or map boundary
        rect_temp=get_rect(point_list[id_moved])
        rect=[[rect_temp._x,rect_temp._x+rect_temp._width],[rect_temp._y,rect_temp._y+rect_temp._height]]
        range_query_orthogonal(BalKdTree, rect, found)

        # if there are points in the rectangle or the rectangleis outside the map region
        if point_list[id_moved].LabelPos!=8 and \
            (len(found)>0 or rect[0][0]<range_axe[0] or rect[0][1]>range_axe[1] or rect[1][0]<range_axe[2] or rect[1][1]>range_axe[3]):
        
            point_list[id_moved].LabelPos+=1 
            point_list[id_moved].credit+=1


# sum up the weights of all agents and calculate the overlapping area
def get_TotalWeiAre(point_list):
    total_weight=0
    total_overlap_area=0
    # based on the new point list acquire the new rectangle list
    label_rect_list=get_rect_list(point_list) 
    
    for p in point_list:
        total_weight+=(9-p.LabelPos)
    for rect1 in label_rect_list:
        for rect2 in label_rect_list:
            if rect1==rect2:
                continue
            area=OverlapArea(rect1,rect2)
            total_overlap_area+=area
    return total_weight, total_overlap_area

# def OverlapWithFeature():

def get_better_position(index, point_list,BalKdTree,range_axe):
    '''
    try whether get back to more desirable position for only one point
    return a new point
    '''
    num_points=len(point_list)
    pos=point_list[index].LabelPos
    if point_list[index].LabelPos>1:
        # isoverlap = 0
        for i in range(1,point_list[index].LabelPos):
            isoverlap = 0
            point_temp = copy.deepcopy(point_list[index])
            point_temp.LabelPos = i
            rect1 = get_rect(point_temp)
            found=[]
            # overlapped with feature or map boundary
            rect=[[rect1._x,rect1._x+rect1._width],[rect1._y,rect1._y+rect1._height]]
            if rect[0][0]<range_axe[0] or rect[0][1]>range_axe[1] or rect[1][0]<range_axe[2] or rect[1][1]>range_axe[3]:
                continue

            range_query_orthogonal(BalKdTree, rect, found)
            if len(found)>0:
                continue

            # check whether the desirable label overlapped with other label
            for j in range(num_points):
                if i==j:
                    continue
                rect2=get_rect(point_list[j])
                if IsOverlapped(rect1,rect2):
                    isoverlap=1
                    break
            
            if isoverlap==0:
                point_list[index].LabelPos=i
                point_list[index].credit-=1
                break
    # return point
            
                

# try whether get back to more desirable position
def get_better_position_list(point_list, BalKdTree):
    '''
    try whether get back to more desirable position for a list of points
    Here, if the arguments in a function is a list,
    the arguments will transfer the address of the list
    '''
    num_points=len(point_list)
    for i in range(num_points):
        if point_list[i].LabelPos>1:
            isoverlap = 0
            point_temp = copy.deepcopy(point_list[i])
            point_temp.LabelPos = point_temp.LabelPos-1
            rect1 = get_rect(point_temp)
            for j in range(num_points):
                if i==j:
                    continue
                rect2=get_rect(point_list[j])

                found=[]
                # overlapped with feature or map boundary
                rect=[[rect1._x,rect1._x+rect1._width],[rect1._y,rect1._y+rect1._height]]
                range_query_orthogonal(BalKdTree, rect, found)

                if IsOverlapped(rect1,rect2):
                    isoverlap=1
                    break
            if isoverlap==1 or len(found)>0:
                break
            else:
                point_list[i].LabelPos-=1 
                point_list[i].credit-=1

class point_label():
    '''
    A class for point labels in Cartesian coordinate systems
    including the coordinate of left-lower point of the label
    How to calculate the size of label based on the text
    '''

    def __init__(self, x=None, y=None, width=None, length=None, text=None, point=None):
        self.x = x
        self.y = y
        # consider how to calculate the size of label based on the text
        self.width = width
        self.length = length
        self.point = point
        self.text = text

    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        elif i == 2:
            return self.text
        elif i == 3:
            return self.point
        return None

    def __eq__(self, other):
        if isinstance(other, point_label):
            return self.x == other.x and self.y == other.y and self.text == other.text
        return NotImplemented

    def isvalid(self):
        if not isinstance(self.x, (int, float)) or not isinstance(self.y, (int, float)):
            return False
        return True

    def distance(self, other):
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
