#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import cv2
import numpy as np
from scipy.optimize import fmin
class Analyser():
    def __init__(self,jpgname,title="Zeeman Effet"):
        self.jpgname=jpgname
        self.title=title
        
        self.img=cv2.imread(self.jpgname)
        print("opened img %s\nshape %s"%(self.jpgname,self.img.shape))
        
        self.ptstack=[[]]
        self.colorsalt=[0]
        self.circle=[[],]
        
        cv2.namedWindow(self.title)
        cv2.setMouseCallback(self.title,self.mouse)
        
        self.printhelp()
        self.main()
    def printhelp(self):
        print("left click to choose a point")
        print("use wasd to adjust the last point")
        print("use c to change color; esc to quit")
        print("press backspace to delete the latest point")
        print("press enter to finish temporary circle and show fit data")
        print("fit data will be displayed in the form: center(x,y) axis(a,b) rotate_angle")
    def mouse(self,event,x,y,flags,param):
        if event==cv2.EVENT_LBUTTONDOWN:
            #print("left click (%d,%d),%s,%s"%(x,y,flags,param))
            self.ptstack[-1].append([x,y])
            if len(self.ptstack[-1])>=5:
                self.fitC()
    def gencolor(self,sth,sth2):
        h=hash(str(sth)+str(sth2))
        r=h%256
        g=int(h/1000)%256
        b=int(h/1000000)%256
        return (r,g,b)
    def getpts(self):
        for i in range(len(self.ptstack)):
            try:
                c=self.gencolor(self.ptstack[i][0],self.colorsalt[i])
            except IndexError:
                c=(0,0,0)
            for j in self.ptstack[i]:
                yield j,c
    def getcircles(self):
        for i in range(len(self.circle)):
            if len(self.circle[i])==0:
                continue
            try:
                color=self.gencolor(self.ptstack[i][0],self.colorsalt[i])
            except IndexError:
                color=(0,0,0)
            j=[int(j) for j in self.circle[i]]
            yield (j[0],j[1]),(j[2],j[3]),j[4],color
    def show(self):
        a=2
        b=1
        img_show=self.img.copy()
        for pt,c in self.getpts():
            #cv2.circle(img_show,tuple(pt),1,c,-1)
            cv2.line(img_show,(pt[0]+a,pt[1]+a),(pt[0]-a,pt[1]-a),c,b)
            cv2.line(img_show,(pt[0]-a,pt[1]+a),(pt[0]+a,pt[1]-a),c,b)
        for center,axes,ang,color in self.getcircles():
            cv2.ellipse(img_show,center,axes,ang,0,360,color,b) 
        cv2.imshow(self.title,img_show)
    def movept(self,k):
        try:
            assert len(self.ptstack[-1][-1])==2
        except IndexError:
            return
        if k in (119,): #w
            self.ptstack[-1][-1][1]-=1
        elif k in (97,): #a
            self.ptstack[-1][-1][0]-=1
        elif k in (115,): #s
            self.ptstack[-1][-1][1]+=1
        elif k in (100,): #d
            self.ptstack[-1][-1][0]+=1
        elif k in (8,): #backspace
            self.ptstack[-1].pop()
        if len(self.ptstack[-1])>=5:
            self.fitC()
    def f_bias(self,x,pt):
        ptx=pt[0]*np.cos(np.deg2rad(x[4]))+pt[1]*np.sin(np.deg2rad(x[4]))
        pty=pt[1]*np.cos(np.deg2rad(x[4]))-pt[0]*np.sin(np.deg2rad(x[4]))
        return abs((ptx-x[0])**2/x[2]**2+(pty-x[1])**2/x[3]**2-1)
    def f_meanbias(self,x): # x: cx,cy,radius
        bias=[self.f_bias(x,pt) for pt in self.ptstack[-1]]
        return np.mean(bias)
    def f_guessinit(self):
        xys=list(zip(*self.ptstack[-1]))
        xs=xys[0];ys=xys[1];cx=np.mean(xs);cy=np.mean(ys)
        r=np.mean((np.std(xs),np.std(ys)))
        return np.array([cx,cy,r,r,0])
    def fitC(self,disp=False):
        r=fmin(self.f_meanbias,self.f_guessinit(),disp=False)
        res=self.f_meanbias(r)
        self.circle[-1]=list(r)
        if disp==True:
            print("get fit result (%.2f,%.2f) (%.2f,%.2f) (%.1f)"%(tuple(r)))
            print("with res %.2e of %d points"%(res,len(self.ptstack[-1])))
            avgr=np.mean(r[2:4])
            print("mean radius %.1f a/b %.2f r^2 %.1f"%(avgr,r[2]/r[3],avgr**2))
    def main(self):
        while(1):
            self.show()
            k=cv2.waitKey(40)&0xFF
            if k in (119,97,115,100,8): #wasd
                self.movept(k)
            elif k==99: #c
                self.colorsalt[-1]+=1
            elif k==27: #ESC
                print("quitting")
                break
            elif k==13: #enter
                self.fitC(disp=True)
                self.ptstack.append([])
                self.colorsalt.append(0)
                self.circle.append([])
            elif k<255: #255 is empty
                pass
                #print("unknown key: %d"%(k))
        cv2.destroyAllWindows()
if __name__=="__main__":
    a=Analyser("./20190604/pp_data/r-pp-41.JPG")
        
