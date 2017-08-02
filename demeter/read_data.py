import numpy as np
from numpy.lib import recfunctions
from jdcal import gcal2jd

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

def read_data(input_paths, required='all', corr_lon=False):

    """Reads binary data"""

    import os

    if 'sub_orb_type' not in required and required != 'all':
        required.append('sub_orb_type')
    
    if 'cnesjd' in required and 'msec_of_day' not in required and \
    required != 'all':
        required.append('msec_of_day')
        
    
    if required == 'all':
        data = [ np.fromfile( open(line.rstrip(), 'rb'), iap_struct, 
        os.path.getsize(line.rstrip()) // 312) for line in 
        input_paths ]
    else:
        data = [ np.fromfile(open(line.rstrip(), 'rb'), iap_struct, 
        os.path.getsize(line.rstrip()) // 312)[required] for line in 
        input_paths ]

    
    data = np.concatenate(data)
    
    if corr_lon:
        lons = ['mlon', 'glon', 'cglon', 'nglon', 'sglon']
        fieldnames = data.dtype.names

        for lon in lons:
            if lon in fieldnames:
                data[lon][data[lon] > 180.0] -= 360

    
    data['cnesjd'] %= 16777216

    idx = data['sub_orb_type'].astype('bool')
    
    if required != 'all':
        
        idx = data['sub_orb_type'].astype('bool')
        required.remove('sub_orb_type')
    
        if 'cnesjd' in required:
            cnesjd = data['cnesjd'].astype(np.double) +\
                     data['msec_of_day'].astype(np.double) / 86400000

            data = recfunctions.drop_fields(data, ['cnesjd', 
                                            'msec_of_day'], usemask=False)

            data = recfunctions.append_fields(data, 'cnesjd', cnesjd,
            dtypes=np.double, usemask=False)
            
            required.remove('msec_of_day')
        
            day = data[np.logical_not(idx)][required]
            night = data[idx][required]
    else:
        day = data[np.logical_not(idx)]
        night = data[idx]
    

    return day, night

def process_line(line_str):
    
    return [
    int(line_str[12:14]), # Kp for 0000 - 0300 UT. -- 0
    int(line_str[14:16]), # Kp for 0300 - 0600 UT. -- 1
    int(line_str[16:18]), # Kp for 0600 - 0900 UT. -- 2
    int(line_str[18:20]), # Kp for 0900 - 1200 UT. -- 3
    int(line_str[20:22]), # Kp for 1200 - 1500 UT. -- 4
    int(line_str[22:24]), # Kp for 1500 - 1800 UT. -- 5
    int(line_str[24:26]), # Kp for 1800 - 2100 UT. -- 6
    int(line_str[26:28]), # Kp for 2100 - 2400 UT. -- 7
    int(line_str[28:31]), # SUM of the eight Kp indices for the day
                          # expressed to the near-est third of a unit.
                          #  -- 8
    int(line_str[31:34]), # ap for 0000 - 0300 UT. -- 9
    int(line_str[34:37]), # ap for 0300 - 0600 UT. -- 10
    int(line_str[37:40]), # ap for 0600 - 0900 UT. -- 11
    int(line_str[40:43]), # ap for 0900 - 1200 UT. -- 12
    int(line_str[43:46]), # ap for 1200 - 1500 UT. -- 13
    int(line_str[46:49]), # ap for 1500 - 1800 UT. -- 14
    int(line_str[49:52]), # ap for 1800 - 2100 UT. -- 15
    int(line_str[52:55]), # ap for 2100 - 2400 UT. -- 16
    int(line_str[55:58]), # Ap or PLANETARY EQUIVALENT DAILY
                          # AMPLITUDE--the arithmetic mean -- 17
    float(line_str[58:61]), # Cp - overall level of magnetic activity
                          #  -- 18
    int(line_str[62:65])  # INTERNATIONAL SUNSPOT NUMBER.  -- 19
    ]

def read_idx(filepath):
    
    f = open(filepath, 'r')

    read_lines = [line.rstrip() for line in f]
    
    f.close()
    
    start = gcal2jd(2000 + int(read_lines[0][0:2]),
    int(read_lines[0][2:4]), int(read_lines[0][4:6]))[1] - 33282
    
    stop = gcal2jd(2000 + int(read_lines[-1][0:2]),
    int(read_lines[-1][2:4]), int(read_lines[-1][4:6]))[1] - 33282

    
    data = np.asarray([process_line(line) for line in read_lines])
    
    idx_frac = np.empty( data.shape[0] * 8, dtype=[
                        ('cnesjd', 'float64'),
                        ('kp', data.dtype),
                        ('ap', data.dtype) ] )
    
    idx_frac['cnesjd'] = np.arange(start, stop + 1, 0.125)
    idx_frac['kp'] = data[:,0:8].flatten()
    idx_frac['ap'] = data[:,9:17].flatten()

    idx_whole = np.empty( data.shape[0], dtype=[
                        ('cnesjd', 'float64'),
                        ('ap', data.dtype),
                        ('cp', data.dtype),
                        ('kp_sum', data.dtype),
                        ('sunspot', data.dtype) ] )
    
    idx_whole['cnesjd'] = cjd_whole = np.arange(start, stop + 1)
    idx_whole['kp_sum'] = data[:,8]
    idx_whole['ap'] = data[:,17]
    idx_whole['cp'] = data[:,18]
    idx_whole['sunspot'] = data[:,19]
        
    return idx_frac, idx_whole


iap_struct = np.dtype([('cnesjd', '>I'), ('msec_of_day', '>I'),
('year', '>H'), ('month', '>H'), ('day', '>H'), ('hour', '>H'),
('min', '>H'), ('sec', '>H'), ('msec', '>H'), ('orbit_num', '>H'),
('sub_orb_type', '>H'), ('tm_station', '>c', 8), ('sft_ver', '>b', 4),
('glat', '>f'), ('glon', '>f'), ('alt', '>f'), ('lt', '>f'),
('mlat', '>f'), ('mlon', '>f'), ('mlt', '>f'), ('ilat', '>f'),
('mcl','>f'), ('cglat', '>f'), ('cglon', '>f'), ('nglat', '>f'),
('nglon', '>f'), ('sglat', '>f'), ('sglon', '>f'), ('Bx', '>f', 1),
('By', '>f', 1), ('Bz', '>f', 1), ('gyro', '>f'), ('Sx', '>f', 1),
('Sy', '>f', 1), ('Sz', '>f', 1), ('sft_ver_2', '>b', 2),
('m_sat2geo', '>f', 9), ('m_geo2lgm', '>f', 9), ('quality', '>H'),
('sft_ver_3', '>b', 2), ('data_type', '>c', 10), ('hk', '>B', 32),
('t_res', '>f'), ('dens_unit', '>c', 6), ('temp_unit', '>c', 6),
('vel_unit', '>c', 6), ('pot_unit', '>c', 6), ('angle_unit', '>c', 6),
('h', '>f'), ('he', '>f'), ('o', '>f'), ('iont', '>f'), ('ionv', '>f'),
('theta', '>f'), ('phi', '>f'), ('pot', '>f')])
