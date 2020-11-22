# Import modules
import arcpy
import numpy as np
import os, sys

# Checking path directory
# When running through ArcGIS pro, abs_path refers to this script
# so I used os.path.dirname twice to go the parent folder of this project
# and then use relative path for setting up project's workspace in ArcGIS pro
abs_path = os.path.abspath(sys.argv[0])
dir_name = os.path.dirname(os.path.dirname(abs_path))

# Allow arcpy to overwrite outputs
arcpy.env.overwrite = True
arcpy.AddToDisplay = True

# Set environment settings
scratch_folder = "scratch"
workspace_folder = f'{dir_name}\\{scratch_folder}' 
arcpy.env.workspace = workspace_folder

# DEM raster input by user 
input_raster_locations = arcpy.GetParameterAsText(0)

# If input_raster_locations has a semicolon, it means that user provided multiple rasters
if ";" not in input_raster_locations:
    # change file location to raster
    input_raster = arcpy.Raster(input_raster_locations)

else:    
    # Split raster files
    split_raster = input_raster_locations.split(";")
    
    # Store coordinate reference system of the first raster and change all of them to the same CRS
    first_raster = arcpy.Raster(split_raster[0])
    first_raster_CRS = arcpy.Describe(first_raster).spatialReference.factoryCode
    
    # Arguments for Mosaic To New Raster geoprocessing tool
    raster_location = f'{dir_name}\\data\\'
    file_name = "merged_raster.tif"
    pixel_type = "32_BIT_FLOAT"
    band_num = 1
    
    # Join all the rasters
    arcpy.AddMessage("Joining all DEM rasters...")
    input_raster = arcpy.MosaicToNewRaster_management(input_raster_locations, raster_location, file_name, first_raster_CRS, pixel_type, "", band_num)

# Check CRS of the DEM raster using its Well Known ID
raster_CRS = arcpy.Describe(input_raster).spatialReference.factoryCode
arcpy.env.outputCoordinateSystem = raster_CRS # to avoid an error in Fill process

# Fill in sinks in DEM
arcpy.AddMessage("Filling sinks in the DEM raster...")
fill_raster = arcpy.sa.Fill(input_raster)

# Generate flow direction
arcpy.AddMessage("Computing flow direction based on DEM raster...")
flow_direction = arcpy.sa.FlowDirection(fill_raster,"", "", "D8")

# Generate flow accumulation based on flow direction
arcpy.AddMessage("Generating flow accumulation based on flow direction...")
flow_accumulation = arcpy.sa.FlowAccumulation(flow_direction)

# Outlet shapefile input by user (change to user input)
#input_outlet = "..\\data\\outlet_feature_class3.shp"
input_outlet = arcpy.GetParameterAsText(1)

# Change CRS of outlet feature class
arcpy.AddMessage("Changing spatial reference of outlet feature layer using DEM raster's Well-Known ID...")
outlet_proj = arcpy.Project_management(input_outlet, "outlet_projected.shp", raster_CRS)
arcpy.SetParameterAsText(7, outlet_proj)

# If more than 1 outlet points are provided, ask user whether to aggregate watersheds into 1 polygon or keep them in separate polygons
aggregate_watershed = arcpy.GetParameterAsText(2)
#aggregate_watershed = False

# Add a new field to determine how to handle multiple watersheds from multiple outlets  
arcpy.DeleteField_management(outlet_proj, "AggNum")
arcpy.AddField_management(outlet_proj, "AggNum", "SHORT")
field = ['AggNum']
i = 0

# Count number of rows in outlet point's attribute table
num_outlet = arcpy.GetCount_management(outlet_proj).messageCount

# Check if number of outlets are more than 1
if num_outlet > 1:
    
    # if user checks aggregate watersheds, same integer value i will be added to each row of AggNum field
    if aggregate_watershed == 'true':
        with arcpy.da.UpdateCursor(outlet_proj, field) as cursor:
            for row in cursor:
                row[0] = i
                cursor.updateRow(row)
    
    # if unchecked, it will assign unique integers to each outlet feature if user does not wants to aggregate
    elif aggregate_watershed == 'false':
        with arcpy.da.UpdateCursor(outlet_proj, field) as cursor:
            for row in cursor:
                row[0] = i
                cursor.updateRow(row)
                i += 1
    # Assigning unique value to each outlet point feature will make snap outlet raster of different values
    # in the next step which will make separate watersheds 

# Snap outlet points to nearest stream pixel, outputs 1 pixel for each outlet point overlapping the pixel
# highest flow accumulation within a specified proximity
arcpy.AddMessage("Snapping outlet point(s) to nearest raster cell with highest flow accumulation value...")
snap_tolerance = arcpy.GetParameterAsText(3) #snap sensitivity, assign to user
input_outlet_snapped = arcpy.sa.SnapPourPoint(outlet_proj, flow_accumulation, snap_tolerance, "AggNum")

# Delete the unique integer field we created in outlet points feature layer
arcpy.DeleteField_management(outlet_proj, "AggNum")

# Delineate watershed based on outlet point by user input
arcpy.AddMessage("Delineating watershed based on flow direction and snapped outlet(s)...")
watershed_raster = arcpy.sa.Watershed(flow_direction, input_outlet_snapped)

# Convert watershed raster to polygon
# make unique file names
arcpy.AddMessage("Converting watershed raster to polygon feature...")
watershed_polygon = arcpy.RasterToPolygon_conversion(watershed_raster,"watershed_polygon.shp")
arcpy.SetParameterAsText(5, watershed_polygon)

# Delineate stream network if x number of pixels run into 1 pixel for flow accumulation
# may be take user input for how much x should be
arcpy.AddMessage("Delineating stream network based on user-specified inflow cells...")
stream_net_tolerance = arcpy.GetParameterAsText(4)
where_clause = f"VALUE > {int(stream_net_tolerance)}"
stream_net = arcpy.sa.Con(flow_accumulation, flow_accumulation, "", where_clause)

# Assign stream order for better visuals
arcpy.AddMessage("Assigning stream order to each stream...")
stream_order = arcpy.sa.StreamOrder(stream_net, flow_direction)

# Convert raster of stream order to features
arcpy.AddMessage("Converting stream order rasters to feature layer...") 
stream_feature = arcpy.sa.StreamToFeature(stream_order, flow_direction, "feature_stream.shp")

# Clip stream network to watershed area
arcpy.AddMessage("Clip stream network using watershed boundary...")
stream_feature_clipped = arcpy.Clip_analysis(stream_feature, watershed_polygon, "feature_stream_clipped.shp")
arcpy.SetParameterAsText(6, stream_feature_clipped)

# Finished
arcpy.AddMessage("Watershed(s) and stream delineation finished!")



                        # ----- X ----- #
                        
                        
                        
                        
#-----------------------------------------------------------------------------#

# Trial and error code
# input_raster = [arcpy.Raster("..\\data\\raster_1.tif"), arcpy.Raster("..\\data\\raster_2.tif"), arcpy.Raster("..\\data\\raster_3.tif"), arcpy.Raster("..\\data\\raster_4.tif")]
#    n = len(input_raster)
#    raster_names = ""
#    for i in input_raster:
#        # Concatenate raster names into a required format for merging all the rasters using Mosaic to New Raster
#        print(i)
#        semicolon = raster_location + i.name + ";"
#        raster_names = raster_names + semicolon
### CHOICE 1: HAVING NO OUTLETS SHAPEFILE
# Delineate watersheds based on outlet points in the raster
#watershed_raster = arcpy.sa.Basin(flow_direction)
#delineate stream network as well and dissolve them into single shapefile.
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

























