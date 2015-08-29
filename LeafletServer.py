''' Style Guide
http://www.python.org/dev/peps/pep-0008/'''

''' standard library imports '''
import os

''' related third party imports ''' 
from flask import Flask,send_file
from StringIO import StringIO
from PIL import Image

class tileRequest:
    def __init__(self, tileStr):
        ''' For more detail see README.md '''
        z,x,y,extension = tileStr.split('.')
        zoom,tx,ty = int(z),int(x),int(y)
        self.zoom = zoom
        self.tx = tx
        self.ty = ty

app = Flask(__name__)
app.debug = True

@app.route('/')
def indexPage():
    f = open('index.html')
    return(f.read())

@app.route('/Imagery/<path:tileStr>')
def ImageryRequest(tileStr):
    tile = tileRequest(tileStr)
    z = tile.zoom
    x = tile.tx
    y = tile.ty
    
    downloadedTileList = os.listdir('DownloadedTiles/')
    tileFileName = str(z)+'.'+str(4*y)+'.'+str(4*x)+'.png'
    
    #if tileFileName not in downloadedTileList:
       #os.system('curl ' + 'http://maps.six.nsw.gov.au/arcgis/rest/services/public/NSW_Base_Map/MapServer/tile/'+str(z)+'/'+str(x)+'/'+str(y)+'.png' + ' > '+'DownloadedTiles/'+tileFileName+' --silent')
    os.system('curl http://appmapdata.environment.nsw.gov.au/arcgiswa/rest/services/Soil_Landscape/Sydney/MapServer/tile/'+str(z)+'/'+str(4*y)+'/'+str(4*x)+' > '+'DownloadedTiles/'+tileFileName+' --silent')
    
    #z,x,y = 11,1228,1883
    #os.system('curl http://appmapdata.environment.nsw.gov.au/arcgiswa/rest/services/Landuse/Landuse/MapServer/'+str(z)+'/'+str(y)+'/'+str(x)+' > out.png')

    #Open the image
    tileImage = Image.open('DownloadedTiles/'+tileFileName)
    #Turn the image into a string
    buffer_image = StringIO()
    tileImage.save(buffer_image, 'png')
    buffer_image.seek(0)
    #Send the string
    return(send_file(buffer_image, mimetype='image/png'))
  
#z,y,x = 12,9853,12524
#os.system('curl http://appmapdata.environment.nsw.gov.au/arcgiswa/rest/services/Soil_Landscape/Sydney/MapServer/tile/'+str(z)+'/'+str(y)+'/'+str(x)+' > out.png')
#os.system('curl http://appmapdata.environment.nsw.gov.au/arcgiswa/rest/services/Soil_Landscape/Sydney/MapServer/tile/12/9853/12524 > out.png')



if __name__ == "__main__":
    print('Server has started')
    os.system('rm -r DownloadedTiles')
    os.system('mkdir DownloadedTiles')

    app.run()
    
    