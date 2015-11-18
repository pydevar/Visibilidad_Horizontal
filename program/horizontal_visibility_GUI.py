#!/usr/bin/env python

__version__ = "Version 1.0"
__copyright__ = "Copyright 2015, PydevAr"
__email__ = "pydev.ar@gmail.com"

import cv2
import sys
from Tkinter import *
from tkFileDialog import askopenfilename
from PIL import Image, ImageTk
import os
import csv

img_path = ""
FILENAME = "save.csv"
refPt = list()


def button_creation():
    but1 = Button(frame, text="Read Image", command=read_img)
    but1.configure(bd=True, highlightthickness=0, activebackground="black")
    but1.grid(row=1, column=1)

    but2 = Button(frame, text="Status Image", command=status_img)
    but2.configure(bd=True, highlightthickness=0, activebackground="red")
    but2.grid(row=2, column=1)

    but3 = Button(frame, text="Show ROI", command=show_roi)
    but3.configure(bd=True, highlightthickness=0, activebackground="yellow")
    but3.grid(row=3, column=1)

    but4 = Button(frame, text="Find Contours", command=find_cont)
    but4.configure(bd=True, highlightthickness=0, activebackground="blue")
    but4.grid(row=4, column=1)

    but5 = Button(frame, text="Show Results", command=show_res)
    but5.configure(bd=True, highlightthickness=0, activebackground="green")
    but5.grid(row=5, column=1)

    but6 = Button(frame, text="Store Coordinates", command=save_values)
    but6.configure(bd=True, highlightthickness=0, activebackground="turquoise")
    but6.grid(row=6, column=1)

    but7 = Button(frame, text="Do All Processes", command=do_all)
    but7.configure(bd=True, highlightthickness=0, activebackground="white")
    but7.grid(row=1, column=2)

    but8 = Button(frame, text="Select ROI", command=select_roi)
    but8.configure(bd=True, highlightthickness=0, activebackground="orange")
    but8.grid(row=2, column=2)

    but9 = Button(frame, text="Read Coordinates", command=read_coord)
    but9.configure(bd=True, highlightthickness=0, activebackground="brown")
    but9.grid(row=3, column=2)

    but10 = Button(frame, text="Next", command=next_id)
    but10.configure(bd=True, highlightthickness=0, activebackground="red")
    but10.grid(row=4, column=2)

    but11 = Button(frame, text="Previous", command=previous_id)
    but11.configure(bd=True, highlightthickness=0, activebackground="blue")
    but11.grid(row=5, column=2)

    but12 = Button(frame, text="Save Changes", command=save_changes)
    but12.configure(bd=True, highlightthickness=0, activebackground="yellow")
    but12.grid(row=6, column=2)


def entry_creation():
    global entrytext1, entrytext2, entrytext3, entrytext4, entrytext5, entrytext6, entrytext7

    label1=Label(root,text="ID Baliza",background=color)
    label1.grid(row=8,column=0, padx=1, pady=1)

    entrytext1 = StringVar()
    E1 = Entry(root, justify='center', textvariable=entrytext1, state="readonly")
    E1.configure(bg="red", readonlybackground=color)
    E1.grid(row=9, column=0, padx=1, pady=1)

    label2=Label(root,text="Coordenada X",background=color)
    label2.grid(row=8,column=1, padx=1, pady=1)

    entrytext2 = StringVar()
    E2 = Entry(root, justify='center', textvariable=entrytext2, state="readonly")
    E2.configure(bg="red", readonlybackground=color)
    E2.grid(row=9, column=1, padx=1, pady=1)

    label3=Label(root,text="Coordenada Y",background=color)
    label3.grid(row=8,column=2, padx=1, pady=1)

    entrytext3 = StringVar()
    E3 = Entry(root, justify='center', textvariable=entrytext3, state="readonly")
    E3.configure(bg="red", readonlybackground=color)
    E3.grid(row=9, column=2, padx=1, pady=1)

    label4=Label(root,text="Valor Pixel",background=color)
    label4.grid(row=8,column=3, padx=1, pady=1)

    entrytext4 = StringVar()
    E4 = Entry(root, justify='center', textvariable=entrytext4, state="readonly")
    E4.configure(bg="red", readonlybackground=color)
    E4.grid(row=9, column=3, padx=1, pady=1)

    label5=Label(root,text="Valor Referencia",background=color)
    label5.grid(row=8,column=4, padx=1, pady=1)

    entrytext5 = StringVar()
    E5 = Entry(root, justify='center', textvariable=entrytext5)
    E5.configure(bg="white", readonlybackground=color)
    E5.grid(row=9, column=4, padx=1, pady=1)

    label6=Label(root,text="Seleccionado",background=color)
    label6.grid(row=8,column=5, padx=1, pady=1)

    entrytext6 = StringVar()
    E6 = Entry(root, justify='center', textvariable=entrytext6)
    E6.configure(bg="white", readonlybackground=color)
    E6.grid(row=9, column=5, padx=1, pady=1)

    label7=Label(root,text="Distancia",background=color)
    label7.grid(row=8,column=6, padx=1, pady=1)

    entrytext7 = StringVar()
    E7 = Entry(root, justify='center', textvariable=entrytext7)
    E7.configure(bg="white", readonlybackground=color)
    E7.grid(row=9, column=6, padx=1, pady=1)


def openfile():
    global img_path
    filename = askopenfilename(parent=root)
    img_path = filename
    print img_path


def read_img():
    global img_path, img, clone
    # Reading image
    img = cv2.imread(img_path, cv2.CV_LOAD_IMAGE_UNCHANGED)
    clone = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    try:
        img.shape
    except:
        print "The image could not be loaded."
        return None, None
        # sys.exit()  # Exit when error
    print "The image has been read successfully"
    return img, clone


def status_img():
    global img
    print "OpenCV Version:", cv2.__version__
    print "-"*5, "Information of the image", "-"*5
    print "Image Shape:", img.shape
    print "Total number of pixels:", img.size
    print "Image data type:", img.dtype


def get_roi():
    global roi, refPt
    if not refPt:
        refPt = [(1148, 1124), (2569, 1452)]
    roi = img[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]


def show_roi():
    global img, roi, refPt
    get_roi()
    cv2.imshow("roi", roi)
    cv2.waitKey(0)


def find_cont():
    global roi, result, clone, refPt

    result = roi.copy()
    clone = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    # cv2.imshow("clone", clone)

    _dummy, b_clone = cv2.threshold(clone, 200, 255, cv2.THRESH_BINARY)
    # cv2.imshow("b_clone", b_clone)
    # cv2.waitKey(0)

    contours, _h = cv2.findContours(b_clone, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # print contours

    id = 0
    for blob in contours:
        # finding centroids of best_cnt and draw a rectangle there
        if blob is not None:
            x, y, w, h = cv2.boundingRect(blob)
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 0, 255), 3)

        M = cv2.moments(blob)
        if M['m00'] != 0:
            cx, cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
            dict_values[id] = [cx, cy, average_value(roi, cx, cy)]
            id += 1


def show_res():
    global roi, result

    cv2.imshow("ROI", roi)
    cv2.imshow("result", result)
    cv2.waitKey(0)


def store_data():
    global writer, csvfile
    csvfile = open(FILENAME, 'wb')
    if not os.path.isfile(FILENAME):
        print "Error: file %s doesn't exist." % FILENAME
    csvfile.write("sep=,\n")  # For excel compatibility
    FIELDNAMES = ['ID Baliza',
                  'Coordenada X',
                  'Coordenada Y',
                  'Valor Pixel',
                  'Valor Referencia',
                  'Seleccionado',
                  'Distancia']
    writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
    writer.writeheader()


def save_coord(id, cx, cy, pixel, reference=' ', selected=' ', distance=' '):
    global writer
    try:
        writer.writerow({
            'ID Baliza': id,
            'Coordenada X': int(cx) + refPt[0][0],
            'Coordenada Y': int(cy) + refPt[0][1],
            'Valor Pixel': pixel,
            'Valor Referencia': reference,
            'Seleccionado': selected,
            'Distancia': distance
            })
    except ValueError as er:
        print "Problem writing file.", er


def average_value(image, cx, cy):
    global refPt
    image1, image2, image3 = [0, 0, 0]
    # print "cx:", cx, "cy:", cy
    counter = 0.0
    for x in range(cx-2, cx+3):
        for y in range(cy-2, cy+3):
            counter += 1.0
            # print x, y, image[y][x]
            image1 += image[y][x][0]
            image2 += image[y][x][1]
            image3 += image[y][x][2]
    ret = " ".join([
        str(round(image1 / counter, 1)),
        str(round(image2 / counter, 1)),
        str(round(image3 / counter, 1))])
    # print "returns", ret
    return ret


def save_values():
    store_data()
    for i in range(len(dict_values.keys())):
        save_coord(i, *dict_values[i])
    csvfile.close()
    print "The coordinates have been stored."


def do_all():
    global img_path
    if img_path == "":
        img_path = "../cam1/3.jpg"
        print "Default Image =", img_path
    else:
        print "Image =", img_path

    read_img()
    get_roi()
    find_cont()
    store_data()
    save_values()


def select_roi():
    global img, resized
    size = (img.shape[1]//4, img.shape[0]//4)
    resized = cv2.resize(img, size)
    resized_clone = resized.copy()
    cv2.namedWindow("resized")
    cv2.setMouseCallback("resized", click_and_crop)
    cv2.imshow("resized", resized)

    key = cv2.waitKey(1) & 0xFF

    # if the 'r' key is pressed, reset the cropping region
    if key == ord("r"):
        resized = resized_clone.copy()


def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, resized
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x*4, y*4)]

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x*4, y*4))

        # draw a rectangle around the region of interest
        cv2.rectangle(resized, (refPt[0][0]//4, refPt[0][1]//4), (refPt[1][0]//4, refPt[1][1]//4), (0, 255, 0), 2)
        cv2.imshow("resized", resized)
        print "The coordinates are (%i, %i) (%i, %i)" %(refPt[0][0], refPt[0][1], refPt[1][0], refPt[1][1])


def read_coord():
    global coord, global_id, entrytext1, entrytext2, entrytext3, entrytext4, entrytext5, entrytext6, entrytext7
    txt_path = "save.csv"
    try:
        f = open(txt_path)
    except:
        print "Error: The text file could not be found"
        sys.exit()
    lines = f.readlines()
    f.close()
    coord = list()  # All the coordinates will be stored in this list.

    for line in lines:
        if line.startswith("sep") or line.startswith("ID"):
            continue
        # print "line", line
        column = line.split(',')
        column[1] = str(int(column[1]) - refPt[0][0])
        column[2] = str(int(column[2]) - refPt[0][1])
        coord.append(column)
        # coord.append([int(float(column[2])), int(float(column[3]))])  # The columns 2 and 3 are appended to coord list
    # print "The coordinates are:", coord
    # print coord[0]
    global_id = 0
    show_coord()


def show_coord():
    global global_id
    entrytext1.set(coord[global_id][0])
    entrytext2.set(coord[global_id][1])
    entrytext3.set(coord[global_id][2])
    entrytext4.set(coord[global_id][3])
    entrytext5.set(coord[global_id][4])
    entrytext6.set(coord[global_id][5])
    entrytext7.set(coord[global_id][6])


def next_id():
    global global_id  # Solve for global_id > max
    write_coord()
    global_id += 1
    show_coord()
    actual_coord()


def previous_id():
    global global_id
    write_coord()
    global_id -= 1
    if global_id < 0:
        global_id = 0
    show_coord()
    actual_coord()


def actual_coord():
    global global_id, roi
    cloned = roi.copy()
    cv2.circle(cloned, (int(coord[global_id][1]), int(coord[global_id][2])), 10, (80, 80, 200), 5)
    cv2.imshow("actual_coord", cloned)


def write_coord():
    coord[global_id][4] = entrytext5.get()
    coord[global_id][5] = entrytext6.get()
    coord[global_id][6] = entrytext7.get()


def save_changes():
    store_data()
    for i in range(len(coord)):
        save_coord(*coord[i])
    csvfile.close()
    print "The coordinates have been stored."


dict_values = dict()
root = Tk()
root.wm_title("Horizontal Visibility")
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
root.geometry("+%d+%d" % (x, y))
root.deiconify()
root.resizable(False,False)
icon = (r'PaR.ico')
root.iconbitmap(icon)
color = "#535353"
acbgcolor="#eceefb"
root.configure(background=color)

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Select Image", command=openfile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Menu", menu=filemenu)

# Frame that contains the buttons
frame = Frame(root)
frame.grid(row=5, pady=10)

button_creation()
entry_creation()
root.config(menu=menubar)
root.mainloop()

print "The program ended successfully."