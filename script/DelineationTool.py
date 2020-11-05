# import packages
import arcpy
import numpy as np
import os

# Changing working directory to where this script is located
#abs_path = os.path.abspath(sys.argv[0])
#dir_name = os.path.dirname(abs_path)
#os.chdir(dir_name)

# Allow arcpy to overwrite outputs
arcpy.env.overwrite = True

# Set environment settings 
# arcpy.env.workspace = "V:/FinalProject/Watershed-"

# DEM raster input by user (change to user input)
input_raster = arcpy.Raster("V:\\FinalProject\\Watershed-Stream-Delineation-Tool\\data\\wake_county.tif")

# Fill in sinks in DEM
fill_raster = arcpy.sa.Fill(input_raster)

# Generate flow direction
flow_direct = arcpy.sa.FlowDirection(fill_raster, True)

# Delineate watersheds based on outlet points in the raster
watershed_raster = arcpy.sa.Basin(flow_direct)

# Convert watershed raster to polygon
watershed_polygon = arcpy.RasterToPolygon_conversion(watershed_raster,
                                                     "watershed_polygon.shp",
                                                     )
