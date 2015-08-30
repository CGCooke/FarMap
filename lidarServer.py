''' Style Guide
http://www.python.org/dev/peps/pep-0008/'''

''' standard library imports '''
import os

''' related third party imports ''' 
from flask import Flask,send_file
from StringIO import StringIO
from PIL import Image

from globalmaptiles import GlobalMercator

class tileRequest:
    def __init__(self, tileStr):
        ''' For more detail see README.md '''
        z,y,x,extension = tileStr.split('.')
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
    tileFileName = str(z)+'.'+str(y)+'.'+str(x)+'.png'
    
    print(x,y,z)    
    tilesize = 256
    tx = tile.tx
    ty =tile.ty

    zoom = tile.zoom
    px = tx*tilesize 
    py = ty*tilesize 
    gm = GlobalMercator()

    mx1,my1 = gm.PixelsToMeters(px, py, zoom)

    mx2,my2 = gm.PixelsToMeters(px+tilesize, py+tilesize, zoom)
    print(mx1,-my2,mx2,-my1)

    os.system('rm Subset.TIF')
    os.system('gdalwarp -q -t_srs epsg:3857 -te '+str(mx1)+' '+str(-my2)+' '+str(mx2)+' '+str(-my1)+' -r Lanczos -ts 256 256 Warped.TIF Subset.TIF')
    

    #Open the image
    tileImage = Image.open('Subset.TIF')
   
    #Turn the image into a string
    buffer_image = StringIO()
    tileImage.save(buffer_image, 'png')
    buffer_image.seek(0)
    #Send the string
    return(send_file(buffer_image, mimetype='image/png'))
  

os.system('gdalwarp -t_srs EPSG:3857 -q -r cubic Beach.TIF Warped.TIF')

if __name__ == "__main__":
    os.system('rm Subset.TIF')
    print('Server has started')
    os.system('rm -r DownloadedTiles')
    os.system('mkdir DownloadedTiles')

    app.run()
    

    
