# -*- coding: utf-8 -*-
import numpy as np

from master_wrapper_class import MasterWrapper

DEFAULT_PATH = r'C:\Users\Mirko\Documents\Python Scripts\dev_environment\master_wrapper\simulation_database'
DEFAULT_MASTER_PATH = r'C:\Program Files (x86)\MASTER-2009'
DEFAULT_EPOCH = ['2009/01/01/00', '2010/01/01/00']
DEFAULT_ORBIT = [7178.0, 0.001, 60.0, 316.0, 0.0]

                                         
def run_master(sim_name='sim_1', run_id='master', simulation_case=0,
               begin_epoch=DEFAULT_EPOCH[0], end_epoch=DEFAULT_EPOCH[1],
               orbit=DEFAULT_ORBIT, save_path=DEFAULT_PATH, save_inputs=False,
               master_path=DEFAULT_MASTER_PATH):
    
    master_run = MasterWrapper(sim_name, run_id, simulation_case, save_path,
                               save_inputs, master_path)
    check = master_run.check_simulation()
    if check:
        master_run.set_master_config()
        master_run.set_master_input(orbit, begin_epoch, end_epoch)
        master_run.set_master_default()
        master_run.call()
    return "Simulation completed"


def run_master_multi(input_file, save_path=DEFAULT_PATH, save_inputs=False,
                     master_path=DEFAULT_MASTER_PATH):
    # load input to the master simulations
    with open(input_file, 'r') as f_in:
        data = f_in.readlines()
    for line in data:
        line = line.rstrip('\n').split('\t')
        run_master(line[0], line[1], line[2], line[3],
                   line[4], line[5:], save_path, save_inputs, master_path)
    return "Simulations completed!"


def create_input_file(file_name, save_path, simulation_case, begin_epoch, end_epoch,
                      altitude_range, altitude_step, inclination_range,
                      inclination_step):

    RE = 6378.1  #equatorial radius in km
    data = []
    for alt in range(altitude_range[0], altitude_range[1], altitude_step):
        for inc in range(inclination_range[0], inclination_range[1],
                         inclination_step):
            data.append(['_'.join(['h'+str(alt), 'i'+str(inc)]), 'master', simulation_case,
                         begin_epoch, end_epoch, RE + alt, 0.001, inc, 0.0, 0.0])
    data = np.array(data)
    with open('/'.join([save_path, file_name]), 'w') as f_out:
        for item in data:
            f_out.write('\t'.join(item) + '\n')   
    