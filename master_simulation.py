# -*- coding: utf-8 -*-
import os
orbit = [7178.0, 0.001, 30.0, 316.0, 0.0]
path = 'C:/Users/mt19g14/MASTER Simulation Database/test_folder/output'

try: 
    os.makedirs(path)
except OSError:
    if not os.path.isdir(path):
        raise