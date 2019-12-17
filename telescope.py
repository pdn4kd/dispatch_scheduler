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
            self.diameter = float(config['Setup']['DIAMETER'])
        except:
            print('ERROR accessing configuration file: ' + self.config_file)
            sys.exit()
        try:
            self.area = float(config['Setup']['AREA'])
        except:
            self.area = math.pi*self.diameter**2
            print('WARNING telescope area not found, estimating from diameter (0 obstruction)')
    

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
        
class instrument:
    def __init__(self,config_file,number,base_directory='.'):
        self.base_directory = base_directory
        self.config_file = config_file
        self.load_config()
        self.number = number

    def load_config(self):
        try:
            config = ConfigObj(self.base_directory+'/config/'+self.config_file)
            self.instname = str(config['Setup']['INSTNAME'])
            self.efficiency = float(config['Setup']['EFFICIENCY'])
            self.R = float(config['Setup']['R'])
            self.λmin = float(config['Setup']['WAVELENGTH_MIN'])
            self.λmax = float(config['Setup']['WAVELENGTH_MAX'])
            self.well_depth = float(config['Setup']['WELL_DEPTH'])
            self.gain = float(config['Setup']['GAIN'])
            self.read_noise = float(config['Setup']['READ_NOISE'])
            self.dark_current = float(config['Setup']['DARK_CURRENT'])
            self.n_pix = float(config['Setup']['PIXELS'])
            self.read_time = float(config['Setup']['READOUT_TIME'])
            self.general_noise = float(config['Setup']['GENERAL_NOISE'])
        except:
            print('ERROR accessing configuration file: ' + self.config_file)
            sys.exit()
        try:
            self.SNR = float(config['Setup']['SNR'])
        except:
            print('WARNING: No SNR information in configuration file (' + self.config_file + '), assuming nominal value (0)')
            self.SNR = 0
