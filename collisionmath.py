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


def collision_response(puck1, puck2):
    '''Calculates the final velocities of two colliding pucks '''

    vx1i = puck1.velocity[0]
    vy1i = puck1.velocity[1]
    vx2i = puck2.velocity[0]
    vy2i = puck2.velocity[1]
    m1 =  puck1.mass
    m2 = puck2.mass
    x1,y1 = puck1.position
    x2,y2 = puck2.position
    ki = 0.5 * m1 * (vx1i**2 + vy1i**2) + 0.5 * m2 * (vx2i**2 + vy2i**2)
    kf = elasticity * ki

    const1 = ((2*m2) / (m1 + m2)) * (dot_product([vx1i-vx2i, vy1i-vy2i], [x1-x2, y1-y2])) / (magnitude_squared([x1-x2, y1-y2])+.000001)
    vx1f = vx1i - (const1 * (x1-x2))
    vy1f = vy1i - (const1 * (y1-y2))

    const2 = ((2*m1) / (m1 + m2)) * (dot_product([vx2i-vx1i, vy2i-vy1i], [x2-x1, y2-y1])) / (magnitude_squared([x2-x1, y2-y1])+.000001)
    vx2f = vx2i - (const2 * (x2-x1))
    vy2f = vy2i - (const2 * (y2-y1))

    return [vx1f, vy1f], [vx2f, vy2f]