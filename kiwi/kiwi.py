# interface to the kiwi module
# written by Shariq

import os
import time

KIWI_DIRECTORY = '../kiwi/bin/'
# ends with / !!!

os.system(KIWI_DIRECTORY+'webcam &')

def classifyImage(path):
 print 'NOT IMPLEMENTED YET! TODO'
 return 0

def newBox(bounding = [(0,0,100,100)]):
 open(KIWI_DIRECTORY+'thingy_bounding', 'w').write('\n'.join([' '.join(x) for x in bounding]))
 while True:
  time.sleep(0.1)
  for fn in os.listdir(KIWI_DIRECTORY):
   if 'bounding.jpg' in fn:
    return (int(fn.replace('_bounding.jpg','').split('_')[-1]),classifyImage(KIWI_DIRECTORY + fn))
