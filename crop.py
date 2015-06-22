from __future__ import print_function
from PIL import Image


name_fmt = 'trj_6_0_{n}.png'
for i in range(64):
    print('Cropping', i)
    name = name_fmt.format(n=i)
    image = Image.open(name)
    cropped = image.crop((100, 450, 1800, 1800))
    cropped.save('cropped_' + str(i), 'png')
    image.close()
