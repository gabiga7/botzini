import numpy as np
from PIL import Image

def is_white(data):
    if data==(255,255,255,255):
        return True

def is_black(data):
    if data==(0,0,0,255):
        return True

def is_yellow(data):
    if data==(255,255,0,255):
        return True

def ball_position_from_left(width,height,img):
    for i in range(0,width):# process all pixels
        for j in range(0,height):
            data = img.getpixel((i,j))
            if data[0] == 255 and data[1] == 255 and data[2] ==0 :
                return i
    return 0

def ball_position_from_right(width,height,img):
    for i in reversed(range(0,width)):# process all pixels
        for j in reversed(range(0,height)):
            data = img.getpixel((i,j))
            if data[0] == 255 and data[1] == 255 and data[2] ==0 :
                return i
    return 0

def ball_position(width,height,img):
    return (ball_position_from_right(width,height,img)+ball_position_from_left(width,height,img))//2




def print_vertical_line(i,img,color):
    for j in range (height):
        img.putpixel((i,j),color)


def defender_position(field, ball_position, img):
    section=field//15
    absolute_sector=ball_position//section
    relative_sector=absolute_sector//5
    print(int(section*relative_sector*5))
    print_vertical_line(int(section*absolute_sector),img,(255, 0, 0))
    if relative_sector<1.5:
        return 1
    elif relative_sector<2.25:
        return 2
    else:
        return 3





img = Image.open('baby.png')
width = img.size[0] 
height = img.size[1]


print(width,height)
for i in range(0,width):# process all pixels
    for j in range(0,height):
        data = img.getpixel((i,j))
        if data[0] > 200 and data[1] < 100 and data[2] < 100 :
            img.putpixel((i,j),(255, 255, 255))
        elif data[0] > 200 and data[1] > 200 and data[2] < 100 :
            img.putpixel((i,j),(255, 255, 0))
        else :
            img.putpixel((i,j),(0, 0, 0))

median=height/2
i=0
data = img.getpixel((i,median))
while is_black(data):
    data = img.getpixel((i,median))
    i+=1
#left red bar begin found
lb=i
while is_white(data):
    data = img.getpixel((i,median))
    i+=1
#left red bar end found
le=i
while is_black(data):
    data = img.getpixel((i,median))
    i+=1
#right red bar begin found
rb=i
while is_white(data):
    data = img.getpixel((i,median))
    i+=1
#right red bar end found
re=i

field=rb-le



ball=ball_position(width,height,img)
print("ball=",ball)
print_vertical_line(ball,img,(255, 255, 0))
print(defender_position(field,ball,img))
img.show()
img.save("vf.png")

