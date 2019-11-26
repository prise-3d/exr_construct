#! /usr/bin/python

import os
import argparse
import OpenEXR
import Imath
import numpy 

"""

This program generates an exr image from the average of an exr file set.
It can also calculate intermediate files.

"""

def saveDataToExr(r,g,b,size0,size1,filename) :

    data_red = (r).tostring()  
    data_green = (g).tostring()      
    data_blue = (b).tostring() 

    exr = OpenEXR.OutputFile(filename, OpenEXR.Header(size0,size1))
    print("  >> write "+filename)
    exr.writePixels({'R': data_red, 'G': data_green, 'B': data_blue})


def exr_const(path, inter, step = 1, output = "/tmp", intermediate = False):
    
    listdir = os.listdir(path)
    n = 0

    pt = Imath.PixelType(Imath.PixelType.FLOAT)

    for element in listdir :
        full_name = str(path)+element
        #print(full_name)
        if os.path.isfile(full_name) and OpenEXR.isOpenExrFile(full_name) :
            
            print("+ "+full_name)
            im = OpenEXR.InputFile(full_name)
            dw = im.header()['dataWindow']
            size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)
            
            redstr = im.channel('R',pt)
            greenstr = im.channel('G',pt)
            bluestr = im.channel('B',pt)

            #red = numpy.fromstring(redstr, dtype = numpy.float32)            
            red = numpy.frombuffer(redstr, dtype= numpy.float32)
            red.shape = (size[1], size[0])

            green = numpy.frombuffer(greenstr, dtype = numpy.float32)
            green.shape = (size[1], size[0])

            blue = numpy.frombuffer(bluestr, dtype = numpy.float32)
            blue.shape = (size[1], size[0])

            if n == 0 :
                
                redres = numpy.copy(red)
                greenres = numpy.copy(green)
                blueres = numpy.copy(blue)
            else :
                redres += red 
                greenres += green
                blueres += blue 

            n += 1    
            
            if intermediate and ( (n*step) % inter ) == 0 :   

               # intermediate save 
                out_file_name = output+"/out_"+ f"{(n*step):05d}" +".exr"
                saveDataToExr(redres/n,greenres/n,blueres/n,size[0],size[1],out_file_name)

            # last element = final save    
            if element == listdir[-1] : 
                out_file_name = output+"/out_final.exr"
                saveDataToExr(redres/n,greenres/n,blueres/n,size[0],size[1],out_file_name)


if __name__ == "__main__" :

    parser = argparse.ArgumentParser()    
    parser.add_argument("path")
    parser.add_argument("-s", "--step", type=int,
                    help="step used for rendering")
    parser.add_argument("-o", "--output",help="output directory")                
    parser.add_argument("-i", "--interval", type=int,
                    help="interval for intermediate files (must be a multiple of step)")  
    parser.add_argument("-I", "--intermediate", help="compute intermediate exr files",
                    action="store_true")                              
    args = parser.parse_args()  

    step = args.step  
    path = args.path
    inter = args.interval
    out = args.output
    intermediate = args.intermediate

    if (inter == None) :
        inter = step

    print("step = "+str(step)+ " "  +str(type(step)))
    print("inter = "+str(inter)+ " " +str(type(inter)))
    print("starting...\n dir = "+path)
    
    # if output folder path does not exist
    if not os.path.exists(out):
        os.makedirs(out)

    exr_const(path,inter,step,out,intermediate)
