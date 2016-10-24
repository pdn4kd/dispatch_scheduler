"""
Functions to read a ''general'' output file from Simbad, used in reading the 
target list, but will be replaced by the google speadsheet with all the target
information. Produces a list of dictionaries, which is the same format that the
spreadsheet reader will produce.
"""

#import ipdb
import collections
import copy

def read_simbad(simbad_output):
    """
    make a dictionary of dictionaries for targets in the given list
    this is for the standard input of a simbad output file, and the 
    target dictionaries will have all the attributes in the file
    could probably be trimmed, but we'll see. might as well include all the 
    the information provided

    currently overwriting binaries, should look into a smarter way, based
    on visual versus spec possibly?
    """
    # open and read the simbad tsv
    with open(simbad_output,'r') as sb_file:
        lines  = sb_file.read().splitlines()
    key_list = []
    for raw_key in lines[5].split('\t'):
        key = "".join(raw_key.split()).lower()
        if key == 'typedident': key = 'name'
        # some cases where i don't like the simbad key
        if key == '#': key = 'number'
        # i think it will be up to the user to figure which coord is which
        # and this allows for multiple ones to be used
        if 'coord' in key: key = key.split('(')[0]
        key_list.append(key)
    target_list = []# collections.OrderedDict()
    for target in lines[7:]:
#        target_name = "".join(target.split('\t')[1].split())       
        target_list.append(collections.OrderedDict())
        ind = 0
        spltarg = target.split('\t')
        while '' in spltarg: spltarg.remove('')
#        ipdb.set_trace()
        for key in key_list:
            if 'coord' in key:
                if len(spltarg[ind].split())>2:
#                target_list[-1][key] = collections.OrderedDict()
#                    ipdb.set_trace()
                    ra = " ".join(spltarg[ind].split()[0:3]).split()
                    ra = (float(ra[0])+float(ra[1])/60.+float(ra[2])/3600.)
                    dec = " ".join(spltarg[ind].split()[3:]).split()
                    if float(dec[0])<0:
                        dec=float(dec[0])-float(dec[1])/60.-float(dec[2])/3600.
                    else:
                        dec=float(dec[0])+float(dec[1])/60.+float(dec[2])/3600.
                    target_list[-1]['ra']=ra
                    target_list[-1]['dec']=dec

                else:
                    target_list[-1]['ra']=float(spltarg[ind].split()[0])
                    target_list[-1]['dec']=float(spltarg[ind].split()[1])
            elif 'pm' in key:
                target_list[-1]['pmra']=float(spltarg[ind].split()[0])
                target_list[-1]['pmdec']=float(spltarg[ind].split()[1])
            else:
                # attempt to convert to a float, but don't throw if not
                try:
                    target_list[-1][key] = \
                        float(spltarg[ind])
                except:
                    target_list[-1][key] = spltarg[ind].strip()
            ind+=1
        
    return target_list

def filter(target_list,decmin=None,decmax=None,ramin=None,\
               ramax=None,magvmin=None,magvmax=None):
    """
    given a target list, go through and filter the list based on given limits
    if they are not the defaults provided. looking into adding more criteria

    does order of filter matter here? also look into optimization. could we 
    apply all criteria at once for each key, rather than looping multiple times
    , mostlikely a better idea.

    """
    # a marker to see if we applied a filter
    new_list_flag = False
    new_list = []


    # check for declination limits, will work this into setting up site 
    # most likely to be able to auto clip targets that will never rise
    # if so, throw a warning to user
    if (decmin or decmax):
        print('Filtering for declination...')
        new_list_flag = True
        if decmin and decmax:
            for target in target_list:
                if target['dec']>decmin and target['dec']<decmax:
                    new_list.append(copy.deepcopy(target))
        elif decmin:
            for target in target_list:
                if target['dec']>decmin:
                    new_list.append(copy.deepcopy(target))
        elif decmax:
            for target in target_list:
                if target['dec']<decmax:
                    new_list.append(copy.deepcopy(target))
        target_list = copy.deepcopy(new_list)
        new_list = []

    # check for RA limits, this is weird but why not include the option
    if (ramin or ramax):
        print('Filtering for right ascension...')
        new_list_flag = True
        if ramin and ramax:
            for target in target_list:
                if target['ra']>ramin and target['ra']<ramax:
                    new_list.append(copy.deepcopy(target))
        elif ramin:
            for target in target_list:
                if target['ra']>ramin:
                    new_list.append(copy.deepcopy(target))
        elif ramax:
            for target in target_list:
                if target['ra']<ramax:
                    new_list.append(copy.deepcopy(target))
        target_list = copy.deepcopy(new_list)
        new_list = []

    if (magvmin or magvmax):
        print('Filtering for magv...')
        new_list_flag = True
        if magvmin and magvmax:
            for target in target_list:
                if target['magv']>magvmin and target['magv']<magvmax:
                    new_list.append(copy.deepcopy(target))
        elif magvmin:
            for target in target_list:
                if target['magv']>magvmin:
                    new_list.append(copy.deepcopy(target))
        elif magvmax:
            for target in target_list:
                if target['magv']<magvmax:
                    new_list.append(copy.deepcopy(target))
        target_list = copy.deepcopy(new_list)
        new_list = []

    return target_list

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    #ipdb.set_trace()
#    tlist = read_simbad('sample_list.txt')
    tlist = read_simbad('secret/eta_list.txt')
    #ipdb.set_trace()
    newlist = filter(tlist)
    ras = []
    decs = []
    mags = []
    for target in newlist: ras.append(target['ra'])
    for target in newlist: decs.append(target['dec'])
    for target in newlist: 
        try: mags.append(float(target['magv']))
        except: pass
    plt.plot(ras,decs,'.')
#    plt.plot(mags,'.')
    plt.show()
    #ipdb.set_trace()
