import numpy as np
import cv2 as cv
from PIL import Image


def is_none(data):
    if not(is_red(data) or is_yellow(data)):
        return True

def is_yellow(data):
    if data[0] > 200 and data[1] > 200 and data[2] < 150 :
        return True

def is_red(data):
    #print(data)
    if data[0] > 200 and data[1] < 100 and data[2] < 100 :
        return True

def ball_position_from_left(width,height,img):
    for i in range(0,width):# process all pixels
        for j in range(0,height):
            data = img.getpixel((i,j))
            if is_yellow(data):
                print("ball found at",i)
                return i
    return 0

def ball_position_from_right(width,height,img):
    for i in reversed(range(0,width)):# process all pixels
        for j in reversed(range(0,height)):
            data = img.getpixel((i,j))
            if is_yellow(data):
                return i
    return 0

def ball(width,height,img):
    #return (ball_position_from_right(width,height,img)+ball_position_from_left(width,height,img))//2
    return ball_position_from_right(width,height,img)

def yellow_ball_coordinates(img):
    width = img.size[0] 
    height = img.size[1]
    for i in range(0,width):# process all pixels
        for j in range(0,height):
            data = img.getpixel((i,j))
            if data[0] > 200 and data[1] > 200 and data[2] < 150 :
                print("ball found")
                return i,j
            """else :
                #print("no yellow ball found")
                #img.putpixel((i,j),(200, 200, 0))"""
    return 0,0


def print_vertical_line(i,img,color):
    height = img.size[1]
    for j in range (height):
        img.putpixel((i,j),color)


def bar(field, ball_position, img):
    section=field//15
    if section==0:
        return 0
    absolute_sector=ball_position//section
    relative_sector=absolute_sector//5
    #print("defender absolute alignment",int(section*relative_sector*5))
    print_vertical_line(int(section*absolute_sector),img,(255, 0, 0))
    if relative_sector<1.5:
        return 1
    elif relative_sector<2.25:
        return 2
    else:
        return 3


def main(img):
    

    width = img.size[0] 
    height = img.size[1]
    #print("image size=",width,"x",height)

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
    #print(data)
    while is_none(data):
        data = img.getpixel((i,median))
        if i<width-1:
            i+=1
        else:
            break
    #left red bar begin found
    #print("left red bar BEGIN found at",i)
    while is_red(data):
        data = img.getpixel((i,median))
        if i<width-1:
            i+=1
        else:
            break
    #left red bar end found
    #print("left red bar END found at",i)
    le=i
    while is_none(data):
        data = img.getpixel((i,median))
        if i<width-1:
            i+=1
        else:
            break
    #right red bar begin found
    rb=i
    while is_red(data):
        data = img.getpixel((i,median))
        if i<width-1:
            i+=1
        else:
            break    
    #right red bar end found

    field=rb-le
    print("field=",field)

    #print(yellow_ball_coordinates(img))

    ball_position=ball(width,height,img)
    #print("ball absolute alignment=",ball_position)
    print_vertical_line(ball_position,img,(255, 255, 0))
    bar_position=bar(field,ball_position,img)
    print("bar position",bar_position)

    #img.show()
    #img.save("vf.png")

print('start')
cap = cv.VideoCapture(0)
while(True):
# Capture image par imaghe
    ret, img = cap.read()
    #conversion to PIL
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    main(img)

    #conversion to cv
    img = np.asarray(img)
    img = cv.cvtColor(img, cv.COLOR_RGB2BGR)

    # Préparation de l'affichage de l'image
    cv.imshow('frame',img)
    # affichage et saisie d'un code clavier
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
# Ne pas oublier de fermer le flux et la fenetre
cap.release()
cv.destroyAllWindows()