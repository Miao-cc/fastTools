import sys
import math
import ephem
import datetime as dt
from telescope import *
from astropy.time import Time
from astropy.coordinates import SkyCoord
from astropy import units as u
from datetime import datetime

#----------------------------------------------
#get survey point
#return the FAST pointing in survey mode
class survey:
    '''
    call:
    a = survey(TimeMJD = '', decJ2000 = '')
    survey.MJDtransit():
    survey.surveyPoint():
    '''
    def __init__(self, TimeMJD = '', decJ2000 = ''):
        self.TimeMJD = TimeMJD
        self.decJ2000 = decJ2000

    def MJDtransit(self):
        # Transfer Fits header MJD --> UTC time
        # return Starttime_utc, Starttime_BJ
        TimeMJD = self.TimeMJD
        t_header = Time(TimeMJD,format='mjd',scale='utc')
        tmp_t_header = str(t_header.datetime).split('.')
        if tmp_t_header.__len__() == 1:
                tmp_t_header[0] = tmp_t_header[0] + '.000001'
        else:
                tmp_t_header[0] = tmp_t_header[0] + '.' + tmp_t_header[1]
        Starttime_utc = datetime.strptime(tmp_t_header[0],"%Y-%m-%d %H:%M:%S.%f")
        Starttime_BJ = Starttime_utc + dt.timedelta(hours=8)
        return Starttime_utc, Starttime_BJ
    
    
    def surveyPoint(self):
        #input parameters
        TimeMJD = self.TimeMJD 
        decJ2000 = self.decJ2000
    
        src = ephem.FixedBody()
        src._ra = '00:00:00'            # Epoch J2000
        src._dec = decJ2000
        
        # Transfer Fits header MJD --> UTC time
        Starttime_utc, Starttime_BJ = self.MJDtransit()
    
        #use telescope FAST
        Dawodang = fast(str(Starttime_utc).split(' ')[0])
        
    
        # Calculate transit time
        src.compute()
        ttrans=Dawodang.next_transit(src)
    
        # Get FAST az and el
        FAST_az = 90.- float(src.alt)*360./2/math.pi
        FAST_el = 270.- float(src.az)*360./2/math.pi
    
        #transit localtime(UTC+8) to UTC time(UTC+0)
        t_transit = Time(ephem.localtime(ttrans),scale='utc')
    
        # Compensate start time & transit time
        # transit time module time format to datetime module time format
        Transit_utc = datetime.strptime(str(t_transit),"%Y-%m-%d %H:%M:%S.%f")
        Delta = Transit_utc - Starttime_utc
        Offset_sec = 236 * float(Delta.seconds)/24./3600.   # compensate periodical delay and modify start_time to beam centre 
        
        Delta_final = Delta + dt.timedelta(seconds = Offset_sec)
        #print 'Delta time after offset =', Delta_final
        
        #H24_date = (str(Starttime_utc).split(' ')[0]).split('-')
        #H24 = dt.datetime(int(H24_date[0]), int(H24_date[1]), int(H24_date[2]), 23, 59, 59)
        H24 = dt.datetime(Starttime_utc.year, Starttime_utc.month, Starttime_utc.day, 23, 59, 59)
        RaJ = H24 - (Delta_final - dt.timedelta(seconds = 3600*8+1))
        
        src._ra =  RaJ.strftime("%H:%M:%S.%f")
        src.compute()
        dtrans=Dawodang.next_transit(src)
        
        Dtransit = str(Time(ephem.localtime(dtrans),scale='utc')).split('.')
    
        if (Dtransit.__len__()==1):
            Dtransit[0]=Dtransit[0]+'.000001'
        else:
            Dtransit[0]=Dtransit[0]+'.'+Dtransit[1]
        d_transit = datetime.strptime(Dtransit[0],"%Y-%m-%d %H:%M:%S.%f")
        Delta_ra = Starttime_BJ - d_transit
        RaJ += Delta_ra
        
        # transit Ra,Dec to degrees
    
        src._ra = str(RaJ).split(' ')[1]
        RaJ_deg  = '%.12f' % (float(src._ra)*360./2/math.pi)
        DecJ_deg = '%.12f' % (float(src._dec)*360./2/math.pi)
    
        #print '\n', 'Ra(J2000) =', str(RaJ).split(' ')[1],  '  Dec(J2000) =',  decJ2000
        #print '\n', 'Ra(deg) =', RaJ_deg, '  Dec(deg) =', DecJ_deg
        return src._ra, src._dec, str(Starttime_BJ)


