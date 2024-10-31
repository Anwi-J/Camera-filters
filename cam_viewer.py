import tkinter as tk
import cv2
from PIL import Image, ImageTk

def start_webcam():
    global is_running
    is_running = True
    update()

def stop_webcam():
    global is_running
    is_running = False

def update():
    if is_running:
        ret, frame = cap.read()
        if ret:
            if flip_var.get():
                frame = cv2.flip(frame, 1)
            if gray_var.get():
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if edge_var.get():
                # frame = cv2.edge_detect(frame, edge_var.get())
                frame = cv2.Canny(frame, 210, 310)
            if rotate_var.get() != 0:
                frame = rotate_frame(frame, rotate_var.get())
            if resize_var.get() != 100:
                frame = resize_frame(frame, resize_var.get())
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            photo = ImageTk.PhotoImage(image=img)
            canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            canvas.photo = photo  # Keep a reference to the image to prevent it from being garbage collected
    window.after(10, update)

def rotate_frame(frame, angle):
    h, w = frame.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_frame = cv2.warpAffine(frame, rotation_matrix, (w, h))
    return rotated_frame

def resize_frame(frame, scale_percent):
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    resized_frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
    return resized_frame

def on_closing():
    cap.release()
    window.destroy()

is_running = False

window = tk.Tk()
window.title('Webcam Viewer')

cap = cv2.VideoCapture(0)

flip_var = tk.BooleanVar()
gray_var = tk.BooleanVar()
edge_var = tk.BooleanVar()
rotate_var = tk.IntVar()
resize_var = tk.IntVar()

flip_var.set(True)
gray_var.set(True)
edge_var.set(True)
rotate_var.set(0)
resize_var.set(100)

flip_checkbox = tk.Checkbutton(window, text='Flip', variable=flip_var)
flip_checkbox.pack()

gray_checkbox = tk.Checkbutton(window, text='GrayScale', variable=gray_var)
gray_checkbox.pack()

edge_checkbox = tk.Checkbutton(window, text = 'Edge detection', variable =edge_var)
edge_checkbox.pack()

rotate_label = tk.Label(window, text='Rotation Angle:')
rotate_label.pack()

rotate_scale = tk.Scale(window, from_=0, to=360, orient='horizontal', variable=rotate_var)
rotate_scale.pack()

resize_label = tk.Label(window, text='Resize Percent:')
resize_label.pack()

resize_scale = tk.Scale(window, from_=10, to=200, orient='horizontal', variable=resize_var)
resize_scale.pack()


canvas = tk.Canvas(window)
canvas.pack()

start_button = tk.Button(window, text='Start Webcam', command=start_webcam)
start_button.pack()

stop_button = tk.Button(window, text='Stop Webcam', command=stop_webcam)
stop_button.pack()

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()