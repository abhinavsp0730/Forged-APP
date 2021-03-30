import os
import numpy as np 
import cv2
import requests
import sys

from PIL import Image
from io import BytesIO
from matplotlib import pyplot

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uuid
import boto3
import uvicorn
import shutil
from fastapi.middleware.cors import CORSMiddleware

manTraNet_root = './ManTraNet/'
manTraNet_srcDir = os.path.join( manTraNet_root, 'src' )
sys.path.insert( 0, manTraNet_srcDir )
manTraNet_modelDir = os.path.join( manTraNet_root, 'pretrained_weights' )

import modelCore
manTraNet = modelCore.load_pretrain_model_by_index( 4, manTraNet_modelDir )

from datetime import datetime 
def read_rgb_image( image_file ) :
    rgb = cv2.imread( image_file, 1 )[...,::-1]
    return rgb
    
def decode_an_image_array( rgb, manTraNet, dn=1 ) :
    x = np.expand_dims( rgb.astype('float32')/255.*2-1, axis=0 )[:,::dn,::dn]
    t0 = datetime.now()
    y = manTraNet.predict(x)[0,...,0]
    t1 = datetime.now()
    return y, t1-t0

def decode_an_image_file( image_file, manTraNet, dn=1 ) :
    rgb = read_rgb_image( image_file )
    mask, ptime = decode_an_image_array( rgb, manTraNet, dn )
    return rgb[::dn,::dn], mask, ptime.total_seconds()

def mkdir_p(mypath):
    '''Creates a directory. equivalent to using mkdir -p on the command line'''

    from errno import EEXIST
    from os import makedirs,path

    try:
        makedirs(mypath)
    except OSError as exc: # Python >2.5
        if exc.errno == EEXIST and path.isdir(mypath):
            pass
        else: raise


def ranname():
  return str(uuid.uuid1())+".png"

# replace # with your aws access keys for s3 bucket
s3_client = boto3.client('s3', 
                      aws_access_key_id="################", 
                      aws_secret_access_key="################", 
                      region_name="us-west-1"
                      )

def get_image_from_url(url,xrange=None, yrange=None, dn=1) :
    name = ranname()
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = np.array(img)
    if img.shape[-1] > 3 :
        img = img[...,:3]
    ori = np.array(img)
    if xrange is not None :
        img = img[:,xrange[0]:xrange[1]]
    if yrange is not None :
        img = img[yrange[0]:yrange[1]]
    mask, ptime =  decode_an_image_array( img, manTraNet, dn )
    ptime = ptime.total_seconds()
    # show results
    fig = pyplot.figure( figsize=(15,5) )
    pyplot.title('Original Image')
    pyplot.subplot(131)
    pyplot.imshow( img )
    pyplot.title('Forged Image (ManTra-Net Input)')
    pyplot.subplot(132)
    pyplot.imshow( mask, cmap='gray' )
    pyplot.title('Predicted Mask (ManTra-Net Output)')
    pyplot.subplot(133)
    pyplot.imshow( np.round(np.expand_dims(mask,axis=-1) * img[::dn,::dn]).astype('uint8'), cmap='jet' )
    for ax in fig.axes:
      ax.axis("off")
    pyplot.title('Highlighted Forged Regions')
    pyplot.suptitle('Inference Time {:.2f} seconds'.format( ptime ))
    output_dir = "tantra"
    mkdir_p(output_dir)
    txt = '{}/'+name
    pyplot.savefig(txt.format(output_dir))
    pyplot.show()
    return name

def upload(s3,name):
  bucket_name = 'mantrap'
  content = open('./tantra/'+name, 'rb')
  s3.put_object(
  Bucket=bucket_name, 
  Key= name, 
  Body=content)


class Item(BaseModel):
    url: str


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/predict")
async def create_item(item: Item):
    item_dict = item.dict()
    name = get_image_from_url(item.url)
    upload(s3_client, name)
    shutil.rmtree('./tantra', ignore_errors=True)
    # put your aws s3 bucket url.
    img = "https://"+name
    return {"url": img}