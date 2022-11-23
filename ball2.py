import RPi.GPIO as GPIO
import time
import cv2
import imutils
import time

greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
yellowLower = (25, 90, 10)
yellowUpper = (64, 255, 255)

vs = cv2.VideoCapture(0)
#vs = cv2.VideoCapture("covos2.mp4")


#Set function to calculate percent from angle
def angle_to_percent (angle) :
    if angle > 180 or angle < 0 :
        return False

    start = 4
    end = 12.5
    ratio = (end - start)/180 #Calcul ratio from angle to percent

    angle_as_percent = angle * ratio

    return start + angle_as_percent

GPIO.setmode(GPIO.BOARD) #Use Board numerotation mode
GPIO.setwarnings(False) #Disable warnings

#Use pin 12 for PWM signal
pwm_gpio = 12
frequence = 50
GPIO.setup(pwm_gpio, GPIO.OUT)
pwm = GPIO.PWM(pwm_gpio, frequence)

#Init at 0°
pwm.start(angle_to_percent(0))
print("test")
time.sleep(1)




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


def print_vertical_line(i,img,height,left_end):
    for j in range (height-1):
        img[j,left_end+i]=[0,0,255]

def print_horizontal_line(i,img,width,height):
    for i in range (width-1):
        img[height//2,i]=[0,0,0]


def bar(field, ball_position, img,height,left_end, previous):
    print("previous=",previous)
    precision=18
    ball_position=ball_position-left_end
    section=field//(5*precision)
    if section==0:
        return 0
    absolute_sector=ball_position//section
    if int(absolute_sector)<0 or int(absolute_sector)>(5*precision):
        return 0

    relative_sector=absolute_sector//5
    if relative_sector!=previous:
        pwm.ChangeDutyCycle(angle_to_percent(relative_sector*10))
        print("canging duty")
    previous=relative_sector
    print("relative_sector=",relative_sector)

    #print("defender absolute alignment",int(section*relative_sector*5))
    #print_vertical_line(int(section*absolute_sector),img,height,left_end)
    return int(relative_sector),previous


def get_field(source=None):
    if source is None:
        camera = cv2.VideoCapture(0)
    else:
        camera = cv2.VideoCapture(source)
    return_value, img = camera.read()

    #cv2.imwrite('redbar.png', img)

    height,width,_ = img.shape
    del(camera)
    median_height = int(height/2)
    median_width = int(width/2)



    i=median_width
    data = img[median_height,i]
    while not(is_red(data)):
        data = img[median_height,i]
        if i>0:
            i-=1
        else:
            break
    #left red bar begin found
    print("left red bar END found at",i)
    le=i
    i=median_width
    data = img[median_height,i]
    while not(is_red(data)):
        data = img[median_height,i]
        if i<width-1:
            i+=1
        else:
            break
    #left red bar end found
    print("right red bar BEGIN found at",i)
    rb=i
    field=rb-le

    print("field=",field)
    #print_horizontal_line(median_height,img,width,height)
    #cv2.imwrite('redbar.png', img)

    return field,le


#field,left_end=get_field("covos2.mp4")
field,left_end=640,0
previous=1 
while True:
    _, frame = vs.read()

    if frame is None:
        break

    #blurred = cv2.blur(frame, (11, 11), 0)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    height, width = frame.shape[:2]
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(hsv, yellowLower, yellowUpper)

    #mask = cv2.inRange(hsv, greenLower, greenUpper)

    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    #mask = cv2.erode(mask, None, iterations=1)
    #mask = cv2.dilate(mask, None, iterations=1)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        _,previous=bar(field, center[0], frame, height,left_end,previous)
        #t2=time.time()
        #print("p1=",t2-t1)
        # To see the centroid clearly
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 5)
            cv2.imwrite("circled_frame.png", cv2.resize(frame, (int(width / 2), int(height / 2))))
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vs.release()
cv2.destroyAllWindows()
pwm.stop()
GPIO.cleanup()
