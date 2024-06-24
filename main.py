import customtkinter as ctk
from PIL import Image, ImageTk

# class 'PasswordStrengthChecker'
class PasswordStrengthChecker:
    def __init__(self):
        self.root = ctk.CTk()        
        # setting the background color of root container
        ctk.set_appearance_mode("dark-blue")
        # setting the title of the GUI
        self.root.title("Password Strength Checker")
        # Setting the dimension of GUI
        self.root.minsize(600, 300)
        self.root.maxsize(600, 420)
        # frame 'window' created inside 'root' container with background color set as #000000
        self.window = ctk.CTkFrame(self.root)
        self.window.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Load the image using PIL
        bulbImage = "images/bulbImage.png"
        pil_bulbImage = Image.open(bulbImage)
        errorImage = "images/errorImage.png"
        pil_errorImage = Image.open(errorImage)
        iconImage = "images/iconImage.png"
        pil_iconImage = Image.open(iconImage)

        # pictures converted to PhotoImage variables
        self.bulbPicture = ctk.CTkImage(light_image=pil_bulbImage, dark_image=pil_bulbImage, size=(20,20))
        self.errorPicture = ctk.CTkImage(light_image=pil_errorImage, dark_image=pil_errorImage, size=(18,18))
        self.iconPicture = ImageTk.PhotoImage(pil_iconImage)

        self.password_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        self.password_frame.pack(pady=10, padx=10, fill="x")

        self.passwordLabel = ctk.CTkLabel(self.password_frame, text="Password :", font=("Arial", 15, "bold"))
        self.passwordLabel.grid(row=0, column=0, padx=(80, 10), pady=10, sticky="w")

        self.passwordEntry = ctk.CTkEntry(self.password_frame, font=("Helvetica", 15), show="*", width=200)
        self.passwordEntry.grid(row=0, column=1, padx=(2, 80), pady=10, sticky="w")
        self.password_frame.grid_columnconfigure(1, weight=1)

        # Enabling copy and paste in Entry
        self.passwordEntry.bind("<Control-c>", self.copy_to_clipboard)
        self.passwordEntry.bind("<Control-v>", self.paste_from_clipboard)

        # variable of integer type to monitor ON and OFF conditions of checkbutton 'hidePassword'
        self.choiceNum = ctk.IntVar()
        self.hidePassword = ctk.CTkCheckBox(self.window,text="Show password", font=("Arial", 12), variable=self.choiceNum, command=self.showOrHideEntry)
        self.hidePassword.pack(pady=2)

        # Button to check the strength of user's password in the Entry 'passwordEntry'.
        self.submitButton = ctk.CTkButton(self.window,text="Check your password strength",command=self.checkPasswordStrength, font=("Helvetica",15))
        self.submitButton.pack(pady=8)

        # Create a frame for the highlight effect
        self.highlight_frame = ctk.CTkFrame(self.window, corner_radius=10, fg_color="transparent")
        self.highlight_frame.pack(pady=7)

        # Create the label inside the highlight frame
        self.passwordStrength = ctk.CTkLabel(self.highlight_frame, text="", font=("Arial", 15), padx=10, pady=5)
        self.passwordStrength.pack()

        # Frame inside 'window' container
        self.frame1 = ctk.CTkFrame(self.window, width=300)
        self.frame1.pack(pady=10, padx=10, fill="y", expand=True)
        self.frame1.pack_propagate(False)

        # Setting the icon near to title in GUI
        self.root.wm_iconphoto(True, self.iconPicture)
        self.root.mainloop()

    # Function to check the strength of user entered password in Entry 'passwordEntry'/
    def checkPasswordStrength(self):
        # Getting the string entered by user in Entry 'passwordEntry'.
        userPassword = self.passwordEntry.get()
        # List of strings to display as strength of password in the order of weak to very strong password.
        strength = ["Weak password","Moderate password","Strong password","Very strong password"]
        # symbols in list
        symbolsList = ["!","'",",",".","\"","+","-","/","\\","(",")","*","=","_","&","^","%","$","#","@","|","[","]","{","}","<",">","~","`"]
        # List of commonly used weak passwords worldwide
        commonWeakPasswords = ["password","qwerty","qwertyui","123","123456","xyz","abc","abcdef","admin","1111","000","password123",
                           "password1","123321","monkey","football","hello","iloveyou","dragon","letmein","baseball","flower",
                           "superman","princess","passw0rd","master","root","welcome","starwars","sunshine","777","555","google",
                           "qwert","qwer","qwe","computer","laptop","soccer","222","333","444","666","888","999","apple",
                           "internet","angel","lion","pokemon","ccc","www","zzz","gotham","batman","spiderman","ball","happy",
                           "princes","prince","family","beatles","school","meme","cool","music","dance","man","secret","college",
                           "cat","dog","sweet","disney","house","home","thankyou","software","date"]
        status = 3
        issuesInPassword = []
        ideasToUser = []
        if len(userPassword)<8:
            issuesInPassword.append("  Password length very small")
            status = 0
        elif userPassword.isspace():
            issuesInPassword.append("  Only white spaces is present")
            status = 0

        # Initialized boolean variables to check for letters, numbers, symbols to False
        hasUpperCase = hasLowerCase = hasDigit = hasSymbol = hasWhiteSpace = False
        countWhiteSpace = sameCharacterRepetition=0

        # Iterate through every character in the string 'userPassword'.
        for ptr in range(len(userPassword)):
            if ptr>0 and userPassword[ptr]==userPassword[ptr-1]:
                sameCharacterRepetition += 1
            character = userPassword[ptr]
            if character==" ":
                hasWhiteSpace = True
                countWhiteSpace += 1
            elif character.isdecimal():
                hasDigit = True
            elif character.isalpha()==True:
                if character.islower():
                    hasLowerCase = True
                elif character.isupper():
                    hasUpperCase = True
            elif character in symbolsList:
                hasSymbol = True
        if sameCharacterRepetition>0:
            issuesInPassword.append("  Characters repeating continuously")
        if countWhiteSpace>1:
            issuesInPassword.append("  Too many white spaces")
        if hasDigit==False:
            issuesInPassword.append("  No numbers present")
        if hasLowerCase==False and hasUpperCase==False:
            issuesInPassword.append("  No alphabets present")
        elif hasLowerCase==False and hasUpperCase==True:
            issuesInPassword.append("  No letters in lowercase")
        elif hasUpperCase==False and hasLowerCase==True:
            issuesInPassword.append("  No letters in uppercase")
        if hasSymbol==False:
            issuesInPassword.append("  No symbols")

        # If password has digits,upper and lowercase letters, symbols, rank password based on its length.
        # Also rank based on characters repeating continuously.
        if hasLowerCase==True and hasUpperCase==True and hasDigit==True and hasSymbol==True:
            if len(userPassword)>=8 and len(userPassword)<=10:
                ideasToUser.append("  Make password longer")
                status = 1
            elif len(userPassword)>=11 and len(userPassword)<=14:
                ideasToUser.append("  Make the password a little longer")
                status = 2
            elif len(userPassword)>=15: # password is length greater than or equal to 15 is considered as VERY STRONG password.
                status = 3
                if len(userPassword)>30:
                    ideasToUser.append("  Password very long. Use password manager to store your password!")
            if sameCharacterRepetition>0 or countWhiteSpace>1:
                status = 1
        else:  # User password has digit or letter or symbol missing
            status = 0

        # Check for repeated pattern in user's password.
        # If there are more than 1 pattern repeating, the user password is assumed to be weak.
        # If there is only 1 pattern repeating, if the length of user password is less than 9, it is assumed as weak.
        # Otherwise, if there is only 1 pattern repeating, and the length of user password is more than 8,
        # it is not assumed as weak.
        hasRepeatedPattern = self.checkForPatternRepeating()
        if hasRepeatedPattern==True:
            issuesInPassword.append("  Repeating patterns in password")
            status = 0

        # check for commonly used word worldwide as in password.
        # If the user password has any string from the array 'commonWeakPasswords', assume it as WEAK password
        userPasswordInLower = userPassword.lower()
        for commonWord in commonWeakPasswords:
            if userPasswordInLower.find(commonWord) >= 0:
                status = 0
                issuesInPassword.append("  Commonly used words found")
                break

        # Displaying strength of password based on its strength number 'status' in different colors.
        if status==0:
            self.passwordStrength.configure(text=strength[status], text_color="#FA8072")
        elif status==1:
            self.passwordStrength.configure(text=strength[status], text_color="#FF8C00")
        elif status==2:
            self.passwordStrength.configure(text=strength[status], text_color="#00FFEF")
        elif status==3:
            self.passwordStrength.configure(text=strength[status], text_color="#39FF14")

        # Before displaying the issues in the user password, delete all previously created widgets within the frame 'frame1'
        for widgets in self.frame1.winfo_children():
            widgets.destroy()
        # Displaying issues in the user's password
        for currentIndex in range(len(issuesInPassword)):
            self.issue = ctk.CTkLabel(self.frame1,  text=issuesInPassword[currentIndex], font=("Arial",15), anchor="nw", image=self.errorPicture, compound="left")
            self.issue.pack(anchor="w", padx=15)
        # Displaying any recommendations to user if available
        for currentIndex in range(len(ideasToUser)):
            self.ideas = ctk.CTkLabel(self.frame1, text=ideasToUser[currentIndex], image=self.bulbPicture, compound="left", font=("Arial",15))
            self.ideas.pack()

    # Function to check if any pattern of string is repeating user's password entered
    def checkForPatternRepeating(self):
        # Get the password entered by user in the Entry
        userPassword = self.passwordEntry.get()
        patternMap = {}
        # variable to store count of repeating patterns of length 3 in the user password
        countOfRepeatedPattern = 0
        for ptr in range(len(userPassword)):
            if (ptr+2)<len(userPassword):
                pattern = userPassword[ptr:ptr+3]
                if pattern not in patternMap:
                    patternMap.update({pattern:1})
                else:
                    # Increment the value of the key in dictionary 'patternMap' as key is reappearing
                    patternMap.update({pattern:patternMap.get(pattern)+1})
        # Get the list of values in the dictionary 'patternMap' and loop through it.
        for patternCount in patternMap.values():
            # If the patternCount is more than 1, increment the value of variable 'countOfRepeatedPattern'.
            if patternCount>1:
                countOfRepeatedPattern += 1
        # If there is only 1 pattern repeating in the user's password, if the length of password is less than 8,
        # consider it as weak password. If the length is greater than 10, return FALSE denoting it is not weak password.
        if countOfRepeatedPattern == 1:
            if len(userPassword) <= 10:
                return True # Weak password
            else:
                return False # Not weak password
        # If the count of patterns repeating is more than 1, then assume the user's password as weak password.
        elif countOfRepeatedPattern > 1:
            return True
        # countOfRepeated is zero. Hence, returning False
        return False

    # Function to change the text to secret code based on whether the checkbutton is clicked
    def showOrHideEntry(self):
        if self.choiceNum.get() == 1:
            self.passwordEntry.configure(show="")
        else:
            self.passwordEntry.configure(show="*")
    
    def copy_to_clipboard(self, event=None):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.passwordEntry.selection_get())
        return "break"

    def paste_from_clipboard(self, event=None):
        self.passwordEntry.insert(ctk.INSERT, self.root.clipboard_get())
        return "break"

# Object created for the class 'PasswordStrengthChecker'
app = PasswordStrengthChecker()
