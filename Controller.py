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
        self.username_acquired = False
        self.password_acquired = False
        self.ig_logged_in = False
        self.target_user_acquired = False
        self.scrape_done = False
        self.username = ""
        self.password = ""
        self.target_username = ""
        # Bind the button click and Enter key event to the process_input method
        self.view.sendButton.config(command=self.process_input)
        self.view.userInput.bind("<Return>", lambda event: self.process_input())

        self.commands = {
            "[/help]": "List all commands",
            "[/loginUser (username)]": "Input username for logging in",
            "ctrl+m": "Use [ctrl+m] to mask the user input (useful for hiding password input)",
            "[/loginPass (password)]": "Input password for logging in",
            "[/igLogin]": "Login to Instagram",
            "[/targetUsername (username)]": "Provide the target's Instagram username",
            "[/scrape]": "Get the information of the target",
            "[/generateReport]": "Generate a PDF of the report",
            "[/igLogout]": "Log out of Instagram and remove your Username and Password from this session"
            # Add other commands here
        }
        
    def process_input(self):
        input_text = self.view.get_input()
        if input_text:
            self.view.send_message(input_text)
            if input_text.startswith('/'):
                self.handle_command(input_text)
            else:
                self.view.display_message("Error processing command\n\nType [/help] for the list of possible commands\n\n")

    def handle_command(self, command):
        if command == "/help":
            help_message = "Available commands:\n"
            for cmd, desc in self.commands.items():
                help_message += f"{cmd}: {desc}\n"
            self.view.display_message(help_message)
        elif command.startswith("/loginUser"):
            split_string = command.split()
            if len(split_string) > 1:
                self.username = split_string[1]
                self.username_acquired = True
                self.view.display_message("Username acquired")
            else:
                self.view.display_message("Username not provided.")
        elif command.startswith("/loginPass"):
            if self.username_acquired:
                split_string = command.split()
                if len(split_string) > 1:
                    self.password = split_string[1]
                    self.password_acquired = True
                    self.view.display_message("Password acquired")
                else:
                    self.view.display_message("Password not provided.")
            else:
                self.view.display_message("Enter username first")
        elif command == "/igLogin":
            if self.username_acquired and self.password_acquired:
                if self.model.login_instagram(self.username, self.password):
                    self.view.display_message("Login success!")
                    self.ig_logged_in = True
                else:
                    self.view.display_message("Error loggin in")
            else:
                self.view.display_message("Error! Username or Password is not provided")
        elif command.startswith("/targetUsername"):
                split_string = command.split()
                self.target_username = split_string[1]
                self.view.display_message(F"The target username is: {self.target_username}")
                self.target_user_acquired = True
        elif command == "/scrape":
            if self.target_user_acquired:
                self.view.display_message("Finding the information of this person")
                if self.model.scrape_profile(self.target_username):
                    self.view.display_message("Scraping Done")
                    self.scrape_done = True
                else:
                    self.view.display_message("Person not found")
            else:
                self.view.display_message("Target username not provided")
        elif command == "/generateReport":
            if self.scrape_done:
                self.view.display_message("Generating file report via PDF")
                if self.model.save_to_pdf():
                    self.view.display_message("PDF generated!")
            else:
                self.view.display_message("Cannot generate report due to lacking information")
        elif command == "/igLogout":
            if self.ig_logged_in:
                self.view.display_message("Logging out and removing username and password")
                if self.model.logout():  
                    self.username = ""
                    self.password = ""
                    self.ig_logged_in = False
                    self.username_acquired = False
                    self.password_acquired = False
                    #print("The credentials are: " + self.username + " " + self.password + "test")
                    self.view.display_message("Logout success!")
                else:
                    self.view.display_message("The web logout is unsucessful, please try again")
            else:
                self.view.display_message("Error! User is not yet logged in")
        else:
            self.view.display_message("Unknown command. Type /help for a list of commands.")
