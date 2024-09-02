import RPi.GPIO as GPIO
import tkinter as tk
import math
from tkinter import colorchooser
import time
import cv2

GPIO.setmode(GPIO.BOARD)

enable1Pin = 13 
enable2Pin = 27 
enable3Pin = 33

motor1Pin1 = 14 
motor1Pin2 = 12
motor2Pin1 = 26 
motor2Pin2 = 25
motor3Pin1 = 32
motor3Pin2 = 4

rgbPin = 4
servoPin = 4

GPIO.setup(enable1Pin, GPIO.OUT)
GPIO.setup(enable2Pin, GPIO.OUT)
GPIO.setup(enable3Pin, GPIO.OUT)
GPIO.setup(motor1Pin1, GPIO.OUT)
GPIO.setup(motor1Pin2, GPIO.OUT)
GPIO.setup(motor2Pin1, GPIO.OUT)
GPIO.setup(motor2Pin2, GPIO.OUT)
GPIO.setup(motor3Pin1, GPIO.OUT)
GPIO.setup(motor3Pin2, GPIO.OUT)
GPIO.setup(rgbPin, GPIO.OUT)
GPIO.setup(servoPin, GPIO.OUT)

pwmM1 = GPIO.PWM(enable1Pin,100)
pwmM2 = GPIO.PWM(enable2Pin,100)
pwmM3 = GPIO.PWM(enable3Pin,100)
pwmS1 = GPIO.PWM(servoPin, 100)  # GPIO 17, 50Hz frequency

pwmS1.start(0)
pwmM1.start(0)
pwmM2.start(0)
pwmM3.start(0)

left_rot = False
right_rot = False
rot_speed = 0
camera_on = False

cap = cv2.VideoCapture(-1)

def set_servo_angle(angle):
    # Convert angle to duty cycle
    duty = 2 + (angle / 18)  # Convert angle to duty cycle
    # GPIO.output(17, True)
    pwmS1.ChangeDutyCycle(duty)
    # GPIO.output(17, False)
    # pwmS1.ChangeDutyCycle(0)

while True:
    angle = 0
    set_servo_angle(angle) #getting input from trackbar
    ret, frame = cap.read()
    if not ret:
            break
    
    if camera_on:
        cv2.imshow('Camera Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    while left_rot:
        if rot_speed <= 0:
            GPIO.output(motor1Pin1, GPIO.HIGH)
            GPIO.output(motor1Pin2, GPIO.LOW)
            GPIO.output(motor2Pin1, GPIO.HIGH)
            GPIO.output(motor2Pin2, GPIO.LOW)
            GPIO.output(motor3Pin1, GPIO.HIGH)
            GPIO.output(motor3Pin2, GPIO.LOW)
        pwmM1.start(rot_speed)
        pwmM2.start(rot_speed)
        pwmM3.start(rot_speed)
        rot_speed = rot_speed + 5
    
    while right_rot:
        if rot_speed <= 0:
            GPIO.output(motor1Pin1, GPIO.LOW)
            GPIO.output(motor1Pin2, GPIO.HIGH)
            GPIO.output(motor2Pin1, GPIO.LOW)
            GPIO.output(motor2Pin2, GPIO.HIGH)
            GPIO.output(motor3Pin1, GPIO.LOW)
            GPIO.output(motor3Pin2, GPIO.HIGH)
        
