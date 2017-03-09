# -*- coding: utf-8 -*-
import shutil
import subprocess

from utils import create_folder, check_strings


class MasterWrapper(object):

    def __init__(self, sim_name, run_id, simulation_case, save_path, save_inputs,
                 master_path):

        self.__sim_name = sim_name
        self.__run_id = run_id
        self.__save_path = save_path
        self.__master_path = master_path
        self.__source_path = "source_files"
        self.__save_inputs = save_inputs
        if self.__save_inputs:
            self.__input_path = '/'.join([self.__save_path, self.__sim_name,
                                          'input'])
        else:
            self.__input_path = '/'.join([self.__master_path,
                                          'input'])

        self.__output_path = '/'.join([self.__save_path, self.__sim_name,
                                       'output'])
        self.__data_path = '/'.join([self.__master_path, 'data'])
        self.__data_cloud_path = '/'.join([self.__master_path, 'data',
                                           'clouds'])
        self.__debris_sources, self.__size_limits, self.__distribution_2d, self.__distribution_3d = simulation_setup(simulation_case)
        # checking if data is in correct format
        self.__debris_sources = check_strings(self.__debris_sources)
        self.__size_limits = check_strings(self.__size_limits)
        self.__distribution_2d = check_strings(self.__distribution_2d)
        self.__distribution_3d = check_strings(self.__distribution_3d)
            
        
    def set_master_config(self):
        master_config_file(self.__master_path, self.__source_path,
                           self.__input_path, self.__output_path,
                           self.__data_path, self.__data_cloud_path)  
        return 0

    def set_master_input(self, orbit, begin_epoch, end_epoch,
                         scenario_id=1, analysis_mode=1):

        master_input_file(self.__source_path, self.__input_path,
                          self.__run_id, orbit, begin_epoch, end_epoch,
                          scenario_id, self.__debris_sources,
                          self.__size_limits, analysis_mode)
        return 0

    def set_master_default(self):
        master_default_file(self.__source_path, self.__input_path,
                            self.__distribution_2d, self.__distribution_3d)
        master_default_constellation(self.__source_path, self.__input_path)
        master_default_sdf(self.__source_path, self.__input_path)

    def check_simulation(self):
        if self.__save_inputs:
            sub_folders = ['input', 'output']
        else:
            sub_folders = ['output']
        cf = create_folder(self.__sim_name, self.__save_path, sub_folders)
        return cf

    def call(self):
        p = subprocess.Popen(['master_windows.exe'],
                             cwd=self.__master_path,
                             shell=True)
        p.wait()
        return 0


def master_config_file(master_path, source_path, input_path, output_path,
                       data_path, data_cloud_path):

    with open('/'.join([source_path, 'master.cfg']), 'r') as f_in:
        data = f_in.readlines()
    config_inputs = [output_path, data_path, data_cloud_path, input_path]
    for i in range(4):
        set_data = data[23 + i].split()
        set_data[0] = config_inputs[i]
        data[23 + i] = '  ' + ' '.join(set_data) + '\n'
    with open('/'.join([master_path, 'master.cfg']), 'w') as f_out:
        f_out.writelines(data)
    return 0


def master_input_file(source_path, input_path, run_id, orbit, begin_epoch,
                      end_epoch, scenario_id, switches, size_limits,
                      analysis_mode):
    """
    Modifies MASTER-2009 input files master.inp with user defined values

    Parameters
    ----------
    run_id [str]:
        Identifier of the simulation. Must be unique.
    orbit [list]:
        Target orbit of the simulation.
        orbit = [sma(km), ecc, inc(deg), RAAN(deg), AoP(deg)]
    begin_epoch:
        Starting date of the MASTER simulation in the form:
        YEAR/MONTH/DAY/HOUR
    bend_epoch:
        Ending date of the MASTER simulation in the form:
        YEAR/MONTH/DAY/HOUR
    scenario_id [int]:
        1 - business as usual
        2 - intermediate mititgation
        3 - full mitigation
    switches [list]:
        Defines which debris sources are considered. 0 is 'off' and 1 is 'on'.
        The list has eleven contribution. The different contributions are
        described int the following.
        The number represent the index in the list.
        0 - explosion fragments
        1 - collision fragments
        2 - launch/mission related objects
        3 - NaK droplets
        4 - SRM slag
        5 - SRM Al2O3 dust
        6 - paint flakes
        7 - ejecta
        8 - MLI
        9 - meteoroids
        10 - clouds
    size_limits [list]:
        The lower and upper threshold of the diameter/mass of the debris.
        The units needs to be specified. If meters (m) are specified the
        diameter is considered. If kilograms (kg) are specified, the mass
        is considered.
        The input has the following aspect:
        size_limits = [LOWER_LIMIT, UPPER_LIMIT, UNIT]
        For example:
        size_limits = [1e-4, 1, m]
    analysis_mode [int]:
        Defines the type of analysis carried out. Three options are available:
        1 - target orbit
        2-inertial volume
        3-spatial density

    Returns
    -------
    Write to the output the modified master.inp file. The file is saved in the
    specified input folder.

    Info
    -----
    Author:
        Mirko Trisolini
    Change Log:
    """
    begin_yr, begin_mt, begin_dy, begin_hr = begin_epoch.split('/')
    end_yr, end_mt, end_dy, end_hr = end_epoch.split('/')
    orbit = check_strings(orbit)  # conversion of orbital parameters into strings for writing
    with open('/'.join([source_path, 'master.inp']), 'r') as f_in:
        lines = [line for line in f_in]
        with open('/'.join([input_path, 'master.inp']), 'w') as f_out:
            i = 0
            for line in lines:
                if line.startswith('#'):
                    f_out.write(line)
                    i += 1
                    continue
                sl = line.split()
                if i == 22:
                    # run identifiier
                    sl[0] = run_id
                elif i == 33:
                    # begin date
                    sl[0] = begin_yr
                    sl[1] = begin_mt
                    sl[2] = begin_dy
                    sl[3] = begin_hr
                elif i == 34:
                    # end date
                    sl[0] = end_yr
                    sl[1] = end_mt
                    sl[2] = end_dy
                    sl[3] = end_hr
                elif i == 40:
                    # scenario id:
                    # 1-business as usual
                    # 2-intermediate mitigation
                    # 3-full mitigation
                    sl[0] = str(scenario_id)
                if i == 49:
                    # explosion fragments
                    sl[0] = switches[0]
                if i == 50:
                    # collision fragments
                    sl[0] = switches[1]
                if i == 51:
                    # launch/mission related objects
                    sl[0] = switches[2]
                if i == 52:
                    # NaK droplets
                    sl[0] = switches[3]
                if i == 53:
                    # SRM slag
                    sl[0] = switches[4]
                if i == 54:
                    # SRM Al2O3 dust
                    sl[0] = switches[5]
                if i == 55:
                    # paint flakes
                    sl[0] = switches[6]
                if i == 56:
                    # ejecta
                    sl[0] = switches[7]
                if i == 57:
                    # MLI
                    sl[0] = switches[8]
                if i == 58:
                    # meteoroids
                    sl[0] = switches[9]
                if i == 59:
                    # clouds
                    sl[0] = switches[10]
                if i == 81:
                    # debris lower threshold size - m or kg
                    sl[0] = size_limits[0]
                    sl[1] = size_limits[2]
                if i == 82:
                    # debris upper threshold size - m or kg
                    sl[0] = size_limits[1]
                    sl[1] = size_limits[2]
                if i == 88:
                    # analysis mode:
                    # 1-target orbit
                    # 2-inertial volume
                    # 3-spatial density
                    sl[0] = str(analysis_mode)
                    sl.append('\n')
                elif i == 100:
                    # Target orbit characteristics
                    # begin date
                    sl[0] = begin_yr
                    sl[1] = begin_mt
                    sl[2] = begin_dy
                    sl[3] = begin_hr
                    # end date
                    sl[4] = end_yr
                    sl[5] = end_mt
                    sl[6] = end_dy
                    sl[7] = end_hr
                    # semi-major axis
                    sl[8] = orbit[0]
                    # eccentricity
                    sl[9] = orbit[1]
                    # inclination
                    sl[10] = orbit[2]
                    # right asension of the ascending node
                    sl[11] = orbit[3]
                    # argument of perigee
                    sl[12] = orbit[4]
                    sl.append('\n')
                else:
                    sl.append('\n')
                sl = ' '.join(sl)
                f_out.write(sl)
                i += 1
    return 0


def master_default_file(source_path, input_path, distribution_2D,
                        distribution_3D):
    distribution_2D = check_strings(distribution_2D)
    distribution_3D = check_strings(distribution_3D)
    with open('/'.join([source_path, 'default.def']), 'r') as f_in:
        lines = [line for line in f_in]
        with open('/'.join([input_path, 'default.def']), 'w') as f_out:
            i = 0
            for line in lines:
                sl = line.split()
                if line.startswith('#'):
                    f_out.write(line)
                    i += 1
                    continue
                else:
                    sl.append('\n')
                for item in distribution_2D:
                    if i < 80:
                        if sl[0] == str(item[0]):
                            sl[1] = item[1]
                            sl[2] = item[2]
                            sl[3] = item[3]
                            sl[4] = item[4]
                            sl[5] = item[5]
                            sl[6] = item[6]
                            break
                        elif sl[0] != str(item[0]):
                            sl[1] = '0'
                            continue
                    else:
                        break
                for item in distribution_3D:
                    if i > 80:
                        if sl[0] is str(item[0]):
                            sl[1] = item[1]
                            sl[2] = item[2]
                            sl[3] = item[3]
                            break
                        elif sl[0] != str(item[0]):
                            sl[1] = '0'
                            continue
                    else:
                        break
                sl = ' '.join(sl)
                f_out.write(sl)
                i += 1


def master_default_constellation(source_path, input_path):
    shutil.copy('/'.join([source_path, 'default.con']),
                '/'.join([input_path, 'default.con']))
    return 0


def master_default_sdf(source_path, input_path):
    shutil.copy('/'.join([source_path, 'default.sdf']),
                '/'.join([input_path, 'default.sdf']))
    return 0


def simulation_setup(case):
    """Select among a set of predefined simulation characteristics for MASTER.
    The predefined parameters to specify in MASTER are the sources of debris,
    the size limits, the 2D and 3D distribution fluxes to produce as output.
    """
    #TODO: if time add the possibility to load with input file.
    if case == 0 or case == '0':
        debris_sources = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
        size_limits = [1e-04, 0.1, 'm']

        distribution_2d = [[2, 1, 1, 1, 1e-04, 0.1, -50],
                           [9, 1, 0, 0, 0, 40, 0.5],
                           [10, 1, 0, 0, -180, 180, 2.5],
                           [11, 1, 0, 0, -90, 90, 2.5]]

        distribution_3d = [[1, 1, 11, 10],
                           [2, 1, 10, 9],
                           [3, 1, 10, 2]]
        return debris_sources, size_limits, distribution_2d, distribution_3d

    elif case == 1 or case == '1':  # TODO: update to different values
        debris_sources = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
        size_limits = [1e-04, 0.1, 'm']

        distribution_2d = [[2, 1, 1, 1, 1e-04, 0.1, -200],
                           [9, 1, 0, 0, 0, 40, 0.5],
                           [10, 1, 0, 0, -180, 180, 2.5],
                           [11, 1, 0, 0, -90, 90, 2.5]]

        distribution_3d = [[1, 1, 10, 11],
                           [2, 1, 10, 9],
                           [3, 1, 2, 9],
                           [4, 1, 2, 10],
                           [5, 1, 2, 11],
                           [6, 1, 11, 10],
                           [7, 1, 11, 9]] 
        return debris_sources, size_limits, distribution_2d, distribution_3d
    else:
        raise ValueError("Case number {} does not exist.".format(case))
