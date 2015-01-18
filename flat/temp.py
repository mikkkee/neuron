import llrbt
reload(llrbt)
from sweepline import Segment, Point, SweepLine
from analyzer import have_intersection, analyze


p1 = Point((395.4622, 1949.9093))
p2 = Point((392.0275, 1941.7096))

p3 = Point((392.0275, 1941.7096))
p4 = Point((392.1036, 1946.7090))

p5 = Point((392.0275, 1941.7096))
p6 = Point((395.7875, 1945.0054))

p7 = Point((579.2792, 1979.6996))
p8 = Point((632.2275, 2006.3218))
p9 = Point((632.2275, 2006.3218))
p10 = Point((635.9299, 2009.6821))
p11 = Point((632.2275, 2006.3218))
p12 = Point((637.0581, 2007.6121))


s1 = Segment(p1, p2, 0)
s2 = Segment(p3, p4, 0)
s3 = Segment(p5, p6, 0)

s4 = Segment(p7, p8, 1)
s5 = Segment(p9, p10, 1)
s6 = Segment(p11, p12, 1)

n1 = [s1, s2, s3]
n2 = [s4, s5, s6]


# print "Intersections: {}".format(have_intersection(n1, n2))

with open('test.txt', 'r') as f:
    print "connections : {}".format(analyze(f))
'''
DELETING #(632.222,2006.332)->(635.930,2009.682)#,BLACK,False,False, with key #(632.222,2006.332)->(635.930,2009.682)#, f
rom [#(632.222,2006.332)->(635.930,2009.682)#,BLACK,False,False, #(632.224,2006.327)->(637.058,2007.612)#,BLACK,True,False]
'''
