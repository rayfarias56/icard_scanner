#!/usr/bin/python
""" 

"""
from datetime import datetime
import Tkinter as tk
import tkFileDialog
import tkMessageBox
import csv


__author__ = "Raymond Farias"
__email__ = "rayfarias56@gmail.com"
__license__ = "GNU GENERAL PUBLIC LICENSE"
__copyright__ = "Copyright 2016"
__version__ = "1.0"


# TODO:
# implement nsbe scanner
# clean up and document
# try turning into executable
# version control


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
        tk.Entry(centerFrame, textvariable=self.uinInput).pack(side=tk.TOP, pady=20)

        # Dropdown
        self.scannerMenu = ScannerMenu(centerFrame)
        self.scannerMenu.pack(side="top")

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
        scanner_type = self.scannerMenu.scanner_type.get()
        

        if not raw_uin: 
            return
        self.uinInput.set("")


        if len(raw_uin) == LENGTH_OF_UIN: 
            writeUin(raw_uin)        
            return
            

        if scanner_type == NSBE_SCANNER:
            uin = stripNsbeUin()
        elif scanner_type == SHPE_SCANNER:
            uin = stripShpeUin(raw_uin)

        if uin is not None: 
            writeUin(uin)


class ScannerMenu(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Label
        tk.Label(self, text="Type of Scanner:", font="Helvetica 11 bold").pack(side=tk.LEFT)

        # Dropdown Menu
        choices = [SHPE_SCANNER, NSBE_SCANNER]
        self.scanner_type = tk.StringVar()
        self.scanner_type.set(choices[0])    
        tk.OptionMenu(self, self.scanner_type, *choices).pack(side=tk.LEFT)


# Data Handlers
def writeUin(uin):
    output_csv_writer.writerow([uin+", "])
    showSuccessMessage()


def stripNsbeUin(raw_uin):
    tkMessageBox.showerror(title="Scanner Type Error", message="NSBE scanner not implemented")
    return None

    if raw_uin == ";E?":
        showSwipeErrorMessage()
        return None
    
    if raw_uin[0] != ";" or raw_uin[-1] != "?" or "=" not in raw_uin:
        showBadInputMessage()
        return None

    return raw_uin[5:14]


def stripShpeUin(raw_uin):
    if raw_uin == ";E?":
        showSwipeErrorMessage()
        return None
    
    if raw_uin[0] != ";" or raw_uin[-1] != "?" or "=" not in raw_uin:
        showBadInputMessage()
        return None

    return raw_uin[5:14]


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