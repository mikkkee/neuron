import subprocess
import shlex
from PIL import Image, ImageDraw


from analyzer import parse_result
import settings


def draw_result(result_file, out_prefix='dump_'):
    '''Draw result file to images seperated according to timesteps.'''
    results = parse_result(result_file)
    x = [point.x for timestep in results for neuron in timestep for segment in neuron for point in [segment.left, segment.right]]
    y = [point.y for timestep in results for neuron in timestep for segment in neuron for point in [segment.left, segment.right]]

    # Determine size of canvas.
    min_x, max_x = min(x) - 50, max(x) + 50
    min_y, max_y = min(y) - 50, max(y) + 50

    if abs(min_x - max_x) < 500:
        min_x = min_x - 250
        max_x = max_x + 250

    if abs(min_y - max_y) < 500:
        min_y = min_y - 250
        max_y = max_y + 250

    shift_x = - min_x if min_x < 0 else 0
    shift_y = - min_y if min_y < 0 else 0


    for i, timestep in enumerate(results):

        # Init image.
        name = '{}{:03d}.png'.format(out_prefix, i)
        image = Image.new('RGBA', (int(max_x + shift_x), int(max_y + shift_y)), 'white')
        draw = ImageDraw.Draw(image)

        # Draw segments on.
        for number, neuron in enumerate(timestep):
            for seg in neuron:
                lx = seg.left.x + shift_x
                ly = seg.left.y + shift_y
                rx = seg.right.x + shift_x
                ry = seg.right.y + shift_y

                draw.line(((lx, ly), (rx, ry)), fill=settings.color, width=2)

        image.save(name)


def make_movie(fmt, name, rate=0.2):
    cmd = "/usr/local/bin/ffmpeg -framerate 1/{rate:.2f} -i {fmt}  -c:v libx264 -r 3 -pix_fmt yuv420p {name}.mp4".format(rate=rate, fmt=fmt, name=name)
    cmd = shlex.split(cmd)
    subprocess.call(cmd)
