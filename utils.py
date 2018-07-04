import colorsys


def generate_palette(n):
    HSV_tuples = [(x * 1.0 / n, 1, 1) for x in range(n)]
    RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
    return list(map(lambda x: '#%02x%02x%02x' % (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), RGB_tuples))
