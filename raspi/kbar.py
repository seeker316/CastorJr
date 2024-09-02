import tkinter as tk
import math

class VirtualJoystick(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Virtual Joystick")

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

        # Add a label and trackbar for servo control
        self.servo_label = tk.Label(self, text="Servo Angle: 0°")
        self.servo_label.pack()
        self.servo_trackbar = tk.Scale(self, from_=-90, to=90, orient=tk.HORIZONTAL, length=300, command=self.update_servo)
        self.servo_trackbar.pack()

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

    def print_joystick_values(self):
        # Calculate joystick direction values (X and Y)
        dx = self.knob_position[0] - self.center[0]
        dy = self.knob_position[1] - self.center[1]
        direction = (dx / self.joystick_radius, dy / self.joystick_radius)
        print(f'Joystick Values - X: {direction[0]:.2f}, Y: {direction[1]:.2f}')

    def update_servo(self, value):
        # Update the label with the current servo angle
        self.servo_label.config(text=f"Servo Angle: {value}°")
        print(f'Servo Angle: {value}°')

if __name__ == "__main__":
    app = VirtualJoystick()
    app.mainloop()
