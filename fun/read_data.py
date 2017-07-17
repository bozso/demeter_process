# -*- coding: utf-8 -*-

import numpy as np
from numpy.lib import recfunctions

iap_struct = np.dtype([('cnesjd', '>I'), ('msec_of_day', '>I'), ('year',
'>H'), ('month', '>H'), ('day', '>H'), ('hour', '>H'), ('min', '>H'), ('sec',
'>H'), ('msec', '>H'), ('orbit_num', '>H'), ('sub_orb_type', '>H'),
('tm_station', '>c', 8), ('sft_ver', '>b', 4), ('glat', '>f'), ('glon', '>f'),
('alt', '>f'), ('lt', '>f'), ('mlat', '>f'), ('mlon', '>f'), ('mlt', '>f'),
('ilat', '>f'), ('mcl', '>f'), ('cglat', '>f'), ('cglon', '>f'), ('nglat',
'>f'), ('nglon', '>f'), ('sglat', '>f'), ('sglon', '>f'), ('Bx', '>f', 1),
('By', '>f', 1), ('Bz', '>f', 1), ('gyro', '>f'), ('Sx', '>f', 1), ('Sy',
'>f', 1), ('Sz', '>f', 1), ('sft_ver_2', '>b', 2), ('m_sat2geo', '>f', 9),
('m_geo2lgm', '>f', 9), ('quality', '>H'), ('sft_ver_3', '>b', 2),
('data_type', '>c', 10), ('hk', '>B', 32), ('t_res', '>f'), ('dens_unit',
'>c', 6), ('temp_unit', '>c', 6), ('vel_unit', '>c', 6), ('pot_unit', '>c',
6), ('angle_unit', '>c', 6), ('h', '>f'), ('he', '>f'), ('o', '>f'), ('iont',
'>f'), ('ionv', '>f'), ('theta', '>f'), ('phi', '>f'), ('pot', '>f')])

def validate_paths(file_with_paths, auth_word):
    """Validating filepaths. Checking file size and data type"""

    import os

    with open(file_with_paths) as f:
        content = f.readlines()

    content = ("".join(content)).rstrip()

    input_file_paths = content.splitlines()

    num_of_files = len(input_file_paths)

    # Validating filepaths
    for iii in range(num_of_files):

        size_in_bytes = os.path.getsize(input_file_paths[iii])

        if size_in_bytes % 312:
            print("data_read: Error: Filesize is not adequate!")
            print("data_read: At file: ", input_file_paths[iii])
            return 1
        else:
            input_file = open(input_file_paths[iii], "rb")
            input_file.seek(204)

        if input_file.read(10) != auth_word:
            print("data_read: Error: Data types do not match!")
            print("data_read: At file: ", input_file_paths[iii])
            return 1
        else:
            input_file.close()

    return 0

def read_data(input_file_paths, required='all'):

    """Reads binary data"""

    import os

    shift = 0

    with open(input_file_paths) as f:
        lengths = [os.path.getsize(line.rstrip()) // 312 for line in f]
    
    lengths.reverse()

    num_of_rows = sum(lengths)
    
    if 'sub_orb_type' not in required:
        required.append('sub_orb_type')
    
    if 'cnesjd' in required and 'msec_of_day' not in required:
        required.append('msec_of_day')
    
    if required == 'all':
        data = np.empty(shape = num_of_rows, dtype=iap_struct)
    else:
        sub_dt = [(req, iap_struct[req]) for req in required]
        data = np.empty(shape = num_of_rows, dtype=sub_dt)

    with open(input_file_paths) as f:

        for line in f:

            input_file = open(line.rstrip(), "rb")

            rows = lengths.pop()
            
            if required == 'all':
                data[shift:shift+rows] = np.fromfile(input_file, iap_struct, rows)
            else:                                                                    
                data[shift:shift+rows] = np.fromfile(input_file, iap_struct, rows)[required]
                                                                                
            shift += rows

    data['cnesjd'] %= 16777216

    idx = data['sub_orb_type'].astype('bool')
    
    required.remove('sub_orb_type')

    if 'cnesjd' in required:
        cnesjd = data['cnesjd'].astype(np.double) +\
                 data['msec_of_day'].astype(np.double) / 86400000

        data = recfunctions.drop_fields(data, ['cnesjd', 'msec_of_day'],
                                        usemask=False)

        data = recfunctions.append_fields(data, 'cnesjd', cnesjd, dtypes=np.double,
                                          usemask=False)
    
    required.remove('msec_of_day')
    
    day = data[np.logical_not(idx)][required]
    night = data[idx][required]

    return day, night
