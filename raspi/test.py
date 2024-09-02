import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
import threading
GPIO.setmode(GPIO.BOARD)

def detect_red_ball(frame):
    
    error= 0 
    estimated_distance = 0
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      
    lower = np.array([0, 100, 0])   
    upper = np.array([6, 255, 255]) 
    
    lower_red = np.array([160, 100, 0])
    upper_red = np.array([180, 255, 255])
    
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    mask2 = cv2.inRange(hsv, lower, upper)
    mask = cv2.bitwise_or(mask1, mask2)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 1000]
    cv2.drawContours(frame, filtered_contours, -1, (0, 255, 0), 2)
    for contours in filtered_contours:
        x, y, w, h = cv2.boundingRect(contours)
        aspect_ratio = float(w) / h
        if 0.8 <= aspect_ratio <= 1.1:
            largest_contour = max(filtered_contours, key=cv2.contourArea)
            
            # Get the moments of the largest contour
            M = cv2.moments(largest_contour)
                
            (x, y), radius = cv2.minEnclosingCircle(largest_contour)
            center = (int(x), int(y))
            radius = int(radius)
            cv2.circle(frame, center, radius, (0, 0, 255), 2)
            if M["m00"] != 0:
                
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])

                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
                
                frame_width = frame.shape[1]
                desired_position = frame_width // 2
                error = cx - desired_position
                print("Error:", error)
                cv2.line(frame, (desired_position, 0), (desired_position, frame.shape[0]), (0, 0, 255), 2)

                focal_length = 1430  # example focal length in pixels
                real_object_size = 19  # example real object size in centimeters
                estimated_distance = (real_object_size * focal_length) / (2 * (largest_contour[0][0][1] - cy))
                estimated_distance = estimated_distance/2
                # Display the estimated distance
                cv2.putText(frame, f"Distance: {estimated_distance:.2f} cm", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return frame,mask,error,estimated_distance

# Interrupt handler function for encoder 1
def encoder1(channel):
    GPIO.setmode(GPIO.BOARD)
    global encoder_val_L
    if GPIO.input(COMP_IN_1) == GPIO.HIGH:
        encoder_val_L += 1
    else:
        encoder_val_L -= 1

    # print(f"Left Motor Encoder : {encoder_val_L}")

# Interrupt handler function for encoder 2
def encoder2(channel):
    GPIO.setmode(GPIO.BOARD)
    global encoder_val_R
    if GPIO.input(COMP_IN_2) == GPIO.HIGH:
        encoder_val_R += 1
    else:
        encoder_val_R -= 1
    
    # print(f"Right Motor Encoder : {encoder_val_R}")


# Initialize camera
cap = cv2.VideoCapture(-1)
PWM_L_PIN = 13
DIR_L_PIN = 15
PWM_R_PIN = 16
DIR_R_PIN = 18
# Motor encoder output pulse per rotation (change as required)
ENC_COUNT_REV = 1300
# Wheel Diameter (in cm):
Dia = 8
# Distance to be travelled (in cm):
Dist = 5
# Encoder output pins
ENC_IN_1 = 35
COMP_IN_1 = 37
ENC_IN_2 = 31
COMP_IN_2 = 33

# Control Parameters
setpoint_L = ((Dist * ENC_COUNT_REV) / (3.142 * Dia))
setpoint_R = ((Dist * ENC_COUNT_REV) / (3.142 * Dia))
current_pos_L = 0
current_pos_R = 0
error_L = 0
error_R = 0
GPIO.setup(ENC_IN_1, GPIO.IN)
GPIO.setup(COMP_IN_1, GPIO.IN)
GPIO.setup(ENC_IN_2, GPIO.IN)
GPIO.setup(COMP_IN_2, GPIO.IN)

GPIO.setup(PWM_L_PIN, GPIO.OUT)
GPIO.setup(DIR_L_PIN, GPIO.OUT)
GPIO.setup(PWM_R_PIN, GPIO.OUT)
GPIO.setup(DIR_R_PIN, GPIO.OUT)


GPIO.output(DIR_L_PIN, GPIO.HIGH)
GPIO.output(DIR_R_PIN, GPIO.LOW)
pwm_L = GPIO.PWM(PWM_L_PIN,100)
pwm_R = GPIO.PWM(PWM_R_PIN,100)

encoder_val_L = 0
encoder_val_R = 0
# Variable for PWM motor speed output
mspeed_L = 0
mspeed_R = 0
base_speed = 30
Kp=1
Kd = 0.1
flag = True
try:
    while True:
        error = 0
        ret, frame = cap.read()
        if not ret:
            break
        # Detect red ball
        past_error = error
        frame,mask,error,distance = detect_red_ball(frame)
        derivative = error - past_error
        Turn = error*Kp + derivative*Kd

        mspeed_L = base_speed + Turn 
        mspeed_R = base_speed - Turn

        if(error == 0):    
            while True:
                if(error != 0):
                    print("hi")
                    flag = False
                    GPIO.output(DIR_L_PIN, GPIO.HIGH)
                    GPIO.output(DIR_R_PIN, GPIO.LOW)
                    break
                else:
                    mspeed_L = 15
                    mspeed_R = 15
                    GPIO.output(DIR_L_PIN, GPIO.HIGH)
                    GPIO.output(DIR_R_PIN, GPIO.HIGH)
                    pwm_L.start(mspeed_L)
                    pwm_R.start(mspeed_R)
                    # time.sleep(0.1)
                    # pwm_L.start(0)
                    # pwm_R.start(0)
                    ret, frame = cap.read()
                    if not ret:
                        break
                    # Detect red ball
                    _,_,error,_ = detect_red_ball(frame)
        
        if (mspeed_L > 60):
            mspeed_L = 60

        if (mspeed_R > 60):
            mspeed_R = 60
            
        if(mspeed_L < 0):
            mspeed_L = base_speed
        
        if(mspeed_R < 0):
            mspeed_R = base_speed

        if ((error < 30 and error > -30) and error != 0):
            # mspeed_L = 0
            # mspeed_R = 0
            # pwm_L.start(mspeed_L)
            # pwm_R.start(mspeed_R)
            # print("stopping aligning")
            # time.sleep(10)
            # # Create threads for interrupt handling
            # encoder_thread_1 = threading.Thread(target=GPIO.add_event_detect, args=(ENC_IN_1, GPIO.RISING, encoder1))
            # encoder_thread_2 = threading.Thread(target=GPIO.add_event_detect, args=(ENC_IN_2, GPIO.RISING, encoder2))
            # # Start interrupt threads
            # encoder_thread_1.start()
            # encoder_thread_2.start()

            # while True:
            #     seek_spd = 50
            #     t1_flag = False
            #     t2_flag = False
            #     current_pos_L = int((encoder_val_L / ENC_COUNT_REV) * 360)
            #     error_L = setpoint_L - current_pos_L
            #     print(f"Left Motor Error: {error_L}")
            #     mspeed_L = int(0.2 * abs(error_L)) + 60
            
            #     if mspeed_L > 100:
            #         mspeed_L = seek_spd
            #     # Control motor based on error
            #     if error_L > 5:
            #         GPIO.output(DIR_L_PIN, GPIO.HIGH)
            #         pwm_L.ChangeDutyCycle(mspeed_L)
            #     elif error_L < -5:
            #         GPIO.output(DIR_L_PIN, GPIO.LOW)
            #         pwm_L.ChangeDutyCycle(mspeed_L)
            #     else:
            #         pwm_L.ChangeDutyCycle(0)
            #         print("Motor L OFF")
            #         encoder_thread_1.join()
            #         t1_flag = True

            #     # CONTROL LOOP FOR RIGHT MOTOR :
            #     current_pos_R = int((encoder_val_R/ ENC_COUNT_REV) * 360)
            #     error_R = setpoint_R - current_pos_R
            #     print(f"Right Motor Error: {error_R}")
            #     # Calculate motor speed
            #     mspeed_R = int(0.2 * abs(error_R)) + 60
            #     if mspeed_R > 100:
            #         mspeed_R = seek_spd = 50
            #     # Control motor based on error
            #     if error_R > 5:
            #         GPIO.output(DIR_R_PIN, GPIO.LOW)
            #         pwm_R.ChangeDutyCycle(mspeed_R)
            #     elif error_R < -5:
            #         GPIO.output(DIR_R_PIN, GPIO.HIGH)
            #         pwm_R.ChangeDutyCycle(mspeed_R)
            #     else:
            #         pwm_R.ChangeDutyCycle(0)
            #         print("Motor R OFF")
            #         encoder_thread_2.join()
            #         t2_flag = True

            #     if (t1_flag and t2_flag):
            #         break
            #     time.sleep(0.01)
            # print("exiting positional control")
            print("stopping aligning")
            print(abs(distance))
            mspeed_L = 15
            mspeed_R = 15
            # time.sleep(2)
            if(abs(distance) < 65 and abs(distance) > 0 ):
                break
        print("PRINTING ERROR")  
        print(error)
        pwm_L.start(mspeed_L)
        pwm_R.start(mspeed_R)
        # print("motor left speed")
        # print(mspeed_L)
        # print("motor right speed")
        # print(mspeed_R)
        # Display the resulting frame
        # cv2.imshow('Red Ball Detection', frame)
        # cv2.imshow('mask Detection', mask)

        # # Break the loop when 'q' is pressed
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break



    # encoder_thread_1.join()
    # encoder_thread_2.join()
    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()
except:
    # encoder_thread_1.join()
    # encoder_thread_2.join()
    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()
