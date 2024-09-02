# import tkinter as tk
# import math
# from tkinter import colorchooser

# class VirtualJoystick(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("Virtual Joystick")

#         # Add a heading label named "PRIMUS"
#         self.heading_label = tk.Label(self, text="PRIMUS", font=("Arial", 24, "bold"))
#         self.heading_label.pack(pady=10)

#         # Joystick parameters
#         self.canvas_size = 400
#         self.joystick_radius = 100
#         self.knob_radius = 20
#         self.center = (self.canvas_size // 2, self.canvas_size // 2)
#         self.knob_position = self.center

#         # Create the canvas
#         self.canvas = tk.Canvas(self, width=self.canvas_size, height=self.canvas_size, bg="white")
#         self.canvas.pack()

#         # Draw the joystick base and knob
#         self.base = self.canvas.create_oval(
#             self.center[0] - self.joystick_radius, self.center[1] - self.joystick_radius,
#             self.center[0] + self.joystick_radius, self.center[1] + self.joystick_radius,
#             outline="gray", width=3
#         )
#         self.knob = self.canvas.create_oval(
#             self.knob_position[0] - self.knob_radius, self.knob_position[1] - self.knob_radius,
#             self.knob_position[0] + self.knob_radius, self.knob_position[1] + self.knob_radius,
#             fill="red"
#         )

#         # Bind mouse events
#         self.canvas.bind("<Button-1>", self.start_drag)
#         self.canvas.bind("<B1-Motion>", self.dragging)
#         self.canvas.bind("<ButtonRelease-1>", self.stop_drag)

#         # Initialize dragging state
#         self.dragging_state = False

#         # Frame for arrow buttons
#         self.arrow_button_frame = tk.Frame(self)
#         self.arrow_button_frame.pack(pady=10)

#         # Add two buttons with opposite arrow symbols
#         self.left_arrow_button = tk.Button(self.arrow_button_frame, text="←", font=("Arial", 18))
#         self.left_arrow_button.pack(side=tk.LEFT, padx=20)
#         self.left_arrow_button.bind("<ButtonPress-1>", self.left_arrow_pressed)
#         self.left_arrow_button.bind("<ButtonRelease-1>", self.arrow_released)

#         self.right_arrow_button = tk.Button(self.arrow_button_frame, text="→", font=("Arial", 18))
#         self.right_arrow_button.pack(side=tk.RIGHT, padx=20)
#         self.right_arrow_button.bind("<ButtonPress-1>", self.right_arrow_pressed)
#         self.right_arrow_button.bind("<ButtonRelease-1>", self.arrow_released)

#         # Add a label and trackbar for servo control
#         self.servo_label = tk.Label(self, text="Servo Angle: 0°")
#         self.servo_label.pack()
#         self.servo_trackbar = tk.Scale(self, from_=-90, to=90, orient=tk.HORIZONTAL, length=300, command=self.update_servo)
#         self.servo_trackbar.pack()

#         # Add a color wheel button
#         self.color_button = tk.Button(self, text="Pick a Color", command=self.open_color_wheel)
#         self.color_button.pack()

#         # Add a label to display the selected color
#         self.color_label = tk.Label(self, text="Selected Color: None", bg="white", width=20)
#         self.color_label.pack()

#         # Add a Camera Feed button
#         self.camera_button = tk.Button(self, text="Camera Feed", command=self.open_camera_feed)
#         self.camera_button.pack()

#         # Variables for holding state
#         self.hold_state = {"left": False, "right": False}

#     def start_drag(self, event):
#         # Check if the click is inside the knob
#         if self.is_within_knob(event.x, event.y):
#             self.dragging_state = True

#     def dragging(self, event):
#         if self.dragging_state:
#             # Calculate distance from the center
#             dx = event.x - self.center[0]
#             dy = event.y - self.center[1]
#             dist = math.sqrt(dx ** 2 + dy ** 2)

#             # Constrain the knob within the joystick radius
#             if dist <= self.joystick_radius:
#                 self.knob_position = (event.x, event.y)
#             else:
#                 angle = math.atan2(dy, dx)
#                 self.knob_position = (
#                     int(self.center[0] + self.joystick_radius * math.cos(angle)),
#                     int(self.center[1] + self.joystick_radius * math.sin(angle))
#                 )

#             # Update the knob position
#             self.update_knob_position()
#             self.print_joystick_values()

#     def stop_drag(self, event):
#         self.dragging_state = False
#         # Reset knob to center
#         self.knob_position = self.center
#         self.update_knob_position()
#         self.print_joystick_values()

#     def is_within_knob(self, x, y):
#         dx = x - self.knob_position[0]
#         dy = y - self.knob_position[1]
#         return math.sqrt(dx ** 2 + dy ** 2) <= self.knob_radius

#     def update_knob_position(self):
#         self.canvas.coords(
#             self.knob,
#             self.knob_position[0] - self.knob_radius, self.knob_position[1] - self.knob_radius,
#             self.knob_position[0] + self.knob_radius, self.knob_position[1] + self.knob_radius
#         )

#     def print_joystick_values(self):
#         # Calculate joystick direction values (X and Y)
#         dx = self.knob_position[0] - self.center[0]
#         dy = self.knob_position[1] - self.center[1]
#         direction = (dx / self.joystick_radius, dy / self.joystick_radius)
#         print(f'Joystick Values - X: {direction[0]:.2f}, Y: {direction[1]:.2f}')

#     def update_servo(self, value):
#         # Update the label with the current servo angle
#         self.servo_label.config(text=f"Servo Angle: {value}°")
#         print(f'Servo Angle: {value}°')

#     def open_color_wheel(self):
#         # Open the color chooser dialog
#         color = colorchooser.askcolor(title="Choose a Color")
#         if color[1]:
#             # Update the background of the entire window to the selected color
#             self.config(bg=color[1])
#             # Update other widgets to match the new background
#             self.canvas.config(bg=color[1])
#             self.servo_label.config(bg=color[1])
#             self.color_button.config(bg=color[1])
#             self.color_label.config(bg=color[1])
#             self.camera_button.config(bg=color[1])  # Update camera button background color
#             self.heading_label.config(bg=color[1])  # Update heading background color
#             self.left_arrow_button.config(bg=color[1])  # Update left arrow button background color
#             self.right_arrow_button.config(bg=color[1])  # Update right arrow button background color
#             print(f'Selected Color: {color[1]}')

#     def open_camera_feed(self):
#         # Placeholder function for camera feed
#         print("Camera Feed button clicked")

#     def left_arrow_pressed(self, event):
#         self.hold_state["left"] = True
#         self.hold_left_arrow()

#     def right_arrow_pressed(self, event):
#         self.hold_state["right"] = True
#         self.hold_right_arrow()

#     def arrow_released(self, event):
#         self.hold_state["left"] = False
#         self.hold_state["right"] = False

#     def hold_left_arrow(self):
#         if self.hold_state["left"]:
#             print("Left arrow button held RPi.GPIOdown")
#             self.after(100, self.hold_left_arrow)  # Continuously call this function every 100 ms

#     def hold_right_arrow(self):
#         if self.hold_state["right"]:
#             print("Right arrow button held down")
#             self.after(100, self.hold_right_arrow)  # Continuously call this function every 100 ms

# if __name__ == "__main__":
#     app = VirtualJoystick()
#     app.mainloop()

import tkinter as tk
import math
from tkinter import colorchooser
import cv2

class VirtualJoystick(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Virtual Joystick")

        # Add a heading label named "PRIMUS"
        self.heading_label = tk.Label(self, text="PRIMUS", font=("Arial", 24, "bold"))
        self.heading_label.pack(pady=10)

        # Joystick parameters
        self.canvas_size = 400
        self.joystick_radius = 100
        self.knob_radius = 20
        self.center = (self.canvas_size // 2, self.canvas_size // 2)
        self.knob_position = self.center

        # Create the canvas
        self.canvas = tk.Canvas(self, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.pack()

        # Draw the joystick base and knob
        self.base = self.canvas.create_oval(
            self.center[0] - self.joystick_radius, self.center[1] - self.joystick_radius,
            self.center[0] + self.joystick_radius, self.center[1] + self.joystick_radius,
            outline="gray", width=3
        )
        self.knob = self.canvas.create_oval(
            self.knob_position[0] - self.knob_radius, self.knob_position[1] - self.knob_radius,
            self.knob_position[0] + self.knob_radius, self.knob_position[1] + self.knob_radius,
            fill="red"
        )

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.dragging)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)

        # Initialize dragging state
        self.dragging_state = False

        # Frame for arrow buttons
        self.arrow_button_frame = tk.Frame(self)
        self.arrow_button_frame.pack(pady=10)

        # Add two buttons with opposite arrow symbols
        self.left_arrow_button = tk.Button(self.arrow_button_frame, text="←", font=("Arial", 18))
        self.left_arrow_button.pack(side=tk.LEFT, padx=20)
        self.left_arrow_button.bind("<ButtonPress-1>", self.left_arrow_pressed)
        self.left_arrow_button.bind("<ButtonRelease-1>", self.arrow_released)

        self.right_arrow_button = tk.Button(self.arrow_button_frame, text="→", font=("Arial", 18))
        self.right_arrow_button.pack(side=tk.RIGHT, padx=20)
        self.right_arrow_button.bind("<ButtonPress-1>", self.right_arrow_pressed)
        self.right_arrow_button.bind("<ButtonRelease-1>", self.arrow_released)

        # Add a label and trackbar for servo control
        self.servo_label = tk.Label(self, text="Servo Angle: 0°")
        self.servo_label.pack()
        self.servo_trackbar = tk.Scale(self, from_=-90, to=90, orient=tk.HORIZONTAL, length=300, command=self.update_servo)
        self.servo_trackbar.pack()

        # Add a color wheel button
        self.color_button = tk.Button(self, text="Pick a Color", command=self.open_color_wheel)
        self.color_button.pack()

        # Add a label to display the selected color
        self.color_label = tk.Label(self, text="Selected Color: None", bg="white", width=20)
        self.color_label.pack()

        # Add a Camera Feed button
        self.camera_button = tk.Button(self, text="Camera Feed", command=self.open_camera_feed)
        self.camera_button.pack()

        # Variables for holding state
        self.hold_state = {"left": False, "right": False}
        self.camera_active = False  # Flag to track camera state
        self.cap = None  # Video capture object

    def start_drag(self, event):
        # Check if the click is inside the knob
        if self.is_within_knob(event.x, event.y):
            self.dragging_state = True

    def dragging(self, event):
        if self.dragging_state:
            # Calculate distance from the center
            dx = event.x - self.center[0]
            dy = event.y - self.center[1]
            dist = math.sqrt(dx ** 2 + dy ** 2)

            # Constrain the knob within the joystick radius
            if dist <= self.joystick_radius:
                self.knob_position = (event.x, event.y)
            else:
                angle = math.atan2(dy, dx)
                self.knob_position = (
                    int(self.center[0] + self.joystick_radius * math.cos(angle)),
                    int(self.center[1] + self.joystick_radius * math.sin(angle))
                )

            # Update the knob position
            self.update_knob_position()
            self.print_joystick_values()

    def stop_drag(self, event):
        self.dragging_state = False
        # Reset knob to center
        self.knob_position = self.center
        self.update_knob_position()
        self.print_joystick_values()

    def is_within_knob(self, x, y):
        dx = x - self.knob_position[0]
        dy = y - self.knob_position[1]
        return math.sqrt(dx ** 2 + dy ** 2) <= self.knob_radius

    def update_knob_position(self):
        self.canvas.coords(
            self.knob,
            self.knob_position[0] - self.knob_radius, self.knob_position[1] - self.knob_radius,
            self.knob_position[0] + self.knob_radius, self.knob_position[1] + self.knob_radius
        )

    def map_value(self, value, min1, max1, min2, max2):
        return (value - min1) * (max2 - min2) / (max1 - min1) + min2

    def calculate_motor_values(self, nJoyX, nJoyY):
        motor_cal1 = (-0.333 * nJoyX) + (-0.577 * nJoyY) + (0.333 * 0)
        motor_cal2 = (-0.333 * nJoyX) + (0.577 * nJoyY) + (0.333 * 0)
        motor_cal3 = (0.666 * nJoyX) + (0 * nJoyY) + (0.333 * 0)
        
        motor_s1 = self.map_value(motor_cal1, -92, 92, -255, 255)
        motor_s2 = self.map_value(motor_cal2, -92, 92, -255, 255)
        motor_s3 = self.map_value(motor_cal3, -67, 67, -255, 255)

        return round(motor_s1), round(motor_s2), round(motor_s3)

    
    def print_joystick_values(self):
            # Calculate joystick direction values (X and Y)
            dx = self.knob_position[0] - self.center[0]
            dy = self.knob_position[1] - self.center[1]
            direction = (dx / self.joystick_radius, dy / self.joystick_radius)
            x_val = (direction[0]*100)
            y_val = (direction[1]*100)
            motor_s1, motor_s2, motor_s3 = self.calculate_motor_values(x_val, y_val)
            # print(f'Joystick Values - X: {direction[0]:.2f}, Y: {direction[1]:.2f}')
            print(f'Joystick Values - X: {x_val:.2f}, Y: {y_val:.2f}')
            print(f'Motor Values - M1: {motor_s1}, M2: {motor_s2}, M3: {motor_s3}')


    def update_servo(self, value):
        # Update the label with the current servo angle
        self.servo_label.config(text=f"Servo Angle: {value}°")
        print(f'Servo Angle: {value}°')

    def open_color_wheel(self):
        # Open the color chooser dialog
        color = colorchooser.askcolor(title="Choose a Color")
        if color[1]:
            # Update the background of the entire window to the selected color
            self.config(bg=color[1])
            # Update other widgets to match the new background
            self.canvas.config(bg=color[1])
            self.servo_label.config(bg=color[1])
            self.color_button.config(bg=color[1])
            self.color_label.config(bg=color[1])
            self.camera_button.config(bg=color[1])  # Update camera button background color
            self.heading_label.config(bg=color[1])  # Update heading background color
            self.left_arrow_button.config(bg=color[1])  # Update left arrow button background color
            self.right_arrow_button.config(bg=color[1])  # Update right arrow button background color
            print(f'Selected Color: {color[1]}')

    def open_camera_feed(self):
        if not self.camera_active:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("Error: Cannot open camera")
                return
            self.camera_active = True
            self.show_camera_feed()
        else:
            self.camera_active = False
            if self.cap is not None:
                self.cap.release()
                cv2.destroyAllWindows()

    def show_camera_feed(self):
        if self.camera_active:
            ret, frame = self.cap.read()
            if ret:
                cv2.imshow("Camera Feed", frame)
                cv2.waitKey(1)
            self.after(10, self.show_camera_feed)  # Continue showing feed

    def left_arrow_pressed(self, event):
        self.hold_state["left"] = True
        self.hold_left_arrow()

    def right_arrow_pressed(self, event):
        self.hold_state["right"] = True
        self.hold_right_arrow()

    def arrow_released(self, event):
        self.hold_state["left"] = False
        self.hold_state["right"] = False

    def hold_left_arrow(self):
        if self.hold_state["left"]:
            print("Left arrow button held down")
            self.after(100, self.hold_left_arrow)  # Continuously call this function every 100 ms

    def hold_right_arrow(self):
        if self.hold_state["right"]:
            print("Right arrow button held down")
            self.after(100, self.hold_right_arrow)  # Continuously call this function every 100 ms

if __name__ == "__main__":
    app = VirtualJoystick()
    app.mainloop()
