import numpy as np
from PIL import Image
import time

def is_none(data):
    if not(is_red(data) or is_yellow(data)):
        return True

def is_yellow(data):
    if data[0] > 200 and data[1] > 200 and data[2] < 100 :
        return True

def is_red(data):
    if data[0] > 200 and data[1] < 100 and data[2] < 100 :
        return True

def ball_position_from_left(width,height,img):
    for i in range(0,width):# process all pixels
        for j in range(0,height):
            data = img.getpixel((i,j))
            if is_yellow(data):
                return i
    return 0

def ball_position_from_right(width,height,img):
    for i in reversed(range(0,width)):# process all pixels
        for j in reversed(range(0,height)):
            data = img.getpixel((i,j))
            if is_yellow(data):
                return i
    return 0

def ball_position(width,height,img):
    #return (ball_position_from_right(width,height,img)+ball_position_from_left(width,height,img))//2
    return ball_position_from_right(width,height,img)




def print_vertical_line(i,img,color):
    height = img.size[1]
    for j in range (height):
        img.putpixel((i,j),color)


def bar(field, ball_position, img):
    section=field//15
    absolute_sector=ball_position//section
    relative_sector=absolute_sector//5
    print("defender absolute alignment",int(section*relative_sector*5))
    print_vertical_line(int(section*absolute_sector),img,(255, 0, 0))
    if relative_sector<1.5:
        return 1
    elif relative_sector<2.25:
        return 2
    else:
        return 3


def main():
    start_time = time.time()
    

    img = Image.open('baby.png')
    width = img.size[0] 
    height = img.size[1]
    print("image size=",width,"x",height)

    """for i in range(0,width):# process all pixels
        for j in range(0,height):
            data = img.getpixel((i,j))
            if data[0] > 200 and data[1] < 100 and data[2] < 100 :
                img.putpixel((i,j),(255, 255, 255))
            elif data[0] > 200 and data[1] > 200 and data[2] < 100 :
                img.putpixel((i,j),(255, 255, 0))
            else :
                img.putpixel((i,j),(0, 0, 0))"""

    median=height/2
    i=0
    data = img.getpixel((i,median))
    while is_none(data):
        data = img.getpixel((i,median))
        i+=1
    #left red bar begin found
    while is_red(data):
        data = img.getpixel((i,median))
        i+=1
    #left red bar end found
    le=i
    while is_none(data):
        data = img.getpixel((i,median))
        i+=1
    #right red bar begin found
    rb=i
    while is_red(data):
        data = img.getpixel((i,median))
        i+=1
    #right red bar end found

    field=rb-le
    print("rb=",rb,"le=",le,"field=",field)


    ball=ball_position(width,height,img)
    print("ball absolute alignment=",ball)
    print_vertical_line(ball,img,(255, 255, 0))
    bar_position=bar(field,ball,img)
    print("bar position",bar_position)
    print("--- %s seconds ---" % (time.time() - start_time))

    img.show()
    img.save("vf.png")

main()