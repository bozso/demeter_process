# -*- coding: utf-8 -*-

import numpy as np
from jdcal import gcal2jd

def process_line(line_str):
    
    # kp 3 hour, ap 3 hour, ap average, sspot num
    
    return [ int(line_str[12:14]), int(line_str[14:16]), int(line_str[16:18]), 
    int(line_str[18:20]), int(line_str[20:22]), int(line_str[22:24]), 
    int(line_str[24:26]), int(line_str[26:28]), int(line_str[31:34]), 
    int(line_str[34:37]), int(line_str[37:40]), int(line_str[40:43]), 
    int(line_str[43:46]), int(line_str[46:49]), int(line_str[49:52]), 
    int(line_str[52:55]), int(line_str[55:58]), int(line_str[62:65])]

def read_kp(filepath):

    cnesjd = []
    
    f = open(filepath, 'r')

    read_lines = [line.rstrip() for line in f]
    
    f.close()
    
    start = gcal2jd(2000 + int(read_lines[0][0:2]),
    int(read_lines[0][2:4]), int(read_lines[0][4:6]))[1] - 33282
    
    stop = gcal2jd(2000 + int(read_lines[-1][0:2]),
    int(read_lines[-1][2:4]), int(read_lines[-1][4:6]))[1] - 33282

    cjd_frac = np.arange(start, stop + 1, 0.125)
    cjd_whole = np.arange(start, stop + 1)
    
    data = np.asarray([process_line(line) for line in read_lines])
    
    return np.column_stack( (cjd_frac, data[:,0:8].flatten(), 
    data[:,8:16].flatten()) ), np.column_stack( (cjd_whole, data[:,16:18]) )

