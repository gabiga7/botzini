import cv2




def is_none(data):
    if not(is_red(data) or is_yellow(data)):
        return True

def is_yellow(data):
    if data[2] > 200 and data[1] > 200 and data[0] < 150 :
        return True

def is_red(data):
    #print(data)
    if data[2] > 200 and data[1] < 150 and data[0] < 150 :
        return True


def print_vertical_line(i,img):
    for j in range (height):
        img[i,j]=[0,0,255]


def bar(field, ball_position, img):
    precision=5
    section=field//(5*precision)
    if section==0:
        return 0
    absolute_sector=ball_position//section
    relative_sector=absolute_sector//5
    #print("defender absolute alignment",int(section*relative_sector*5))
    print_vertical_line(int(section*absolute_sector),img,(255, 0, 0))
    return int(relative_sector)


def get_field():
    camera = cv2.VideoCapture(0)
    return_value, img = camera.read()

    #cv2.imwrite('begin.png', img)

    height,width,_ = img.shape
    del(camera)

    median = int(height/2)



    i=0
    data = img[median,i]
    while is_none(data):
        data = img[median,i]
        if i<width-1:
            i+=1
        else:
            break
    #left red bar begin found
    #print("left red bar BEGIN found at",i)

    while is_red(data):
        data = img[median,i]
        if i<width-1:
            i+=1
        else:
            break
    #left red bar end found
    #print("left red bar END found at",i)

    le=i
    while is_none(data):
        data = img[median,i]
        if i<width-1:
            i+=1
        else:
            break
    #right red bar begin found
    #print("right red bar BEGIN found at",i)

    rb=i
    while is_red(data):
        data = img[median,i]
        if i<width-1:
            i+=1
        else:
            break    
    #right red bar end found
    #print("right red bar END found at",i)

    field=rb-le

    #print("field=",field)

    return field

bar_position=bar(field,ball_position,img)
