import ephem
import datetime


#---------------------------------------------------
#Telescope address
#define different telescopes. Parkes, FAST and effersberg
'''
call
obs_date = "2018/8/16 18:24:59"
fast = telescope.fast()
fast = telescope.fast(obsData = obs_date)
lsttime = otelescope.bs_lst(fast, obs_date):
'''

def parkes(obsData = str(datetime.datetime.now())):
    parkes           = ephem.Observer()
   # parkes.lon       = '148:15:47' 
   # parkes.lat       = '-32:59:52'
   # parkes.horizon   = '30.25'
   # parkes.lon       = '148:15:48.636' 
   # parkes.lat       = '-32:59:54.263'   
    parkes.lon       = '148:15:49' 
    parkes.lat       = '-32:59:55'    
    parkes.horizon   = '30.5'
    parkes.pressure  = 0 
    parkes.elevation = 414.8
    parkes.date      = obsData
    parkes.epoch     = '2000'
    return parkes

def fast(obsData = str(datetime.datetime.now())):
    fast           = ephem.Observer()
    fast.lon       = '106.856594' 
    fast.lat       = '25.652939'
    fast.horizon   = '-18'
    fast.pressure  = 0 
    fast.date      = obsData
    return fast 

def effelsberg(obsData = str(datetime.datetime.now())):
    effelsberg           = ephem.Observer()
    effelsberg.lon       = '6.88361'
    effelsberg.lat       = '50.52483'
    effelsberg.horizon   = '+8:06'
    effelsberg.pressure  = 0
    effelsberg.date      = obsData
    return effelsberg


  #obs(rise_time)
  #rise_lst=obs.sidereal_time()
  #out put sidereal time
def obs_lst(obs, obsData):
    rise_set_time = obsData
    obs.date=rise_set_time
    return obs.sidereal_time()

