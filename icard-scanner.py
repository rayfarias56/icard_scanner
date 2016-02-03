#!/usr/bin/python
""" 

"""
from datetime import datetime
import Tkinter as tk
import tkFileDialog
import tkMessageBox
import csv
import time

__author__ = "Raymond Farias"
__email__ = "rayfarias56@gmail.com"
__license__ = "GNU GENERAL PUBLIC LICENSE"
__copyright__ = "Copyright 2016"
__version__ = "1.0"


LENGTH_OF_UIN = 9
NSBE_SCANNER = "NSBE"
SHPE_SCANNER = "SHPE"


# Open an output file. 
file_name = "event_attendance_"+str(datetime.now()).split('.')[0].replace(" ", "_")+".csv"
output_file = open(file_name, "w")
output_csv_writer = csv.writer(output_file)


class MainAppFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent

        # Allow <Return> key to submit. This is for ease of typing and auto submit a scan.
        self.root.bind("<Return>", lambda event: self.submit())
        
        # Initialize window 
        parent.title('iCard Scanner')
        self.centerWindow()


        # Wrapper frame to center all widgets
        centerFrame = tk.Frame(self)


        # Title Text
        tk.Label(centerFrame, text="Scan card or enter UIN",
            font="Helvetica 16 bold").pack(side="top", pady=10)

        # Entry Field
        self.uinInput = tk.StringVar()
        entry = tk.Entry(centerFrame, textvariable=self.uinInput)
        entry.pack(side=tk.TOP, pady=20)
        entry.focus_set()

        # Submit button
        tk.Button(centerFrame, text="Manual Submit", 
            command=lambda: self.submit()).pack(side=tk.TOP, pady=20)
        
        centerFrame.place(anchor=tk.CENTER, relx=0.5, rely=0.45)

        # Adjust to fit attached widgets and use adjusted size to set minimum size
        parent.update()
        parent.minsize(parent.winfo_width(), parent.winfo_height())


    def centerWindow(self):
        window = self.root
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        w = 350
        h = 200
        x = (screen_width - w)/2
        y = (screen_height - (h * 1.5))/2
        window.geometry("%dx%d+%d+%d" % (w, h, x, y))


    def submit(self):
        ''' 
        '''
        raw_uin = self.uinInput.get()

        if not raw_uin: 
            return
        
        self.uinInput.set("")
        uin = self.stripUin(raw_uin)
        if uin is not None: 
            writeUin(uin)


    def stripUin(self, raw_uin):
        if raw_uin == ";E?":
            showSwipeErrorMessage()
            return None

        # If it looks like it's just a manual UIN submission. Assume so. 
        if raw_uin.isdigit() and len(raw_uin) == LENGTH_OF_UIN: 
            writeUin(raw_uin)        
            return
        
        # Some scanners submit two lines, one with school data, one with card data. Ignore school data.
        if "CARDHOLDER/UNIVERSITY" in raw_uin:
            return None

        # Filter input that doesn't look like UIN from a card scanner.
        if raw_uin[0] != ";" or raw_uin[-1] != "?" or "=" not in raw_uin:
            showBadInputMessage()
            return None

        return raw_uin[5:14]


def writeUin(uin):
    output_csv_writer.writerow([uin+", "])
    showSuccessMessage()


def showSuccessMessage():
    tkMessageBox.showinfo(title="Success", message="Attendance Recorded")

def showSwipeErrorMessage():
    tkMessageBox.showerror(title="Swipe Error", message="Try swiping again.")

def showBadInputMessage():
    tkMessageBox.showerror(title="Bad Input Error",
                message="Cannot understand input. You may have selected the wrong scanner type.")


if __name__ == "__main__":
    root = tk.Tk()
    MainAppFrame(root).pack(side="top", fill="both", expand=True)
    root.mainloop()