import os
import matplotlib.pyplot as plt
import xlrd
import tkinter as tk
import subprocess
from tkinter import filedialog as fd
from matplotlib.dates import DateFormatter


###############################
#   VARIABLES AND FUNCTIONS   #
###############################

workdirpath = os.getcwd()
global fileslist


font = {'family': 'sans-serif',
        'color': 'black',
        'weight': 'bold',
        'size': 16,
        }


def floathourtotime(fh):
    hours, hourseconds = divmod(fh, 1)
    minutes, seconds = divmod(hourseconds * 60, 1)
    return (
        int(hours),
        int(minutes),
        int(seconds * 60)
    )


def openfile():
    global fileslist
    fileslist = fd.askopenfilenames(filetypes=[("All Files", "*.*")])
    labels = [file1_label, file2_label, file3_label, file4_label, file5_label,
              file6_label, file7_label, file8_label, file9_label, file10_label]

    for i in range(10):
        labels[i].configure(text=fileslist[i], bg="gainsboro")


def concatenate()->None:
    button_cat.configure(text="No input files!", fg="white", bg="red")
    outxt = outname_field.get(0.0,"end-1c")
    comtxt = comment_field.get(0.0,"end-1c")
    c_prog = os.path.join(workdirpath,"c","combpy.exe")
    arguments = [c_prog,outxt,comtxt]
    for i in fileslist:
        arguments.append(i)
    p = subprocess.call(arguments)
    if(p==0):
        button_cat.configure(text="Done!", bg="green")
    elif(p==1):
        button_cat.configure(text="Failed! (input error)", bg="red", fg="white")
    elif(p==2):
        button_cat.configure(text="Failed! (output error)", bg="red", fg="white")
    else:
        button_cat.configure(text="Failed! (unknown error)", bg="red", fg="white")


def combthrough():
    outxt = outname_field.get(0.0,"end-1c")
    c_prog = os.path.join(workdirpath,"c","pyac.exe")
    arguments = [c_prog,outxt]
    p = subprocess.call(arguments)
    if(p==0):
        button_comb.configure(text="Combing successfull, no problems!", bg="green", fg="white")
    elif(p==1):
        button_comb.configure(text="Combing successfull, log file opened!", bg="blue", fg="white")
        os.startfile("errors.txt")
    else:
        button_comb.configure(text="Failed! (output not found)", bg="red", fg="white")


def graphit():
    outxt = outname_field.get(0.0, "end-1c")
    c_prog = os.path.join(workdirpath,"c","prep.exe")
    arguments = [c_prog,outxt]
    p = subprocess.call(arguments)
    if(p==0):
        button_graphit.configure(text="Moing average done.", fg="white", bg="blue")
    else:
        button_graphit.configure(text="Failed! (output not found)", bg="red", fg="white")
    c_prog = os.path.join(workdirpath,"c","limit.exe")

    arguments = [c_prog,hspinbox.get(),vspinbox.get(),finspinbox.get()]
    print(arguments)
    p = subprocess.call(arguments)
    if(p==0):
        button_graphit.configure(text="Plotting.", fg="white", bg="green")
    else:
        button_graphit.configure(text="Failed! (data file not found)", bg="red", fg="white")
    data = os.path.join(workdirpath,"150avg.dat")
    limit = os.path.join(workdirpath,"limit.dat")
    xl = []
    yl = []
    for llines in open(limit, "r"):
        llines = [i for i in llines.split()]
        xl.append(float(llines[0]))
        yl.append(float(llines[1]))
    x = []
    y = []
    for line in open(data, "r"):
        lines = [i for i in line.split()]
        x.append(float(lines[0]))
        y.append(float(lines[1]))
    pydate = []
    pydate2 = []
    for i in x:
        pydate.append(xlrd.xldate_as_datetime(i,0))
    for i in xl:
        pydate2.append(xlrd.xldate_as_datetime(i,0))
    fig = plt.figure()
    fig.set_figheight(5)
    fig.set_figwidth(10)
    fig.set_dpi(100)
    ax1 = fig.add_subplot(111)
    comtxt = comment_field.get(0.0, "end-1c")
    titlestring= "Felterhelési sebesség ellenőrzése blokk induláskor " + comtxt
    ax1.set_title(titlestring, fontdict=font)
    ax1.set_xlabel('Idő', fontdict=font)
    ax1.set_ylabel('Teljesítmény (MW)', fontdict=font)
    ax1.plot(pydate, y, c="b", label="150 rolling average")
    ax1.plot(pydate2, yl, c="r", label="Limit")
    ax1.minorticks_on()
    ax1.tick_params(which="both", right=True, top=True)
    date_form = DateFormatter("%y-%m-%d\n%H:%M")
    ax1.xaxis.set_major_formatter(date_form)
    fig.tight_layout()
    plt.show()





#######################
#   WINDOW ELEMENTS   #
#######################
if __name__ == "__main__":

    window = tk.Tk()

    window.title("FELL")

    window.geometry("1200x800")

    window.config(background = "white")

    window.grid_rowconfigure( 0, weight=1)
    window.grid_rowconfigure(1, weight=1)
    window.grid_rowconfigure(2, weight=1)
    window.grid_rowconfigure(3, weight=1)
    window.grid_rowconfigure(4, weight=1)
    window.grid_rowconfigure(5, weight=1)
    window.grid_rowconfigure(6, weight=1)
    window.grid_rowconfigure(7, weight=1)
    window.grid_rowconfigure(8, weight=1)
    window.grid_rowconfigure(9, weight=1)
    window.grid_rowconfigure(10, weight=1)

    window.grid_columnconfigure( 0, weight=1)
    window.grid_columnconfigure(1, weight=0, minsize=30)
    window.grid_columnconfigure(2, weight=1)

    butyok_frame= tk.Frame(window, bg="white",)

    #################   LABELS   #################

    instruction_label = tk.Label(window, text="Chosen input file(s)", fg="black", bg="white",width=1, height=1)
    outname_label = tk.Label(window, text="Output path and name", fg="black", bg="white",width=1, height=1)
    outcomment_label = tk.Label(window, text="Mandatory comment line", fg="black", bg="white")
    xbuty_label = tk.Label(butyok_frame, text="x bizgere (idő)", fg="black", bg="white")
    ybuty_label = tk.Label(butyok_frame, text="y bizgere (teljesítmény)", fg="black", bg="white")
    nyamnyam_label = tk.Label(butyok_frame, text="(:< Nyamnyam >:)", fg="black", bg="white")

    #chosen files list
    file1_label = tk.Label(window, fg="black", bg="white",width=1, height=1)
    file2_label = tk.Label(window, fg="black", bg="white",width=1, height=1)
    file3_label = tk.Label(window, fg="black", bg="white",width=1, height=1)
    file4_label = tk.Label(window, fg="black", bg="white",width=1, height=1)
    file5_label = tk.Label(window, fg="black", bg="white",width=1, height=1)
    file6_label = tk.Label(window, fg="black", bg="white",width=1, height=1)
    file7_label = tk.Label(window, fg="black", bg="white",width=1, height=1)
    file8_label = tk.Label(window, fg="black", bg="white",width=1, height=1)
    file9_label = tk.Label(window, fg="black", bg="white",width=1, height=1)
    file10_label = tk.Label(window, fg="black", bg="white",width=1, height=1)

    #spacer label



    #################   BUTTONS   #################

    button_explore = tk.Button(window, text="...", command=openfile)
    button_cat = tk.Button(window, text="Weed and combine files", fg="black", command=concatenate)
    button_comb = tk.Button(window, text="Comb output file for irregularities", fg="black", command=combthrough)
    button_graphit = tk.Button(window, text="ZSÁÁÁÁÁÁÁÁÁÁÁ (plot results)", fg="black", command=graphit)

    #################   TEXT INPUT FIELDS   #################

    outname_field = tk.Text(width = 1, height = 1, bg="white", fg="black")
    outname_field.insert(1.0,"D:/felterhelés/kampányok/")
    comment_field = tk.Text(width = 1, height = 1, bg="white", fg="black")


    #################   SPINBOXES   #################

    hspinbox = tk.Spinbox(butyok_frame, from_=-3, to=0, repeatdelay=500, repeatinterval=100, relief="sunken", bg="gainsboro", fg="blue")
    vspinbox = tk.Spinbox(butyok_frame, from_=0, to=3, repeatdelay=500, repeatinterval=100, relief="sunken", bg="gainsboro", fg="blue")
    finspinbox = tk.Spinbox(butyok_frame, from_=15, to=20, repeatdelay=500, repeatinterval=100, relief="sunken", bg="gainsboro", fg="blue")

    ########################
    #   PACKING THE GRID   #
    ########################

    #################   SUBFRAME   #################
    nyamnyam_label.grid(column=0, row=0, sticky="nsew")
    finspinbox.grid(column=1, row=0, sticky="nsew")
    xbuty_label.grid(column=0, row=1, sticky="nsew")
    hspinbox.grid(column=1, row=1, sticky="nsew")
    ybuty_label.grid(column=0, row=2, sticky="nsew")
    vspinbox.grid(column=1, row=2, sticky="nsew")

    #################   ROW 0   #################
    instruction_label.grid(column=0, row=0, sticky="nsew")
    button_explore.grid(column=1, row=0)


    #################   ROW 1   #################
    file1_label.grid(column=0, row=1, sticky="nsew")


    #################   ROW 2   #################
    file2_label.grid(column=0, row=2, sticky="nsew")

    #################   ROW 3   #################
    file3_label.grid(column=0, row=3, sticky="nsew")
    outname_label.grid(column=2, row=3, sticky="nsew")

    #################   ROW 4   #################
    file4_label.grid(column=0, row=4, sticky="nsew")
    outname_field.grid(column=2, row=4, sticky="nsew")

    #################   ROW 5   #################
    file5_label.grid(column=0, row=5, sticky="nsew")
    outcomment_label.grid(column=2, row=5, sticky="nsew")

    #################   ROW 6   #################
    file6_label.grid(column=0, row=6, sticky="nsew")
    comment_field.grid(column=2, row=6, sticky="nsew")

    #################   ROW 7   #################
    file7_label.grid(column=0, row=7, sticky="nsew")
    button_cat.grid(column=2, row=7, sticky="nsew")

    #################   ROW 8   #################
    file8_label.grid(column=0, row=8, sticky="nsew")
    button_comb.grid(column=2, row=8, sticky="nsew")

    #################   ROW 9   #################
    file9_label.grid(column=0, row=9, sticky="nsew")
    butyok_frame.grid(column=2, row=9, sticky="nsew")

    #################   ROW 10   #################
    file10_label.grid(column=0, row=10, sticky="nsew")
    button_graphit.grid(column=2, row=10, sticky="nsew")

    #############################
    #   ZSÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁÁ   #
    #############################

    window.mainloop()

