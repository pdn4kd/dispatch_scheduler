"""
a class for a telescope in use with the dispatch scheduler. need to keep track 
of where it is pointing, etc. Could also implement two observing mode feature.
"""

from configobj import ConfigObj
import utils
import sys
import os
import ephem
import datetime
import math


class telescope:
    def __init__(self,config_file,number,base_directory='.'):
        self.base_directory = base_directory
        self.config_file = config_file
        self.load_config()
        self.number = number

    def load_config(self):
        try:
            config = ConfigObj(self.base_directory+'/config/'+self.config_file)
            self.slewrate = float(config['Setup']['SLEWRATE'])
            self.alt = float(config['Setup']['PARK_ALT'])
            self.azm = float(config['Setup']['PARK_AZM'])
        except:
            print('ERROR accessing configuration file: ' + self.config_file)
            sys.exit()
        try:
            self.area = float(config['Setup']['AREA'])
        except:
            try:
                self.diameter = float(config['Setup']['DIAMETER'])
                self.area = math.pi*self.diameter**2
            except:
                print('ERROR accessing configuration file: ' + self.config_file)
                sys.exit()

    

    def acquire_target(self,target):
        """
        slew to a given target, give some overhead for actually acquiring?
        """
        pass

    def slew(self,target_alt,target_azm,time):
        pass

    def observe(self,target,scheduler):
        obs_string = 'T1'
        return obs_string
        
        
