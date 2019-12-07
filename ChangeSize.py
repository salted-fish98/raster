# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 14:17:07 2019

@author: fzy_1998
"""

from osgeo import gdalnumeric
import numpy as np
import gdal,os

def getLonlat(file):
    print(file)
    ds = gdal.Open(file)
    geos = ds.GetGeoTransform()
    cols = ds.RasterXSize
    rows = ds.RasterYSize
    minX = geos[0]
    maxY = geos[3]
    maxX = cols*geos[1]+minX
    minY = rows*geos[5]+maxY
    return minX,maxX,minY,maxY

def getxy(minX1,maxX1,minY1,maxY1,minX2,maxX2,minY2,maxY2,shape,pixel):
    #2为裁剪后的小范围。1为裁剪前的大范围
    if (minX2-minX1)>0:
        y1 = round((minX2-minX1)/pixel)
    else:
        y1 = 0
        
    if (maxX1-maxX2)>0:
        y2 = shape[1]-round((maxX1-maxX2)/pixel)
    else:
        y2 = shape[1]   
        
    if (minY2-minY1)>0:
        x2 = shape[0]-round((minY2-minY1)/pixel)
    else:
        x2 = shape[0]
    
    if (maxY1-maxY2)>0:
        x1 = round((maxY1-maxY2)/pixel)
    else:
        x1 = 0
    
    return x1,x2,y1,y2
    
def convert(infile,dsfile,pixel,output):
    minX1,maxX1,minY1,maxY1 = getLonlat(infile)
    minX2,maxX2,minY2,maxY2 = getLonlat(dsfile)
    
    data1 = gdalnumeric.LoadFile(infile)
    
    #经度范围
    shape = data1.shape
    x1,x2,y1,y2 = getxy(minX1,maxX1,minY1,maxY1,minX2,maxX2,minY2,maxY2,shape,pixel)
    
    data = data1[x1:x2,y1:y2]
    
    #获取目标的经纬度
    ds = gdal.Open(dsfile)
    geos2 = list(ds.GetGeoTransform())
    minX2,maxX2,minY2,maxY2 = getLonlat(dsfile)
    
    #更新新建数据的经纬度
    geos1 = list(ds.GetGeoTransform())
    
    if minX1<minX2:
        geos1[0] = minX2
    else:
        geos1[0] = minX1
        
    if maxY1<maxY2:
        geos1[3] = maxY1
        
    else:
        geos1[3] = maxY2
        
    #获取更新后的经纬度
    minX1 = geos1[0]
    maxY1 = geos1[3]
    maxX1 = geos1[0]+data.shape[1]*pixel
    minY1 = geos1[3]-data.shape[0]*pixel

    data2 = gdalnumeric.LoadFile(dsfile)
    shape = data2.shape
    x1,x2,y1,y2 = getxy(minX2,maxX2,minY2,maxY2,minX1,maxX1,minY1,maxY1,shape,pixel)

    data2 = np.zeros((shape[0],shape[1]))
    data2 = data2.astype(np.float32)
    data2[data2==0]=np.nan
    data2[x1:x2,y1:y2] = data
    
    
    shape = data2.shape
    driver = gdal.GetDriverByName("GTiff") 
    dataset = driver.Create(output, shape[1], shape[0], 1, gdal.GDT_Float32)
    dataset.SetGeoTransform(geos2)
    dataset.SetProjection(ds.GetProjection()) 
    dataset.GetRasterBand(1).WriteArray(data)
    

def getNames(names):
    namesList = []
    for name in names:
        a = name.split('.')[-1]
        if a=='tif':
            namesList.append(name)
    return namesList

if __name__ == "__main__":

    infile = r'F:\生态红线0.01\土壤水分\栅格\water'
    dsfile = 'F:/生态红线0.01/neimenggu_meteo/prep/prepMon/pre198001_new.tif'
    out =  r'F:\生态红线0.01\土壤水分\栅格\water1'
    '''
    filepath = r'F:\生态红线0.01\土壤水分\栅格\water\2009_7_Kriging.tif'
    dsfile = r'F:\生态红线0.01\neimenggu_meteo\rh\rhMon\rh198001_new.tif'
    outpath = r'F:\生态红线0.01\土壤水分\栅格\2009_7_Kriging.tif'
    pixel = 0.01
    convert(filepath,dsfile,pixel,outpath)
    '''
    os.chdir(infile)
    names = os.listdir()
    names = getNames(names)
    for name in names:
        filepath = infile+'\\'+name 
        outpath = out+'\\'+name
        pixel = 0.01
        convert(filepath,dsfile,pixel,outpath)
 