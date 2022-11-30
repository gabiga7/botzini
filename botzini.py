import cv2 
import tkinter as tk
from PIL import ImageTk, Image
import socket
import imutils
from struct import pack
import random


yellowLower = (25, 90, 10)
yellowUpper = (64, 255, 255)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host, port = '192.168.178.112', 65000
server_address = (host, port)



#defense poussée max
def get_defense_5():
    point = random.randint(0, 100)
    if 0 <= point <= 14:
        return (2,5)
    elif 14 <= point <= 28:
        return (3,5)
    elif 28 <= point <= 42:
        return (1,4)
    elif 42 <= point <= 56:
        return (2,4)
    elif 56 <= point <= 70:
        return (4,2)
    elif 70 <= point <= 84:
        return (3,2)
    elif 84 <= point <= 88:
        return (3,4)
    elif 88 <= point <= 92:
        return (2,3)
    elif 92 <= point <= 96:
        return (4,3)
    elif 96 <= point <= 100:
        return (1,5)
   
#defense tirée max
def get_defense_1():
    point = random.randint(0, 100)
    if 0 <= point <= 14:
        return (5,2)
    elif 14 <= point <= 28:
        return (5,3)
    elif 28 <= point <= 42:
        return (4,1)
    elif 42 <= point <= 56:
        return (4,2)
    elif 56 <= point <= 70:
        return (2,4)
    elif 70 <= point <= 84:
        return (2,3)
    elif 84 <= point <= 88:
        return (4,3)
    elif 88 <= point <= 92:
        return (3,2)
    elif 92 <= point <= 96:
        return (3,4)
    elif 96 <= point <= 100:
        return (5,1)

#defense milieu
def get_defense_3():
    point = random.randint(0, 100)
    if 0 <= point <= 14:
        return (2,3)
    elif 14 <= point <= 28:
        return (3,2)
    elif 28 <= point <= 42:
        return (2,4)
    elif 42 <= point <= 56:
        return (4,2)
    elif 56 <= point <= 70:
        return (3,1)
    elif 70 <= point <= 84:
        return (1,3)
    elif 84 <= point <= 88:
        return (5,1)
    elif 88 <= point <= 92:
        return (1,5)
    elif 92 <= point <= 96:
        return (4,5)
    elif 96 <= point <= 100:
        return (5,4)

#defense tirée
def get_defense_2():
    point = random.randint(0, 100)
    if 0 <= point <= 16:
        return (5,1)
    elif 16 <= point <= 32:
        return (4,3)
    elif 32 <= point <= 48:
        return (3,2)
    elif 48 <= point <= 64:
        return (3,4)
    elif 64 <= point <= 70:
        return (5,2)
    elif 70 <= point <= 76:
        return (5,3)
    elif 76 <= point <= 82:
        return (4,1)
    elif 82 <= point <= 88:
        return (4,2)
    elif 88 <= point <= 94:
        return (2,4)
    elif 94 <= point <= 100:
        return (2,3)

#defense poussée
def get_defense_4():
    point = random.randint(0, 100)
    if 0 <= point <= 16:
        return (1,5)
    elif 16 <= point <= 32:
        return (3,4)
    elif 32 <= point <= 48:
        return (2,3)
    elif 48 <= point <= 64:
        return (4,3)
    elif 64 <= point <= 70:
        return (2,5)
    elif 70 <= point <= 76:
        return (3,5)
    elif 76 <= point <= 82:
        return (1,4)
    elif 82 <= point <= 88:
        return (2,4)
    elif 88 <= point <= 94:
        return (4,2)
    elif 94 <= point <= 100:
        return (3,2)






def is_none(data):
    if not(is_red(data) or is_yellow(data)):
        return True

def is_yellow(data):
    if data[2] > 200 and data[1] > 200 and data[0] < 150 :
        return True

def is_red(data):
    if data[2] > 200 and data[1] < 150 and data[0] < 150 :
        return True

def ball_position_to_couple(ball_sector):
    if ball_sector == 1:
        return get_defense_1()
    elif ball_sector == 2:
        return get_defense_2()
    elif ball_sector == 3:
        return get_defense_3()
    elif ball_sector == 4:
        return get_defense_4()
    elif ball_sector == 5:
        return get_defense_5()
    else:
        return (1,1)

def which_guard(defense_couple):
    if defense_couple[0]==defense_couple[1]==1:
        return 0
    elif defense_couple[0]<defense_couple[1]:
        if random.randint(0,5) == 0:
            return 0
        else:
            return 1
    elif defense_couple[0]>defense_couple[1]:
        if random.randint(0,5) == 0:
            return 1
        else:
            return 0
    else:
        return 1
   

def def_bar(field, ball_x, img,height,left_end,prev_goal_pos,prev_def_pos,prev_guard,prev_ball_sector):
    precision=18
    if field==0 or precision==0:
        return (1,1),(1,1)
    ball_position=ball_x-left_end
    left_goal_corner=left_end+(field*0.36)
    right_goal_corner=left_end+field-(field*0.36)
    if ball_position<left_goal_corner:
        defense_couple=(0,1)
        guard=0
        return defense_couple,(guard,1)
    elif ball_x>right_goal_corner:
        defense_couple=(5,4)
        guard=1
        return defense_couple,(guard,5)
    goal_length=right_goal_corner-left_goal_corner
    goal_section=goal_length/5
    ball_sector=int((ball_position-left_goal_corner)//goal_section)+1
    if ball_sector==prev_ball_sector:
        if random.randint(0,1) == 0:
            return (prev_goal_pos,prev_def_pos),(prev_guard,prev_ball_sector)
    defense_couple=ball_position_to_couple(ball_sector)
    guard=which_guard(defense_couple)
    return defense_couple,(guard,ball_sector)

def mid_bar(field, ball_x, img,height,left_end):
    precision=18
    ball_position=ball_x-left_end
    relative_sector=int((ball_position/((field/6)/precision))%precision)
    if field==0 or precision==0:
        return 0
    #print("relative_sector=",relative_sector)
    return int(relative_sector)


def get_field(img):
    height,width,_ = img.shape
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
    le=i
    i=median_width
    data = img[median_height,i]
    while not(is_red(data)):
        data = img[median_height,i]
        if i<width-1:
            i+=1
        else:
            break
    rb=i
    field=rb-le
    return field,le

#field,left_end=640,0

previous=1

root = tk.Tk()
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
lmain = tk.Label(root)
lmain.grid()

# Initialize the camera with index 0
cap = cv2.VideoCapture(1)
# Check that we have camera access
# This check is not included in all further examples
if not cap.isOpened():
    lmain.config(text="Unable to open camera: please grant appropriate permission in Pydroid permissions plugin and relaunch.\nIf this doesn't work, ensure that your device supports Camera NDK API: it is required that your device supports non-legacy Camera2 API.", wraplength=lmain.winfo_screenwidth())
    root.mainloop()
else:
    # You can set the desired resolution here
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    ret,frame=cap.read()
    field,left_end=get_field(frame)


def refresh():
    global imgtk
    global previous
    ret, frame = cap.read()
    if not ret:
        # Error capturing frame, try next time
        lmain.after(0, refresh)
        return
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
    prev_goal_pos,prev_def_pos,prev_mid_pos,prev_guard,prev_ball_sector=1,1,1,1,1


    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        midfield=mid_bar(field, center[0], frame,height,left_end)
        defense=def_bar(field,center[0],frame,height,left_end,prev_goal_pos,prev_def_pos,prev_guard,prev_ball_sector)
        goal_pos,def_pos,mid_pos,guard,prev_ball_sector=defense[0][0],defense[0][1],midfield,defense[1][0],defense[1][1]
        if prev_goal_pos!= goal_pos or def_pos!=prev_def_pos or mid_pos!=prev_mid_pos or guard!=prev_guard:
            message=pack('4i',goal_pos,def_pos,mid_pos,guard)
            sock.sendto(message, server_address)
        #t2=time.time()
        #print("p1=",t2-t1)
        # To see the centroid clearly
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 5)
            cv2.imwrite("circled_frame.png", cv2.resize(frame, (int(width / 2), int(height / 2))))
            cv2.circle(frame, center, 5, (0, 0, 255), -1)







    w = lmain.winfo_screenwidth()
    h = lmain.winfo_screenheight()
    cw = frame.shape[0]
    ch = frame.shape[1]
   
    # In portrait, image is rotated
    cw, ch = ch, cw
    if (w > h) != (cw > ch):
        # In landscape, we have to rotate it
        cw, ch = ch, cw
        # Note that image can be upside-down, then use clockwise rotation
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    # Keep aspect ratio
    w = min(cw * h / ch, w)
    h = min(ch * w / cw, h)
    w, h = int(w), int(h)
    # Draw a horizontal red line at the center of the screen
    cv2.line(frame, (0, int(h / 2)), (w, int(h / 2)), (255, 0, 0), 2)
    # Resize to fill the whole screen
    frame = cv2.resize(frame, (w, h), interpolation=cv2.INTER_LINEAR)
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.configure(image=imgtk)
    lmain.update()
    lmain.after(0, refresh)


refresh()
root.mainloop()