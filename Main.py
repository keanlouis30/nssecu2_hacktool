# This project was made in partial fulfillment of the requirements for the course NSSECU2
# submitted by:
# ABANIEL, AARON C.
# BIACORA, LUIS GABRIEL S.
# BLASCO, GIAN RAPHAEL Q.
# EVANGELISTA, REGINALD ANDRE I.
# QUINONES, ANGELO Y.
# ROSALES, KEAN LOUIS R.
# Group 4 | S12
# Submitted to:
# ASCAN, ADRIAN GIOVANNI
# on 
# (deadline)


#Main program
import tkinter as tk
from Model import ModelClass
from View import ViewClass
from Controller import ControllerClass

if __name__ == "__main__":
    root = tk.Tk()
    model = ModelClass()
    view = ViewClass(root)
    controller = ControllerClass(model, view)
    root.mainloop()
