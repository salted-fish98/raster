# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 01:11:43 2019

@author: fzy_1998
"""

from osgeo import gdalnumeric,gdal
import numpy as np

def openRaster(file):
    data = gdalnumeric.LoadFile(file)
    data = data.astype(np.float32)
    a = data[0][0]
    data[data==a]=np.nan
    return data

def saveTif(data,file,output):
    ds = gdal.Open(file)
    shape = data.shape
    driver = gdal.GetDriverByName("GTiff") 
    dataset = driver.Create(output, shape[1], shape[0], 1, gdal.GDT_Float32)
    dataset.SetGeoTransform(ds.GetGeoTransform())
    dataset.SetProjection(ds.GetProjection()) 
    dataset.GetRasterBand(1).WriteArray(data)