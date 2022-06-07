import math

def dot_product(v1, v2):
    '''Returns the dot product of two vectors'''

    return v1[0] * v2[0] + v1[1] * v2[1]


def magnitude_squared(v):
    '''Returns the magnitude squared of a vector'''

    return (v[0]*v[0] + v[1]*v[1])


def subtract_vectors(v1,v2):
    '''Subtracts two vectors'''

    return (v1[0] - v2[0], v1[1] - v2[1])


def get_angle_of_motion(v1,v2):
    '''Returns the angle of motion between two vectors'''

    return math.atan(v2/(v1+.000001))