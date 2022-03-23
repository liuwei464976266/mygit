import keyBoard,time,math
circle_time = 1
def getLoaclPoint(handle):
    pass
def turnAngle(handle,x,y):
    x1,y1 = getLoaclPoint(handle)
    keyBoard.key_down(handle,'w')
    time.sleep(1)
    keyBoard.key_up(handle,'w')
    x2,y2 = getLoaclPoint(handle)
    angle1 = math.atan(y-y1,x-x1)
    angle2 = int(angle1 * 180 / math.pi)
    angle3 = math.atan(y2 - y1, x2 - x1)
    angle4 = int(angle3 * 180 / math.pi)
    angle = angle4 - angle2
    keyBoard.key_down(handle, 'd')
    time.sleep(circle_time * angle / 360)
    keyBoard.key_up(handle, 'd')
