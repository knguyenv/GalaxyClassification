from PIL import Image
import glob
import numpy as np



def cropAndOutput(inFolder, outFolder):

    for fName in glob.glob(inFolder + '*.jpeg'):
        original = Image.open(fName)
        fileName = fName.split('/')[1]
        width, height = original.size   # Get dimensions

        left = width/4
        top = height/4
        right = 3 * width/4
        bottom = 3 * height/4

        degree = 0
        whitePixelCount = -1
        rotateDegree = -1

        while degree < 360:
            rImage = original.rotate(degree)
            bbox = rImage.getbbox()
            curCount = sum(rImage.crop((left, top, width/2, height/2))
                           .convert('1')
                           .point(bool)
                           .getdata())
            if curCount > whitePixelCount:
                whitePixelCount = curCount
                rotateDegree = degree
            degree += 45

        cropped = original.rotate(rotateDegree)
        cropped = cropped.crop((left, top, right, bottom))
        #cropped = cropped.convert('1')
        cropped.save(outFolder + fileName, 'jpeg')

cropAndOutput('2arms/', 'input2/')
cropAndOutput('5arms/', 'input5/')
cropAndOutput('smooth/', 'inputS/')


