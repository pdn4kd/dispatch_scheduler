"""
a compilation of multi use funtions
"""
import math


def angular_distance(a1,b1,a2,b2,in_degrees=False):
    if in_degrees:
        a1 = math.radians(a1)
        b1 = math.radians(b1)
        a2 = math.radians(a2)
        b2 = math.radians(b2)
    
    dist = math.acos(math.sin(b1)*math.sin(b2) + math.cos(b1)*math.cos(b2)*\
                         math.cos(a1-a2))
    if in_degrees:
        return math.degrees(dist)
    else:
        return dist


if __name__ == '__main__':
    import ipdb
    ipdb.set_trace()
    a1,b1 = 60.,89.
    a2,b2 = 60.,0.
    print(angular_distance(a1,b1,a2,b2,in_degrees=True))
    ipdb.set_trace()
