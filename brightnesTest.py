from PIL import Image
from PIL import ImageStat
import os


def brightness( im_file ):
   im = Image.open("/home/ryan/slideFilter/testing/f2_clean/" + im_file).convert('L')
   stat = ImageStat.Stat(im)
   return stat.mean[0]


brightnessArr = []
# mainStr = "rm "
for subdir, dirs, files in os.walk("/home/ryan/slideFilter/testing/f2_clean"):
    for file in files:
        brightnessArr.append(brightness(file))
        # mainStr += " " + file

print("\nThe range of the array is " + '{0:.1f}'.format(min(brightnessArr)) + " - " + '{0:.1f}'.format(max(brightnessArr)))
print("Average is : " + str(sum(brightnessArr) / len(brightnessArr)))
# print(mainStr)
print("done\n")