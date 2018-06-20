# write the information of points with labels into txt file for arcgis
# ID x y label
# 50 points in total

import sys
sys.path.append("E:\\pylibs")
import numpy as np
import pickle

label_list = ['Adams', 'Allen', 'Ashland', 'Ashtabula', 'Athens',
              'Auglaize', 'Belmont', 'Brown', 'Butler', 'Carroll', 'Champaign',
              'Clark', 'Clermont', 'Clinton', 'Columbiana', 'Coshocton', 'Crawford',
              'Cuyahoga', 'Darke', 'Defiance', 'Delaware', 'Erie', 'Fairfield', 'Fayette',
              'Franklin', 'Fulton', 'Gallia', 'Geauga', 'Greene', 'Guernsey', 'Hamilton',
              'Hancock', 'Hardin', 'Harrison', 'Henry', 'Highland', 'Hocking', 'Holmes', 'Huron',
              'Jackson', 'Jefferson', 'Knox', 'Lake', 'Lawrence', 'Licking', 'Logan', 'Lorain', 'Lucas', 'Madison', 'Mahoning']

# point_generate_random(num_points,num_pixel)
# coordinate range from 0 to 600
with open('x_list_file.pickle', 'rb') as file:
    x_list = pickle.load(file)
with open('y_list_file.pickle', 'rb') as file:
    y_list = pickle.load(file)

# write the data from pattern_price_list to txt file
file = open('E:\\pylibs\\pointlabeling\\Points_with_labels.txt', 'w')
file.write("ID" + "," + "X" +
               "," + "Y" + "," + "Label" + "\n")
for i in range(len(label_list)):
    file.write(str(i+1) + "," + str(x_list[i]) +
               "," + str(y_list[i]) + "," + label_list[i] + "\n")
file.close()
