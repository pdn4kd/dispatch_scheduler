"""
A quick program for stripping the output from exoplanets.org
Temporary, and probably useless.
"""
#import ipdb

if __name__ == '__main__':
 #   ipdb.set_trace()
    tl_file = open('Exoplanet')
    newfile = ''
    for line in tl_file:
        newline = line.split()[0]+line.split()[1]+'\n'
        newfile += newline
    
#    ipdb.set_trace()
    newtargs = open('targets.txt','w')
    newtargs.write(newfile)
