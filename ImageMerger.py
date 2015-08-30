from osgeo import gdal
from osgeo import osr
import numpy as np
from PIL import Image
import os

def arrayToRaster(array,fileName,EPSGCode,xMin,xMax,yMin,yMax,numBands):
	xPixels = array.shape[1]  # number of pixels in x
	yPixels = array.shape[0]  # number of pixels in y
	pixelXSize =(xMax-xMin)/xPixels # size of the pixel in X direction     
	pixelYSize = -(yMax-yMin)/yPixels # size of the pixel in Y direction

	driver = gdal.GetDriverByName('GTiff')
	dataset = driver.Create(fileName,xPixels,yPixels,numBands,gdal.GDT_Byte, options = [ 'PHOTOMETRIC=RGB' ])
	dataset.SetGeoTransform((xMin,pixelXSize,0,yMax,0,pixelYSize))  

	datasetSRS = osr.SpatialReference()
	datasetSRS.ImportFromEPSG(EPSGCode)
	dataset.SetProjection(datasetSRS.ExportToWkt())
	
	for i in range(0,numBands):
		dataset.GetRasterBand(i+1).WriteArray(array[:,:,i])

	dataset.FlushCache()  # Write to disk.


EPSGCode = 32756
numBands = 3

for fString in os.listdir('LiDAR/'):
	if '.png' in fString:

		img  = np.asarray(Image.open('LiDAR/'+fString))

		xMin,yMin = (fString[1:-11].split(','))
		xMin = int(xMin)
		yMin = int(yMin)
		xMax = xMin + 50
		yMax = yMin + 50 


		arrayToRaster(img,'OUT.TIF',EPSGCode,xMin,xMax,yMin,yMax,numBands)

		os.system('gdalwarp -q -t_srs epsg:32756 -tr 0.25 -0.25 -r lanczos  OUT.TIF '+str(xMin)+'_'+str(yMin)+'.TIF')
		os.system('rm OUT.TIF')


	os.system('gdal_merge.py -init 255 -o out.tif *.TIF')