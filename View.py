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


#GUI

import tkinter as tk
from tkinter import scrolledtext

class ViewClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Social Media Scraper")
        
        # Create panel1
        self.panel1 = tk.Frame(root, bg="#212121", padx=20, pady=20)
        self.panel1.pack(fill=tk.BOTH, expand=True)
        
        # Create user input field
        self.userInput = tk.Entry(self.panel1, bg="#2F2F2F", fg="white", insertbackground="white")
        self.userInput.grid(row=1, column=0, columnspan=4, sticky="ew", padx=(0, 10))
        
        # Create send button
        self.sendButton = tk.Button(self.panel1, text="Send", bg="white", command=self.send_message)
        self.sendButton.grid(row=1, column=4, sticky="e")
        
        # Create chat area
        self.chatArea = scrolledtext.ScrolledText(self.panel1, bg="#212121", fg="white", wrap=tk.WORD)
        self.chatArea.grid(row=0, column=0, columnspan=5, sticky="nsew", pady=(0, 10))
        self.chatArea.insert(tk.END, "Type [/help] for the list of possible commands\n\n")
        self.chatArea.config(state=tk.DISABLED)
        
        # Configure grid weights
        self.panel1.grid_rowconfigure(0, weight=1)
        self.panel1.grid_columnconfigure(0, weight=1)
        self.panel1.grid_columnconfigure(1, weight=1)
        self.panel1.grid_columnconfigure(2, weight=1)
        self.panel1.grid_columnconfigure(3, weight=1)
        self.panel1.grid_columnconfigure(4, weight=0)
        
        # Bind Enter key to send message
        self.userInput.bind("<Return>", lambda event: self.send_message())
    
    def send_message(self, input_text):
        #print("send message is called")
        if input_text:
            self.chatArea.config(state=tk.NORMAL)
            self.chatArea.insert(tk.END, f"You: \n{input_text} \n\n")
            self.chatArea.see(tk.END)
            self.chatArea.config(state=tk.DISABLED)
            self.userInput.delete(0, tk.END)

    def display_message(self, message):
        self.chatArea.config(state=tk.NORMAL)
        self.chatArea.insert(tk.END,"Response:\n" + message + "\n\n")
        self.chatArea.see(tk.END)
        self.chatArea.config(state=tk.DISABLED)

    def get_input(self):
        input_text = self.userInput.get().strip()
        self.userInput.delete(0, tk.END)
        return input_text

