#from beam import *
from fastTools import beam, fastPoint
import ephem

TimeMJD = 58313.54211672340109
Beam1 = ephem.FixedBody()
Beam1._ra = '19:50:26.81'
Beam1._dec = '-12:30:56.78'
source = ephem.FixedBody()
source._ra = '19:50:26.81'
source._dec = '-12:20:56.78'


#call beam function
Beam = beam.beam(0.4, Beam1, MJDTime = TimeMJD, sourcePoint = source, picname='plot')

print "--------------------------------------------------------------------------------"
print "Beam = beam.beam(0.4, Beam1, MJDTime = TimeMJD, sourcePoint = source, picname='plot')"
print "Beam.rotateAngel: "
print "Rotation angel of beam is %s (rad)" %(Beam.rotateAngel)
print "--------------------------------------------------------------------------------"
print "Beam.beamDiameter"
print "beam Diameter(arcmin): ", Beam.beamDiameter
print "--------------------------------------------------------------------------------"
print "Beam.beam1._ra"
print "Beam1 pointing (RA): ", Beam.beam1._ra
print "--------------------------------------------------------------------------------"
print "Beam.beam1._dec"
print "Beam1 pointing (RA): ", Beam.beam1._dec

print "--------------------------------------------------------------------------------"
print "relative position of the beams (angel = 0):"
for key in Beam.beamPositionRead():
    print key, Beam.beamPositionRead()[key]

print "--------------------------------------------------------------------------------"
print "Beam.relativePosition()"
print "relative position of the beams (angel = 0.4):"
print Beam.relativePosition()

print "--------------------------------------------------------------------------------"
print "Beam.plotbeam()"
print "plot the relative position of beams and source"
Beam.plotbeam()

print "--------------------------------------------------------------------------------"
Beam = beam.beam(0.4, Beam1, MJDTime = TimeMJD, sourcePoint = source, picname='plot.png')
print "Beam = beam.beam(0.4, Beam1, MJDTime = TimeMJD, sourcePoint = source, picname='plot.png')"
print "Beam.plotbeam()"
print "save png to the pic plot.png"
Beam.plotbeam()



fastsurvey = fastPoint.survey(TimeMJD, source._dec)

print "--------------------------------------------------------------------------------"
print "fastsurvey = fastPoint.survey(TimeMJD, source._dec)"
print "beam1 pointing (DEC): ", source._dec
print "--------------------------------------------------------------------------------"
print "fastsurvey.MJDtransit()"
print "transit the input MJD to BJ time",fastsurvey.MJDtransit()
print "--------------------------------------------------------------------------------"
print "calculate the pointing of the beam1 in %s when point the DEC: %s." %( TimeMJD, source._dec)
print "--------------------------------------------------------------------------------"
potinRA, pointDec, pointBJTime = fastsurvey.surveyPoint()
print "potinRA, pointDec, pointBJTime = fastsurvey.surveyPoint()"
print "Point RA: %s DEC: %s when %s" %(potinRA, pointDec, pointBJTime)
print "Point RA: %s DEC: %s when %s" %(potinRA, pointDec, pointBJTime)

a = fastPoint.survey(TimeMJD = '58313.7173714', decJ2000 = '-12:30:56.8')j

print a.decJ2000
print a.TimeMJD
print a.MJDtransit()
print a.surveyPoint()

