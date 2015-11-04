from scipy import misc
from os import listdir
from os.path import join
import matplotlib.pyplot as plt
import numpy as np
from convolutional_mlp import evaluate_lenet5
from logistic_sgd import load_data, shared_dataset

def createDataSet():
    dir = r'C:\Users\ohad\Pictures\trafficLight'
    #files = [join(dir,f) for f in listdir(dir) if 'X_3' in f]
    files = [join(dir,f) for f in listdir(dir)]
    print files
    
    target = [x.split('X')[1].split('.')[0][1:] for x in files]
    print target
    
    files_data = zip(files,target)
    print files_data
    
    
    def getArrFromFile(f):
        print 'getting pixels from:',f
        bla = misc.imread(f)
        bla2=bla[::5,::5,:]
        print bla2.shape
        return bla2.ravel()
    
    N = getArrFromFile(files_data[0][0]).shape[0]
    print 'number of features:',N
    dataset = np.zeros((len(files_data),N+1))
    
    print 'dataset shape:', dataset.shape
    
    for n in xrange(len(files_data)):
        dataset[n, 0:N] = getArrFromFile(files_data[n][0])
        dataset[n, N] = files_data[n][1]
    
    return dataset
    
dataset = createDataSet()
#outputFile = "c:\\temp\\foo.csv"
#np.savetxt(outputFile, np.asarray(dataset), delimiter=",", fmt='%d')

def getFormattedDataSet(dataset):
    
    train_set = (dataset[0:10, :-1], dataset[0:10, -1])
    valid_set = (dataset[10:14, :-1], dataset[10:14, -1])
    test_set = (dataset[14:19, :-1], dataset[14:19, -1])
    
    train_set_x, train_set_y = shared_dataset(train_set)
    valid_set_x, valid_set_y = shared_dataset(valid_set)
    test_set_x, test_set_y = shared_dataset(test_set)
    
    rval = [(train_set_x, train_set_y), (valid_set_x, valid_set_y),
            (test_set_x, test_set_y)]
    return rval


evaluate_lenet5(getFormattedDataSet(dataset), learning_rate=0.01)


#plt.imshow(bla2, cmap=plt.cm.gray)
#l = misc.lena()
#plt.show()


