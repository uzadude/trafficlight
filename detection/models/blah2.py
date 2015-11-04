from os import listdir
from os.path import join
from scipy import misc

import matplotlib.pyplot as plt
import numpy as np


dir = r'../imgs'
#files = [join(dir,f) for f in listdir(dir) if 'X_3' in f]
files = [join(dir,f) for f in listdir(dir)]
print files

target = [x.split('X')[1].split('.')[0][1:] for x in files]
print target

files_data = zip(files,target)
print files_data
    
    
bla = misc.imread(files_data[0][0])
    


#plt.imshow(bla2, cmap=plt.cm.gray)
#l = misc.lena()
#plt.show()


