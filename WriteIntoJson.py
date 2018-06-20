'''
Point Labeling Experiment Main Process
package geom and indexing is from Ningchuan xiao(cxiao@gmail.com)
'''
import sys
sys.path.append("E:\\pylibs")
from geom.point import *
from pointlabeling.SimPointExperiment import *
import pickle

label_list=['Adams','Allen','Ashland','Ashtabula','Athens',\
            'Auglaize','Belmont','Brown','Butler','Carroll','Champaign',\
            'Clark','Clermont','Clinton','Columbiana','Coshocton','Crawford',\
            'Cuyahoga','Darke','Defiance','Delaware','Erie','Fairfield','Fayette',\
            'Franklin','Fulton','Gallia','Geauga','Greene','Guernsey','Hamilton',\
            'Hancock','Hardin','Harrison','Henry','Highland','Hocking','Holmes','Huron',\
            'Jackson','Jefferson','Knox','Lake','Lawrence','Licking','Logan','Lorain','Lucas','Madison','Mahoning']

num_points=len(label_list)

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

# create a list for each point feature
point_gjson_list=[]
for point in point_list:
    dic={
        "type":
    }


