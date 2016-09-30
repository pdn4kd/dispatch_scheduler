"""
A collection of functions for plotting and visualization.
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import datetime
import ephem
import glob
import simbad_reader
#import ipdb
import math
import os

def singletarget(sim,target):
    pass

def get_sun(simpath):
    dt_fmt = '%Y-%m-dT%H:%M:%S'
    simname = simpath.split('/')[2]
    summ = np.genfromtxt(simpath+simname+'.txt',dtype=None,delimiter=': ')
    start = datetime.datetime.strptime(summ[1,1],dt_fmt)
    strrises = np.genfromtxt(simpath+'sunrise.txt',dtype=None)
    srises = [datetime.datetime.strptime(dstr,dt_fmt) for dstr in strrises]
    sr_days = []
    sr_times = []
    for srise in srises:
        sr_days.append((srise-start).days)
        ttime = srise.time()
        sr_times.append(ttime.hour+ttime.minute/60.+ttime.second/3600.)

    sr_days=np.array(sr_days)
    sr_times=np.array(sr_times)

    strsets = np.genfromtxt(simpath+'sunset.txt',dtype=None)
    ssets = [datetime.datetime.strptime(dstr,dt_fmt) for dstr in strsets]
    ss_days = []
    ss_times = []
    for sset in ssets:
        ss_days.append((sset-start).days)
        ttime = sset.time()
        ss_times.append(ttime.hour+ttime.minute/60.+ttime.second/3600.)
    ss_days=np.array(ss_days)
    ss_times=np.array(ss_times)
    return sr_days,sr_times,ss_days,ss_times

def get_targ_rise_set(simpath,targetname):
    dt_fmt = '%Y-%m-dT%H:%M:%S'
    simname = simpath.split('/')[2]
    summ = np.genfromtxt(simpath+simname+'.txt',dtype=None,delimiter=': ')
    start = datetime.datetime.strptime(summ[1,1],dt_fmt)
    strrises = np.genfromtxt(simpath+targetname+'rise.txt',dtype=None)
    srises = [datetime.datetime.strptime(dstr,dt_fmt) for dstr in strrises]
    sr_days = []
    sr_times = []
    for srise in srises:
        sr_days.append((srise-start).days)
        ttime = srise.time()
        sr_times.append(ttime.hour+ttime.minute/60.+ttime.second/3600.)

    sr_days=np.array(sr_days).astype(float)
    sr_times=np.array(sr_times)

    strsets = np.genfromtxt(simpath+targetname+'set.txt',dtype=None)
    ssets = [datetime.datetime.strptime(dstr,dt_fmt) for dstr in strsets]
    ss_days = []
    ss_times = []
    for sset in ssets:
        ss_days.append((sset-start).days)
        ttime = sset.time()
        ss_times.append(ttime.hour+ttime.minute/60.+ttime.second/3600.)
    ss_days=np.array(ss_days).astype(float)
    ss_times=np.array(ss_times)
    return sr_days,sr_times,ss_days,ss_times

def get_target(simpath,targetname):

    dt_fmt = '%Y-%m-dT%H:%M:%S'
    simname = simpath.split('/')[2]
    summ = np.genfromtxt(simpath+simname+'.txt',dtype=None,delimiter=': ')
    start = datetime.datetime.strptime(summ[1,1],dt_fmt)
    temp = np.genfromtxt(simpath+targetname+'.txt',names=True,dtype=None)
    start = datetime.datetime.strptime(summ[1,1],dt_fmt)
    obs = [datetime.datetime.strptime(dstr,dt_fmt) \
               for dstr in temp['obs_start']]
#    ipdb.set_trace()
    alts = temp['altitude']
    days = []
    times = []
    for obser in obs:
        days.append((obser-start).days)
        ttime = obser.time()
        times.append(ttime.hour+ttime.minute/60.+ttime.second/3600.)    

    days = np.array(days)
    times = np.array(times)
    return days,times,alts

def window_function(freqs,times):
    result = []
    for freq in freqs:
        result.append(np.sum(np.exp(-2j*np.pi*(1./freq)*times))/len(times))
    return result
    

def plot_target(simpath,target):
    
    sr_days,sr_times,ss_days,ss_times = get_sun(simpath)
    try:
        days,times,alts = get_target(simpath,target['name'])
        dec_times = days+times
    except:
        print('Bad pick, try again')
        return


    figt = plt.figure()#figsize=(11,6))
    ax2 = figt.add_subplot(2,1,2)
    freqs = np.linspace(0,365,100000)
    win_func = window_function(freqs,dec_times)
    plt.plot(freqs,np.absolute(win_func))
    ax1 = figt.add_subplot(2,1,1)
    ax1.plot(sr_days,sr_times,label='sun rises')
    ax1.plot(ss_days,ss_times,label='sun sets')

    """
    pltdays = []
    maxplt = []
    for ind in range(len(sr_times)):
        if sr_times[ind]>tr_times[ind] and tr_times[ind]>ts_times[ind]:
            pltdays.append(ind)
            maxplt.append(sr_times[ind])
        elif sr_times[ind]>tr_times[ind] and tr_times[ind]>ss_times[ind]:
            pltdays.append(ind)
            maxplt.append(sr_times[ind])
        elif ts_times[ind]<sr_times[ind] and ts_times[ind]>ss_times[ind]:
            pltdays.append(ind)
            maxplt.append(ts_times[ind])

#    maxplt = np.minimum(sr_times,ts_times)
#    minplt = np.maximum(ss_times,tr_times)
#    minplt = np.minimum(minplt,sr_times)
    ax1.plot(pltdays,maxplt,'.',label='minplt')
#    ax1.plot(sr_days,maxplt,label='maxplt')
    
#    ax1.fill_between(sr_days,minplt,maxplt,alpha=.5,where=minplt<maxplt,facecolor='yellow')
#    ax1.fill_between(sr_days,sr_times,ss_times,where=(tr_times[1:]<=sr_times),alpha=.5,facecolor='yellow')
    """
    try:
        tr_days,tr_times,ts_days,ts_times=\
            get_targ_rise_set(simpath,target['name'])
        tr_discont = np.where(np.abs(np.diff(tr_times)) >= 0.5)[0]+1
        tr_days = np.insert(tr_days, tr_discont, np.nan)
        tr_times = np.insert(tr_times, tr_discont, np.nan)
        
        ts_discont = np.where(np.abs(np.diff(ts_times)) >= 0.5)[0]+1
        ts_days = np.insert(ts_days, ts_discont, np.nan)
        ts_times = np.insert(ts_times, ts_discont, np.nan)
    
        ax1.plot(tr_days,tr_times,label='target rises',ms=2)
        ax1.plot(ts_days,ts_times,label='target sets',ms=2)
    
    except:
        print('No rise/set data for target?')
    # save plotting the obs for last for cleanliness in legend
    ax1.plot(days,times,'.',label='obs')
    ax1.axis([-.1*len(sr_days),len(sr_days)+.1*len(sr_days),\
                    np.min(ss_times)-.2*np.min(ss_times),\
                    np.max(sr_times)+.2*np.max(sr_times)])

    box = ax.get_position()
    ax1.set_position([box.x0, box.y0, box.width * 1.2, box.height])
    
    # Put a legend to the right of the current axis
    ax1.legend()#loc='center left', bbox_to_anchor=(1, 0.5),borderaxespad=0.)
    title_str =('%s: (%0.2f,%0.2f), Number of obs: %.1f')%(target['name'],target['ra'],target['dec'],target['num_obs'])
    

    dt_fmt = '%Y-%m-dT%H:%M:%S'
    simname = simpath.split('/')[2]
    summ = np.genfromtxt(simpath+simname+'.txt',dtype=None,delimiter=': ')

    ax1.set_title(title_str)
    ax1.set_xlabel('Days from '+summ[1,1][:8])
    ax1.set_ylabel('Hours from UTC 00:00:00')
#    ax2 = figt.add_subplot(2,1,2)
#    ax2.plot(days,alts,'.')
    plt.show()

def onpick(event,simpath,target_list):

    if event.artist!=bline: return True
    N=len(event.ind)
    if not N: return True

    thisstar = event.artist
    xdata,ydata = thisstar.get_data()
    ind = event.ind
    print(xdata[ind][0])
    print(ydata[ind][0])
    for target in target_list:
        if xdata[ind][0] == target['ra'] and ydata[ind][0] == target['dec']:
            print(target['name'])
            plot_target(simpath,target)
            plt.show()
            break
    return True
if __name__ == '__main__':
    #ipdb.set_trace()
    # get the full target list
    target_list = simbad_reader.read_simbad('./secret/eta_list.txt')
    simnumber = raw_input('Enter sim number: ')
    simpath = glob.glob('./results/*.'+simnumber+'/')[0]
    os.stat(simpath)
    
    all_ras = []
    all_decs = []
    max_num_obs = 0
    min_num_obs = 3000
    num_stars_obs=0
    for target in target_list:

        all_ras.append(target['ra'])
        all_decs.append(target['dec'])
        try:
            tdays,ttimes,alts = get_target(simpath,target['name'])
            target['num_obs'] = len(ttimes)
            num_stars_obs+=1
            if target['num_obs']>max_num_obs:
                max_num_obs = target['num_obs']
            if target['num_obs']<min_num_obs:
                min_num_obs = target['num_obs']
        except:
            target['num_obs'] = 0
    print(num_stars_obs)

    


    # for mollweide
#    all_ras=np.radians(np.array(all_ras)-180.)
#    all_decs=np.radians(np.array(all_decs))
    fig = plt.figure()
    ax = fig.add_subplot(111)#,projection='mollweide')
    bline, = ax.plot(all_ras,all_decs,'.',zorder=1,picker=5)
    for target in target_list:

        # subtract 180 to center
        ra = target['ra']
        dec = target['dec']
        # for mollweide
#        ra = math.radians(target['ra']-180.)
#        dec = math.radians(target['dec'])
        if target['num_obs'] == 0:
            ax.scatter(ra,dec,color='grey',s=20,zorder=2)
            ax.text(ra,dec,target['name'],size=7)
        else:
            ax.scatter(ra,dec,c=target['num_obs'],s=20,zorder=2,
                         vmin=min_num_obs,vmax=max_num_obs,cmap=plt.cm.copper)
            ax.text(ra,dec,target['name'],size=7)
    ax.grid()
    ax.axis([-.5,24.9,-40,95])
    ax.set_title('Eta Earth list '+simnumber)
    ax.set_xlabel('Right Ascension [hours]')
    ax.set_ylabel('Declination [$^\circ$]')
#    ax.set_xticklabels(['2h','4h','6h','8h','10h','12h','14h','16h','18h','20h','22h','24h'])
    fig.canvas.mpl_connect('pick_event',lambda event: onpick(event,simpath,target_list))
    plt.show()
    
    #ipdb.set_trace()

        
        
