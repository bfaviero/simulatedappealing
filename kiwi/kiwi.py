# interface to the kiwi module
# written by Shariq

import os
import time
import requests

CNN_API_URL = 'http://ec2-54-146-245-15.compute-1.amazonaws.com:8080/'
KIWI_DIRECTORY = '.'
# ends with / !!!

for fn in os.listdir(KIWI_DIRECTORY):
 if '_bounding' in fn:
  os.system('rm '+KIWI_DIRECTORY + '/' + fn)

def classifyImage(path):
 r = requests.post(CNN_API_URL, files={'image.jpg': open(path, 'rb')})
 print 'got '+r.text
 return [' ','0','1','2','3','4','5','6','7','8','9','x','y','e','A','B','C','D','E','F','G','H','O','J'][int(r.text)]

def newBox(bounding = [(0,0,100,100),(100,0,200,100),(200,0,300,100)]):
 print bounding
 open(KIWI_DIRECTORY+'/thingy_bounding', 'w').write('\n'.join([' '.join(map(str,x)) for x in bounding]))
 os.system(KIWI_DIRECTORY+'/bin/webcam &')
 while True:
  time.sleep(0.1)
  for fn in os.listdir(KIWI_DIRECTORY):
   if 'thingy' in fn and 'bounding.jpg' in fn:
    try:
     results = classifyImage(KIWI_DIRECTORY + '/' + fn)
     return (int(fn.replace('_bounding.jpg','').split('_')[-1]),results)
    except:
     print 'errooooor'
    finally:
     os.system('rm '+KIWI_DIRECTORY+'/thingy_bounding')
     os.system('rm '+KIWI_DIRECTORY+'/'+fn)
