import sys
import os
import ephem
import math
import datetime as dt
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from astropy.time import Time
from astropy.coordinates import SkyCoord
from astropy import units as u
from datetime import datetime
from itertools import islice  



class position:
    '''
    call
    def __init__(self, RotateAngel , beam1Point, MJDTime = '', sourcePoint = '', picname = ''):
    a = fastTools.beam.beamPositionRead()
    a = fastTools.beam.beamPositionRead()



    '''
    def __init__(self, RotateAngel):
        self.rotateAngel = RotateAngel

    #read beam info and return the relative position in rotate angel 0
    def beamPositionRead(self):
        current_path = os.path.dirname(__file__)
        filename = current_path+'/beamPosition.txt'
        beam = open(filename,'r')
        position = {}
        for line in islice(beam, 1, None):
            beamtmp = line.strip().split()
            beamtmp[1] = float(beamtmp[1])
            beamtmp[2] = float(beamtmp[2])
            position.update({beamtmp[0]: beamtmp[1:]})
        beam.close()
        return position 
    
    #return the relative position in input rotate angel
    def relativePosition(self):
        RotateAngel = self.rotateAngel
        beamposition = self.beamPositionRead()
        for i in range(1,20):
            key = 'beam'+str(i)
            position = beamposition[key]
            #change to polar coordinates
            if (position[0] != 0) :
                length = np.sqrt(position[0]**2 + position[1]**2)
                beamAngel = math.atan( position[1]/position[0])
                if (beamAngel < 0): 
                    if (position[1] > 0):
                        beamAngel = beamAngel + 1*math.pi
                    else :
                        beamAngel = beamAngel + 2*math.pi
                else:
                    if (position[0] > 0): 
                        beamAngel = beamAngel + 0*math.pi
                    else :
                        beamAngel = beamAngel + 1*math.pi
            else : 
                if (position[1] > 0):
                    length = np.sqrt(position[0]**2 + position[1]**2)
                    beamAngel = math.pi/2.+ 0*math.pi
                elif (position[1] < 0):
                    length = np.sqrt(position[0]**2 + position[1]**2)
                    beamAngel = math.pi/2.+ 1*math.pi
                else:
                    length = 0
                    beamAngel = 0
            beamposition[key] = [round(length*math.cos(RotateAngel+beamAngel),3), round(length*math.sin(RotateAngel+beamAngel), 3)]
        return beamposition




class plotpic(position):
#class plotpic:
    def __init__(self, RotateAngel, beam1Point, MJDTime, sourcePoint, picname): 
        position.__init__(self, RotateAngel)
        self.BJTime = MJDTime
        self.beam1RA = beam1Point._ra
        self.beam1DEC = beam1Point._dec
        self.RotateAngel = RotateAngel
        self.picname = picname
        self.sourcePoint = sourcePoint

    #def plotbeam(self, RotateAngel, beam1Point, MJDTime, sourcePoint, picname):
    def plotbeam(self):

        from matplotlib.patches import Circle
        #get rotate angel  
        Beam = self.relativePosition()
        BJTime      = self.BJTime 
        beam1RA     = self.beam1RA 
        beam1DEC    = self.beam1DEC 
        RotateAngel = self.RotateAngel
        picname     = self.picname 
        sourcePoint = self.sourcePoint
        if (sourcePoint != ''):
            sourceRA = sourcePoint._ra
            sourceDEC = sourcePoint._dec
        else:
            sourceRA = ''
            sourceDEC = ''


        if (BJTime == ''):
            BJTime = 'Time now:\n' + str(dt.datetime.now())[:-7]
        else :
            BJTime = 'survey Time:\n'+ str(BJTime)
    
        #plot parameter
        legendList = []
        legendWordList = []
        #plot colors
        colorname = [name for name in plt.get_cmap('tab20').colors]
    
        fig = plt.figure(figsize=(15.0, 15.0),dpi = 80)
        ax = fig.add_subplot(111)
    
        for i in range(1,20):
            key = 'beam'+str(i)
            position = Beam[key]
            #draw circle, using the polar angel and length
            cirl = Circle(xy = (position[0], position[1]), radius = 1.5, alpha=1., color = colorname[i])
            ax.annotate(str(i),xy=(position[0], position[1]),xytext=(0,0),textcoords='offset points')
            ax.add_patch(cirl)
            legendList.append(cirl)
            legendWordList.append(key)
    
        #for rotate angel 
        plottext = 'roation angle %s$^\circ$' %(round(RotateAngel*360./2/math.pi, 3))
        if (RotateAngel >= 0 ) :
            plt.annotate(plottext, xy=(15, -5), xycoords='data', xytext=(10, -10), textcoords='data', fontsize=12, arrowprops=dict(arrowstyle="->",connectionstyle="arc3,rad=.2"))  
        elif (RotateAngel < 0) :
            plt.annotate(plottext, xy=(15, -5), xycoords='data', xytext=(10, -10), textcoords='data', fontsize=12, arrowprops=dict(arrowstyle="<-",connectionstyle="arc3,rad=.2"))  
    
        # text 
        #plt.annotate("Beam 1\nRA: %s\nDEC: %s" % (ra, dec), xy=(8,-13))
    
        bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
        if (sourceRA != ''):
            plt.text(0, -17, "Beam 1: RA : %s  DEC: %s\nsource: RA : %s  DEC: %s\n%s" % (beam1RA, beam1DEC, sourceRA, sourceDEC, BJTime), ha="center", va="center", size=15,bbox=bbox_props)
            #plt.text(-13, -12, "" % (), ha="center", va="center", size=15,bbox=bbox_props)
            
            beam1 = ephem.FixedBody()
            beam1._ra = beam1RA           # Epoch J2000
            beam1._dec = beam1DEC            # Epoch J2000
            source = ephem.FixedBody()
            source._ra = sourceRA            # Epoch J2000
            source._dec = sourceDEC            # Epoch J2000
            beamRaJ_deg  = (float(beam1._ra)*360./2./math.pi)
            beamDecJ_deg  = (float(beam1._dec)*360./2./math.pi)
            sourceRaJ_deg  = (float(source._ra)*360./2./math.pi)
            sourceDecJ_deg  = (float(source._dec)*360./2./math.pi)
    
            print beam1._ra, beam1._dec
            print source._ra, source._dec
            print beamRaJ_deg, beamDecJ_deg
            print sourceRaJ_deg, sourceDecJ_deg
            
            sourceOffSet = [(sourceRaJ_deg-beamRaJ_deg)*60/15., (sourceDecJ_deg-beamDecJ_deg)*60.]
            print sourceOffSet
             
            cirl = Circle(xy = (sourceOffSet[0], sourceOffSet[1]), radius = 0.2, alpha=1., color = colorname[0])
            ax.annotate('source',xy=(sourceOffSet[0], sourceOffSet[1]),xytext=(0,0),textcoords='offset points')
            ax.add_patch(cirl)
        else : 
            plt.text(0, -17, "Beam 1: RA : %s DEC: %s\n%s" % (beam1RA, beam1DEC,  BJTime), ha="center", va="center", size=15,bbox=bbox_props)
    
        #
    
        plt.annotate('S', xy=(-15,13),xytext=(-15,17),arrowprops=dict(facecolor='black'),horizontalalignment='left', verticalalignment='top')
        plt.annotate('W', xy=(-13,15),xytext=(-17,15),arrowprops=dict(facecolor='black'),horizontalalignment='left', verticalalignment='top')
    
    
        #plt.legend(handles=legendList,labels=legendWordList,loc='best')
        plt.legend(handles=legendList,labels=legendWordList,loc='upper right', ncol = 5)
        plt.grid(True)
        plt.axis('scaled')
        plt.axis([-20,20,-20,20])
        plt.xlabel("RA offset (arcmin)")# plots an axis lable
        plt.ylabel("DEC offset (arcmin)") 
        plt.title("beam position",fontsize = "20")
        if (picname == 'plot'):
            plt.show()
        elif(picname == ''):
            plt.cla()
            plt.close(fig)
        else :
            plt.savefig(picname,dpi = 100)
            plt.cla()
            plt.close(fig)
    
    
class beam(plotpic, position):
    '''
    call func
    Beam = beam(RotateAngel, beam1Point, [MJDTime = '', sourcePoint = '', picname = ''])
    sourcePoint and beam1Point should in ephem format
    optinal parameters: MJDTime = '', sourcePoint = '', picname = ''
    if input [picname ='plot'], it will plot the pic to the screen
    if input [picname ='plot.png'], it will plot the pic to the file
    if input [picname =''], it will not plot the pic.
    self.rotateAngel 
    self.beamDiameter 
    self.beam1 
    fun:
    self.beamPositionRead()
    self.relativePosition()

    '''
    def __init__(self, RotateAngel , beam1Point, MJDTime = '', sourcePoint = '', picname = ''):
        position.__init__(self, RotateAngel)
        plotpic.__init__(self, RotateAngel , beam1Point, MJDTime, sourcePoint, picname)

        self.rotateAngel = RotateAngel
        self.beamDiameter = "3 arcmin"
        self.beam1 = beam1Point




