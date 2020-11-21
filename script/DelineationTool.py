# add message while each process runs

# import packages
import arcpy
import numpy as np
import os

# Checking path directory
abs_path = os.path.abspath(sys.argv[0])
#dir_name = os.path.dirname(abs_path)
#os.chdir(dir_name)

# Allow arcpy to overwrite outputs
arcpy.env.overwrite = True
arcpy.addOutputsToMap = True

# Set environment settings 
arcpy.env.workspace = "V:\\FinalProject\\Watershed-Stream-Delineation-Tool\\scratch"

# DEM raster input by user (change to user input)
input_raster = [arcpy.Raster("..\\data\\raster_1.tif"), arcpy.Raster("..\\data\\raster_2.tif"), arcpy.Raster("..\\data\\raster_3.tif"), arcpy.Raster("..\\data\\raster_4.tif")]
#input_raster = arcpy.GetParameterAsText(0)

# if added multiple, then mosaic to raster...
if len(input_raster) == 1:
    continue
else:
    n = len(input_raster)
    arcpy.MosaicToNewRaster_management
    #https://pro.arcgis.com/en/pro-app/tool-reference/data-management/mosaic-to-new-raster.htm

# Ask user which way they want to supply outlet point(s)
#choice_outlet = 

# Check CRS of the DEM raster using its Well Known ID
raster_CRS = arcpy.Describe(input_raster).spatialReference.factoryCode
# later assign it the raster's CRS

# Fill in sinks in DEM
fill_raster = arcpy.sa.Fill(input_raster)

# Generate flow direction
flow_direction = arcpy.sa.FlowDirection(fill_raster,"", "", "D8")

### CHOICE 1: HAVING NO OUTLETS SHAPEFILE
# Delineate watersheds based on outlet points in the raster
#watershed_raster = arcpy.sa.Basin(flow_direction)
#delineate stream network as well and dissolve them into single shapefile.

#calculate area so user can filter if they want

### CHOICE 2: USER INPUT OUTLET SHAPEFILE

# Generate flow accumulation based on flow direction
flow_accumulation = arcpy.sa.FlowAccumulation(flow_direction)

# Outlet shapefile input by user (change to user input)
#input_outlet = "..\\data\\outlet_feature_class2.shp"
input_outlet = arcpy.GetParameterAsText(1)

# Check CRS of outlet feature class
arcpy.Describe(input_outlet).spatialReference.name
#make unique file names
outlet_proj = arcpy.Project_management(input_outlet, "outlet_projected.shp", raster_CRS)
arcpy.SetParameterAsText(4, outlet_proj)

# Snap outlet points to nearest stream
snap_tolerance = 50 #snap sensitivity, assign to user
input_outlet_snapped = arcpy.sa.SnapPourPoint(outlet_proj,flow_accumulation, 100)

# Delineate watershed based on outlet point by user input
watershed_raster = arcpy.sa.Watershed(flow_direction, input_outlet_snapped)

# Convert watershed raster to polygon
# make unique file names
watershed_polygon = arcpy.RasterToPolygon_conversion(watershed_raster,"watershed_polygon.shp")
arcpy.SetParameterAsText(2, watershed_polygon)

# Delineate stream network if x number of pixels run into 1 pixel for flow accumulation
# may be take user input for how much x should be
stream_net = arcpy.sa.Con(flow_accumulation > 1000, flow_accumulation)

# Assign stream order for better visuals
stream_order = arcpy.sa.StreamOrder(stream_net, flow_direction)

# Convert raster of stream order to features
# make unique file names 
stream_feature = arcpy.sa.StreamToFeature(stream_order, flow_direction, "feature_stream.shp")

# Clip stream network to watershed area
stream_feature_clipped = arcpy.Clip_analysis(stream_feature, watershed_polygon, "feature_stream_clipped.shp")
arcpy.SetParameterAsText(3, stream_feature_clipped)




# Apply symbology to watershed polygon, stream network and outlet point
#watershed_symbology = "..\\script\\watershed_polygon.lyrx" 
#stream_symbology = "..\\script\\feature_stream_clipped.lyrx"
#outlet_symbology = "..\\script\\outlet_projected.lyrx"

#arcpy.ApplySymbologyFromLayer_management(watershed_polygon, watershed_symbology)
#arcpy.ApplySymbologyFromLayer_management(stream_feature_clipped, stream_symbology)
#arcpy.ApplySymbologyFromLayer_management(outlet_proj, outlet_symbology) 

#m = arcpy.mp.ArcGISProject("CURRENT")
#lm = m.listMaps()[0]
#lm.addLayer(watershed_polygon)
#lm.addLayer(stream_feature_clipped)
#lm.addLayer(outlet_proj)

# delete intermediary files?? ask user

























