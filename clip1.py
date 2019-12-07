# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 00:17:23 2019

@author: fzy_1998
"""

import rasterio as rio
import rasterio.mask
import numpy as np
from geopandas import GeoDataFrame
from rasterio.warp import (reproject, transform_bounds,calculate_default_transform as calcdt)

def clipRaster(shpfile,datafile,clipfile):
    #shp转geojson
    shpdata = GeoDataFrame.from_file(shpfile)
    geo = shpdata.geometry[0]
    feature = [geo.__geo_interface__]
    #裁剪
    src = rio.open(datafile)

    out_image, out_transform = rio.mask.mask(src, feature, crop=True, nodata=np.nan)
    out_meta = src.meta.copy()
    out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})

    band_mask = rasterio.open(clipfile, "w", **out_meta)
    band_mask.write(out_image)