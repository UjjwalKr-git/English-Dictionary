from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from backEnd import *
import speech_recognition as sr
import urllib.request
import webbrowser as wb

def is_connected(host):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

def is_float(n):
    try:
        float(n)
        return float(n)
    except ValueError:
        return str(n)
def is_integer(n):
    try:
        int(n)
        return int(n)
    except ValueError:
        return is_float(n)
# switch() is to stop the program from breaking.
def switch(val):
    audioButton["state"] = val

class FileCl:
    def openCMD():
        fileName = askopenfilename(defaultextension=".txt", filetypes=[("Text Documents","*.txt")])
        if fileName == "":
            fileName = None
        else:
            fileInp = ""
            listOut.delete(0,END)
            file = open(fileName,"r")
            flag = 0
            for finp in file:
                if flag == 0:
                    fileInp = finp[0:-1]
                flag = 1
            inputBox.delete(0,END)
            inputBox.insert(END, fileInp)
            mainFunction.link()
            file.close()
    def saveCMD():
        fileName = inp.get()
        saveFile = ""
        if fileName == "":
            showinfo("Smart English Dictionary", "There is NOTHING to Save.")
        else:
            saveFile = asksaveasfilename(initialfile='{}.txt'.format(fileName), defaultextension=".txt",
                                        filetypes=[("Text Documents","*.txt")])
        if saveFile == "":
            saveFile = None
        else:
            file = open(saveFile,"w")
            file.write("{}\nDefinition(s) of \"{}\" is/are :-\n".format(fileName,fileName))
            for out in listOut.get(0,END):
                file.write(" " + out + "\n")
            file.close()

class EditCl:
    def cleraCMD():
        inputBox.delete(0,END)
        listOut.delete(0,END)
        Lab3.config(text = " ")
        Lab4.config(text = " ")
        mainWindow.title("Smart English Dictionary")
    def copyCMD():
        listOut.event_generate("<<Copy>>")
        showinfo("Smart English Dictionary",
                    "The Selected Element has copied to the clipboard.\n\n")
    def pasteCMD():
        inputBox.delete(0,END)
        inputBox.event_generate("<<Paste>>")

class MoreCl:
    def aboutApp():
        prt=askquestion("Smart English Dictionary",
                    "Smart English Dictionary\n v2.5\n  -By Ujjwal Kumar\n Would You Like to visit Developer's Portfolio?")
        if prt == "yes" and is_connected('https://ujjwalhost.github.io'):
            wb.open_new_tab('https://ujjwalhost.github.io/')
        elif prt == "yes" and is_connected('https://ujjwalhost.github.io')==False:
            showerror("Smart English Dictionary", 
                "You are NOT connected to the Internet.\n\nPlease TRY AGAIN after Connecting to The Internet.")
    def updateApp():
        showinfo("Smart English Dictionary",
            " Latest Version - v2.5\n Current Version - v2.5\n Smart English Dictionary is already Up-to-date")

class mainFunction:
    def selected(event):
        try:
            index = listOut.curselection()[0]
            selection = listOut.get(index)
            if len(selection) > 15:
                pass
            else:
                if isinstance(is_integer(selection[0]), int):
                    inputBox.delete(0,END)
                    if selection[3] == " ":
                        inputBox.insert(END, selection[4:-1])
                    else:
                        inputBox.insert(END, selection[3:-1])
        except Exception:
            pass

    def listenMIC():
        spRec = 1
        if is_connected('https://www.google.com'):
            spRec = 2
        else:
            spRec = 1
        r = sr.Recognizer()
        with sr.Microphone() as source:
            if spRec == 1:
                showerror("Smart English Dictionary", 
                "You are NOT connected to the Internet.\n\nThis Program uses Google APIs for Speech Recognition.\nWhich requires it to connect to Google's Servers.\n\nPlease CONNECT to the Internet and Try Again")
            elif spRec == 2:
                showinfo("Smart English Dictionary", 
                "Speak after pressing OK.\n\nYou are connected to the Internet.\nUsing Google's Speech Recognition.\n\nNote: Google's Speech Recognition is very accurate\n\tBUT it is SLOW.\n\tSo please be patient.")
                audio = r.listen(source)
                try:
                    text = ""
                    text = r.recognize_google(audio)
                    inputBox.delete(0,END)
                    inputBox.insert(END,text)
                    mainFunction.link()
                except:
                    showinfo("Smart English Dictionary", 
                    "Sorry! could not recognize what you said.\nPlease Try again by clicking MIC Button.")

    def submitt():
        """
        This is to link link()&submitt() with switch.
        """
        switch("normal")
        mainFunction.link()

    def link():
        listOut.delete(0,END)
        txt = is_integer(inp.get())
        if txt == "":
            showinfo("Smart English Dictionary", " Input is EMPTY...!\n  >>>  Please Provide an Input.")
            mainWindow.title("EMPTY - Smart English Dictionary")
        elif isinstance(txt, int):
            listOut.insert(END, ">>>  \"{}\" is a Mathematical Number, an Integer.".format(txt))
            mainWindow.title("{} - Smart English Dictionary".format(txt))
        elif isinstance(txt, float):
            listOut.insert(END,
            ">>>  \"{}\" is a Mathematical Rational-Decimal Number (Number containing Decimal).".format(txt))
            mainWindow.title("{} - Smart English Dictionary".format(txt))
        else:
            resList = main(txt)
            if resList[0] == "\\None":
                switch("disabled")
                Lab3.config(text = "Sorry, \"{}\" is unavailable in database.".format(txt) + " Suggestions :-")
                i = 0
                for out in resList[1:]:
                    listOut.insert(END, str(i+1) + ". " + out + "\n")
                    i += 1
                if i == 0:
                    showinfo("Smart English Dictionary", "Sorry, No Seggistions.\n Please try another Input.")
                    listOut.insert(END, " >>>  Sorry, No Seggistions, Please try another Input.")
                Lab4.config(text = " ")
                mainWindow.title("ERROR - Smart English Dictionary")

            else:
                cont = 1
                for cont in range(len(resList)):
                    cont += 1
                if cont == 1 :
                    Lab3.config(text = "Definition of \"{}\" is :-".format(txt))
                    listOut.insert(END, "1. " + resList[0])
                    Lab4.config(text = "Total Definition in Database = {}".format(cont))
                    mainWindow.title(txt + " - Smart English Dictionary")
                else:
                    Lab3.config(text = "Definitions of \"{}\" are :- ".format(txt))
                    i = 1
                    for out in resList:
                        listOut.insert(END, str(i) + ". " + out)
                        i += 1
                    Lab4.config(text = "Total Definitions in Database = {}".format(cont))
                    mainWindow.title(txt + " - Smart English Dictionary")

mainWindow = Tk()

mainWindow.wm_title("Smart English Dictionary")

mainWindow.iconbitmap("icon.ico")
# "Icon made by Freepik <https://www.flaticon.com/authors/freepik> from www.flaticon.com"

toolBar = Menu(mainWindow)
mainWindow.config(menu=toolBar)

file_menu= Menu(toolBar, tearoff=0)
toolBar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open",command=FileCl.openCMD)
file_menu.add_command(label="Save",command=FileCl.saveCMD)
file_menu.add_separator()
file_menu.add_command(label="Exit",command=mainWindow.quit)

edit_menu = Menu(toolBar, tearoff=0)
toolBar.add_cascade(label="Edit",menu=edit_menu)
edit_menu.add_command(label="Copy",command=EditCl.copyCMD)
edit_menu.add_command(label="Paste",command=EditCl.pasteCMD)
edit_menu.add_separator()
edit_menu.add_command(label="Clear",command=EditCl.cleraCMD)

more_menu = Menu(toolBar, tearoff=0)
toolBar.add_cascade(label="More",menu=more_menu)
more_menu.add_command(label="Updates",command=MoreCl.updateApp)
more_menu.add_command(label="About...!",command=MoreCl.aboutApp)

frame0 = Frame(mainWindow)
frame0.pack(side=TOP, fill=BOTH)

canvas = Canvas(frame0, width = 60, height = 65)
canvas.pack(side=LEFT, fill=BOTH)
img = PhotoImage(file="SED.png")
# "Icon made by Freepik <https://www.flaticon.com/authors/freepik> from www.flaticon.com"
canvas.create_image(5,15, anchor=NW, image=img)

title1 = Label(frame0, text = "Smart\nEnglish", font=("Bauhaus 93", 25), justify=LEFT)
title1.pack(side=LEFT, fill=BOTH)
title2 = Label(frame0, text = "Dictionary", font=("Bauhaus 93", 60), justify=LEFT)
title2.pack(side=LEFT, fill=BOTH)

frame1 = LabelFrame(mainWindow, text="Input : ", font="Calbiri 13")
frame1.pack(fill=BOTH)

msgLab = Label(frame1, text = "    ", font="Calbiri 13")
msgLab.pack(side=LEFT)

inp = StringVar()
inputBox = Entry(frame1, textvariable = inp, font=("Arial", 12))
inputBox.pack(side=LEFT, fill=X, expand=YES)

Lab1 = Label(frame1, text = " ", font="Calbiri 13")
Lab1.pack(side=LEFT)

listenImg = PhotoImage(file="vs.png")
# "Icon made by Freepik <https://www.flaticon.com/authors/freepik> from www.flaticon.com"
audioButton = Button(frame1, image=listenImg, command = mainFunction.listenMIC,
                      activeforeground="white", activebackground="black",
                      relief=GROOVE, font="Calbiri 13")
audioButton.pack(side=LEFT, fill=X)

Lab1 = Label(frame1, text = " ", font="Calbiri 13")
Lab1.pack(side=LEFT)

submitButton = Button(frame1, text = "          Submit          ", command = mainFunction.submitt,
                      activeforeground="white", activebackground="black",
                      relief=GROOVE, font="Calbiri 13")
submitButton.pack(side=LEFT, fill=X)

Lab2 = Label(frame1, text = " \n \n ", font="Calbiri 13")
Lab2.pack(side=LEFT)

frame2 = Frame(mainWindow)
frame2.pack(fill=BOTH)

Lab3 = Label(frame2, text = " ", font="Calbiri 13", justify=LEFT)
Lab3.pack(side=LEFT)
Lab4 = Label(frame2, text = " ", font="Calbiri 13", justify=RIGHT)
Lab4.pack(side=RIGHT)

frame3 = Frame(mainWindow)
frame3.pack(fill=BOTH, expand=YES)

listOut = Listbox(frame3, height = 15, width = 50, font=("Calbiri", 13))
listOut.pack(side=LEFT, fill=BOTH, expand=YES)

scrollY = Scrollbar(frame3)
scrollY.pack(side=RIGHT, fill=Y)

frame4 = Frame(mainWindow)
frame4.pack(fill=X)

scrollX = Scrollbar(frame4, orient = HORIZONTAL)
scrollX.pack(side=TOP, fill=X)

listOut.configure(yscrollcommand = scrollX.set)
scrollX.configure(command = listOut.xview)
listOut.configure(yscrollcommand = scrollY.set)
scrollY.configure(command = listOut.yview)
listOut.bind('<<ListboxSelect>>', mainFunction.selected)

mainWindow.mainloop()