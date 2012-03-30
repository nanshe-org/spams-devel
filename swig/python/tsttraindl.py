import sys, time
import numpy as np
from PIL import Image

import spams
#img = Image.open('tst2.png')
#I = np.array(img) / 1.
img = Image.open('../extdata/boat.png')
I = np.array(img) / 255.
if I.ndim == 3:
    A = np.asfortranarray(I.reshape((I.shape[0],I.shape[1] * I.shape[2])))
    rgb = True
else:
    A = np.asfortranarray(I)
    rgb = False

m = 8;n = 8;
#m = 2;n = 2;
X = spams.im2col_sliding(A,m,n,rgb)

X = X - np.tile(np.mean(X,0),(X.shape[0],1))
X = np.asfortranarray(X / np.tile(np.sqrt((X * X).sum(axis=0)),(X.shape[0],1)))
param = { 'K' : 100, # learns a dictionary with 100 elements
          'lambda' : 0.15, 'numThreads' : 4, 'batchsize' : 400,
          'iter' : 1000}

########## FIRST EXPERIMENT ###########
tic = time.time()
D = spams.TrainDL(X,param)
tac = time.time()
t = tac - tic
print 'time of computation for Dictionary Learning: %f' %t

##param['approx'] = 0
print 'Evaluating cost function...'
alpha = spams.Lasso(X,D,param)
xd = X - D * alpha
R = np.mean(0.5 * (xd * xd).sum(axis=0) + param['lambda'] * np.abs(alpha).sum(axis=0))
# display ????

print "objective function: %f" %R

#### SECOND EXPERIMENT ####
print "*********** SECOND EXPERIMENT ***********"

X1 = X[:,0:X.shape[1]/2]
X2 = X[:,X.shape[1]/2 -1:]
param['iter'] = 500
tic = time.time()
(D,model) = spams.TrainDL(X1,param,return_model = True)
tac = time.time()
t = tac - tic
print 'time of computation for Dictionary Learning: %f\n' %t
print 'Evaluating cost function...'
alpha = spams.Lasso(X,D,param)
xd = X - D * alpha
R = np.mean(0.5 * (xd * xd).sum(axis=0) + param['lambda'] * np.abs(alpha).sum(axis=0))
print "objective function: %f" %R

# Then reuse the learned model to retrain a few iterations more.
param2 = param
param2['D'] = D
tic = time.time()
(D,model) = spams.TrainDL(X2,param2,return_model = True,model = model)
tac = time.time()
t = tac - tic
print 'time of computation for Dictionary Learning: %f' %t
print 'Evaluating cost function...'
alpha = spams.Lasso(X,D,param)
xd = X - D * alpha
R = np.mean(0.5 * (xd * xd).sum(axis=0) + param['lambda'] * np.abs(alpha).sum(axis=0))
print "objective function: %f" %R

#################### THIRD & FOURTH EXPERIMENT ######################
# let us add sparsity to the dictionary itself

print '*********** THIRD EXPERIMENT ***********'
param['modeParam'] = 0
param['iter'] = 1000
param['gamma1'] = 0.3
param['modeD'] = 1

tic = time.time()
D = spams.TrainDL(X,param)
tac = time.time()
t = tac - tic
print 'time of computation for Dictionary Learning: %f' %t
print 'Evaluating cost function...'
alpha = spams.Lasso(X,D,param)
xd = X - D * alpha
R = np.mean(0.5 * (xd * xd).sum(axis=0) + param['lambda'] * np.abs(alpha).sum(axis=0))
print "objective function: %f" %R

# DISPLAY
print '*********** FOURTH EXPERIMENT ***********'
param['modeParam'] = 0
param['iter'] = 1000
param['gamma1'] = 0.3
param['modeD'] = 3

tic = time.time()
D = spams.TrainDL(X,param)
tac = time.time()
t = tac - tic
print 'time of computation for Dictionary Learning: %f' %t
print 'Evaluating cost function...'
alpha = spams.Lasso(X,D,param)
xd = X - D * alpha
R = np.mean(0.5 * (xd * xd).sum(axis=0) + param['lambda'] * np.abs(alpha).sum(axis=0))
print "objective function: %f" %R

############
img_file = '../extdata/portrait.png'
try:
    img = Image.open(img_file)
except:
    print "Cannot load image %s : skipping test" %img_file
    return None
I = np.array(img) / 255.
if I.ndim == 3:
    A = np.asfortranarray(I.reshape((I.shape[0],I.shape[1] * I.shape[2])))
    rgb = True
else:
    A = np.asfortranarray(I)
    rgb = False
    
m = 8;n = 8;
X = spams.im2col_sliding(A,m,n,rgb)

X = X - np.tile(np.mean(X,0),(X.shape[0],1))
X = np.asfortranarray(X / np.tile(np.sqrt((X * X).sum(axis=0)),(X.shape[0],1)))
X = np.asfortranarray(X[:,np.arange(0,X.shape[1],10)])

param = { 'K' : 200, # learns a dictionary with 100 elements
          'lambda' : 0.15, 'numThreads' : 4,
          'iter' : 100}
D = spams.TrainDL_Memory(X,param)