import zerorpc
import numpy as np
import cv2
from PIL import Image
import base64
from StringIO import StringIO

class RPCServer(object):
    def hello(self, imgData, name):
        nparr = np.fromstring(imgData, np.uint8)
        img = cv2.imdecode(nparr, 0)
        color_img = cv2.imdecode(nparr, 1)
        cv2.imwrite('./uploads/'+name, color_img)

        percent = 5.0
        w,h = img.shape
        cutoff = percent/100.0*w*h

        histSize = 256
        hist = cv2.calcHist([img],[0],None,[histSize],[0,256])
        areaoftops = 0;
        i = histSize - 1
        while i >= 0: 
            areaoftops += hist[i]
            if areaoftops > cutoff:
                break
            i-=1
        HI = i
        LO = .35*HI
        print "HI: " + str(HI) + ", LO: " + str(LO)
        edges = cv2.Canny(img,LO,HI)
        print color_img.shape
        h,w = img.shape
        for y in range(h):
            for x in range(w):
                if edges[y][x]:
                    color_img[y][x] = [0x00, 0xFF, 0x1E]

        output = StringIO()
        color_img = cv2.cvtColor(color_img,cv2.COLOR_BGR2RGB)
        
        ret = Image.fromarray(color_img, 'RGB')
        ret.save(output, format="JPEG")
        ret.save('./canny/'+name)
        
        contents = output.getvalue()
        b64img = base64.b64encode(contents)

        return b64img

s = zerorpc.Server(RPCServer())
s.bind("tcp://0.0.0.0:4242")
s.run()
