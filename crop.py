from __future__ import print_function
import os

from PIL import Image

# Number of pictures in sequence.
n_pics = 25
# Input and output directory
in_dir = '6/'
out_dir = '6/'
# Crop boundaries: left, upper, right, lower.
left, upper, right, lower = 350, 650, 1450, 1650

name_fmt = 'trj_6_0_{n}.png'

for i in range(n_pics):
    print('Cropping', i)
    name = name_fmt.format(n=i)
    image = Image.open(os.path.join(in_dir, name))
    cropped = image.crop((left, upper, right, lower))
    out_name = 'cropped_' + str(i) + '.png'
    cropped.save(os.path.join(out_dir, out_name), 'png')
    image.close()
