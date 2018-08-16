#from beam import *
import beam
import fastPoint
import ephem

TimeMJD = 58313.54211672340109
Beam1 = ephem.FixedBody()
Beam1._ra = '19:50:26.81'
Beam1._dec = '-12:30:56.78'
source = ephem.FixedBody()
source._ra = '19:50:26.81'
source._dec = '-12:30:56.78'


b =  beam.beam.__doc__
print b

Beam = beam.beam(0.4, Beam1, MJDTime = TimeMJD, sourcePoint = source, picname='plot')

print Beam.rotateAngel

print Beam.beamDiameter

print Beam.beam1._ra
print Beam.beam1._dec


for key in Beam.beamPositionRead():
    print Beam.beamPositionRead()[key]

print Beam.relativePosition()

#Beam.plotbeam()

fastsurvey = fastPoint.survey(TimeMJD, source._dec)
print source._dec
print fastsurvey.MJDtransit()
print fastsurvey.surveyPoint()
