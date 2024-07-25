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


#data handling and output processing
import tkinter as tk

class ControllerClass:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        self.view.sendButton.config(command=self.update_message)
    
    def update_message(self):
        input_text = self.view.userInput.get().strip()
        if input_text:
            self.view.chatArea.config(state=tk.NORMAL)
            self.view.chatArea.insert(tk.END, f"You: \n{input_text} \n\n")
            self.view.chatArea.see(tk.END)
            self.view.chatArea.config(state=tk.DISABLED)
            self.view.userInput.delete(0, tk.END)

