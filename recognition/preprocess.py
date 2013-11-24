from PIL import Image


def image_to_array(image, func=None):
    return map(func, list(image.getdata())) if func else list(image.getdata())


def image_to_2d_array(image, func=None):
    seq = image_to_array(image, func)
    width = image.size[0]

    for i in xrange(0, len(seq), width):
        yield seq[i:i + width]

img = Image.open("/Users/piotrekd/workspace/scribeserver/recognition/8.jpg")


import pdb; pdb.set_trace()  # XXX BREAKPOINT
a = list(image_to_2d_array(img, lambda p: 1.0 - (sum(p) / 3.0 / 255)))
