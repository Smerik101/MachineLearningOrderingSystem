from tkinter import *
from stocktake import open_stocktake
from ordering import open_ordering

def stocktakerun():
    window.withdraw()
    open_stocktake(window)

def orderingrun():
    window.withdraw()
    open_ordering(window)

def mainmenu():

    label1 = Label(frame, text="Welcome!", font=("Arial", 12, "bold"))
    label1.grid(row = 1, column = 0, padx = 10, pady = 15, sticky= W)

    label2 = Label(frame, text="Please select an action to continue.", font=("Arial", 10))
    label2.grid(row = 2, column = 0, padx= 10, columnspan=2)

    button1 = Button(frame, text = "Do Stocktake", font = ("Arial", 8, "bold"), command = stocktakerun)
    button1.grid(row = 3, column = 0, padx = 10, pady= 20, sticky = W, columnspan= 2)

    button2 = Button(frame, text = "Propose Order", font = ("Arial", 8, "bold"), command = orderingrun)
    button2.grid(row = 3, column = 1, padx = 10, pady = 20,  sticky = W,)

# Initiate GUI upon program launch
window = Tk()
window.resizable(width=False, height=False)
window.title("Ordering System")
window.geometry('400x300')
frame = Frame(window)
frame.grid()
mainmenu()
window.mainloop()

