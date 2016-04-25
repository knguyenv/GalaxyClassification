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

        hollowCore = Image.new(original.mode, (20, 20))
        #hollowCore.show()
        box = (width/2 - 9, width/2 - 9, width/2 +10, width/2+10)

        for rate in range(0, 8):
            degree = rate * 45
            rImage = original.rotate(degree)
            names = fileName.split('.')
            newName = names[0] + "_" + str(rate) + "." + names[1]

            #Hollow out the center region
            rImage.paste(hollowCore, (width/2 - 9, width/2 - 9))
            rImage = rImage.crop((left, top, right, bottom))
            rImage.save(outFolder + newName, 'jpeg')


cropAndOutput('2arms/', '2/')
cropAndOutput('5arms/', '5/')
cropAndOutput('smooth/', 'S/')


