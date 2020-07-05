#!/usr/bin/python3


# Original by Oliver Turnbull for EnviroPi project, part of the AstroPi competition

# 2020: Modified by CoderDojo Trento for:
#    - reads from custom directory
#    - evidence viewport ellipse
#    - automatically creates output dir
#    - added console option parsing

from PIL import Image
import numpy
import sys
import os
import time
import csv
import matplotlib
from matplotlib import pyplot as plt
startTime = time.time()


def convertImage(filename):
    
    # Opens image to be converted
    img = Image.open('%s/%s' % (in_dir,filename))
    
    # crop ellipse
    from PIL import ImageDraw
    offset = 100
    background_color = (0,0,0)
    background = Image.new(img.mode, img.size, background_color)    
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    #takes bounding box
    
    draw.ellipse((offset, -300, img.size[0] - offset, img.size[1]), fill=255)
    img = Image.composite(img, background, mask)    
    # end crop ellipse
        
    
    # Places red and blue values in numpy arrays
    imgR, imgG, imgB = img.split() #get channels
    
    # Places red and blue values in numpy arrays
    arrR = numpy.asarray(imgR).astype('float32')
    arrG = numpy.asarray(imgG).astype('float32')
    arrB = numpy.asarray(imgB).astype('float32')
    
    
    # Calculates the Index value by dividing
    # Red minus Blue over Red plus Blue
    
    num = (arrR - arrB)
    denom = (arrR + arrB)
    
    arrIndex = num/denom

    
    # Changes colour map, jet has been used
    customCmap= plt.set_cmap('jet')
    img_w, img_h = img.size
    

    if AUTO_CONTRAST:
       vmin = numpy.nanmin(arrIndex)
       vmax = numpy.nanmax(arrIndex)
    
    dpi   = 600 #int(img_w/fig_w)
    vmin  = -1 #most negative Index value
    vmax  = 1 #most positive Index value
    
    found_min = numpy.nanmin(arrIndex)
    found_max = numpy.nanmax(arrIndex)
    print('found_min:',found_min,' found_max:', found_max)
        
    if AUTO_CONTRAST:            
        vmin = found_min
        vmax = found_max
    print('AUTO_CONTRAST:',AUTO_CONTRAST)

    print('vmin:',vmin,'     vmax:', vmax)

    #lay out the plot, making room for a colorbar space
    fig_w = img_w/dpi
    fig_h = img_h/dpi
    fig = plt.figure(figsize=(fig_w,fig_h), dpi=dpi)
    fig.set_frameon(False)

    #make an axis for the image filling the whole figure except colorbar space
    ax_rect = [0.0, #left
               0.0, #bottom
               1.0, #width
               1.0] #height
    ax = fig.add_axes(ax_rect)
    ax.yaxis.set_ticklabels([])
    ax.xaxis.set_ticklabels([])
    ax.set_axis_off()
    ax.patch.set_alpha(0.0)

    axes_img = ax.imshow(arrIndex,
                          cmap = customCmap,
                          vmin = vmin,
                          vmax = vmax,
                          aspect = 'equal',
                         )
    
    # Adds colorbar, used for illustritive purposes but turned off for actual EnviroPi experiment
    cax = fig.add_axes([0.95, 0.05, 0.025, 0.90] )
    cbar = fig.colorbar(axes_img, cax=cax)
    
    #fig.tight_layout(pad=0)
    fig.savefig("%s/%s" % (out_dir, filename),
                dpi=dpi,
                bbox_inches='tight',
                pad_inches=0.0,
               )
    
    plt.close(fig)
    return numpy.nanmean(arrIndex, )


def show_help():
    print('imageProcess.py [-c] -i <inputdir> -o <outputdir> ')


AUTO_CONTRAST = False
in_dir = 'raw'
out_dir = 'ProcessedImages'

argv = sys.argv[1:]
import sys, getopt
try:
      opts, args = getopt.getopt(argv,"chi:o:")
except getopt.GetoptError:
    show_help()
    sys.exit(2)

for opt, arg in opts:
    if opt == '-h':
        show_help()
        sys.exit()
    elif opt in ("-c"):
        AUTO_CONTRAST = True
    elif opt in ("-i"):
        in_dir = arg
        if not os.path.isdir(in_dir):
            print()
            print('ERROR! SPECIFIED INPUT FOLDER DOES NOT EXISTS:', in_dir)
            print()
            sys.exit(2)
    elif opt in ("-o"):
        out_dir = arg
print()
print('    Input dir:', in_dir)
print('   Output dir:', out_dir)
print('AUTO_CONTRAST:',AUTO_CONTRAST)


if not os. path. isdir(out_dir):
    print()
    print('Creating dir', out_dir)
    os.makedirs(out_dir)

file_paths = sorted(os.listdir(in_dir))
print()
print('Found', len(file_paths), 'files to process in folder', in_dir)

with open(out_dir + '/ProcessedIndex.csv', 'w', newline='') as csvfile_out:

    my_writer = csv.writer(csvfile_out, delimiter=',')

    my_writer.writerow(['File Path', 'Average Index'])

    for file_path in file_paths:
        print()
        print('Processing', file_path)
        avgIndex = convertImage(file_path)
        print('Average Index:',avgIndex)

        my_writer.writerow([file_path, avgIndex])
          
print('time taken %s seconds' %(time.time() - startTime))