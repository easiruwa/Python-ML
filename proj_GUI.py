################################################################################
#                 HAMILTON COLLEGE SUMMER RESEARCH 2016                        #
#   Eseosa Asiruwa '18, Matt Goon '18, Mitchel Herman '19, Sindy Liu '18       #
#                 Python Machine Learning GUI Interface                        #
#                              proj_GUI.py                                     #
#                                                                              #
#   This Program is the GUI for proj.py. It creates the parameter files        #
#   necessary to run the main code. Please see the attatched Manual for more   #
#   instructions                                                               #
#                                                                              #
#                                                                              #
#                                                                              #
#                                                                              #
#                                                                              #
#                                                                              #
################################################################################

# Basic Concept Design:
# Everytime user goes forward create the new window and show it.
# Everytime user goes backward show the previous window and delete the window.

from Tkinter import*
import tkMessageBox
import Tkconstants
import tkFileDialog
import os
import re
import proj


# Initial list of sensors, will be used later in submit_sensors()
sensors = ["fNIRS", "EEG", "Respiration", "ECG", "EDA"]
# Intiial list of sensors that are selected
selected_sensors = []

# List to hold all the lines of output to be written to parameter file
output = []

# List to hold all the lines of output to be written to data name file
output_filenames = []

class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Data Fusion and Machine Learning")
        self.center_UI(400, 250)
        self.config(background = "gray90")
        root = Frame(self)
        root.grid_rowconfigure(0, weight = 1)
        root.grid_columnconfigure(0, weight = 1)

        # Initialize a dictionary?
        self.frames = {}

        # Initially create and show the first window
        self.create_frame(window1)
        self.show_frame(window1)


    # Takes a frame name (NOT A STRING!), creates an instance of it,
    # and adds the frame to the "frames" dictinary.
    def create_frame(self, frame):
        f = frame(self)
        self.frames[frame] = f
        f.grid(row = 0, column = 0, sticky = "nsew")

    # Takes a frame name (NOT A STRING!) and destroys the corresponding frame
    def close_frame(self, frame):
        f = self.frames[frame]
        f.destroy()

    # Takes a frame name (NOT A STRING!) and shows the corresponding frame
    def show_frame(self, frame):
        f = self.frames[frame]
        f.tkraise()

    # Centers the window
    def center_UI(self, width, height):
            sw = self.winfo_screenwidth()
            sh = self.winfo_screenheight()
            x = (sw - width)/2
            y = (sh - height)/2
            self.geometry('%dx%d+%d+%d' % (width, height, x, y))


################################################################################

# 1st Window: Select the Sensors

################################################################################

class window1(Frame):
    def __init__(self, master):
        """Intitialize Frame"""
        Frame.__init__(self, master, background = "gray90")
        self.master = master
        self.grid()
        self.create_window1()

## Create Window 1's widgets
    def create_window1(self):

        # Header & Instructions
        self.header = Label(self,
                            text = """Sensor Selection """,
                            background = "gray90", font = "Arial 15 underline")
        self.header.grid(row = 0,column = 0,
            rowspan = 2, columnspan = 7, sticky = W)

        self.instructions = Label(self,
                            text = "     Select which sensors\
to include data from.",
                            pady = 4, background = "gray90", font = "Arial 14")
        self.instructions.grid(row = 3,column = 0,
            rowspan = 1, columnspan = 7, sticky = W)

        # fNIRS: Header & Checkbox
        self.fNIRS = IntVar()
        self.fNIRS_Check = Checkbutton(self, variable = self.fNIRS,
            background = "gray90")
        self.fNIRS_Check.grid(row = 4, column = 1)

        self.fNIRS_Header = Label(self,text = "fNIRS",
            background = "gray90", font = "Arial 14")
        self.fNIRS_Header.grid(row = 4, column = 3, sticky = W)

        # EEG: Header & Checkbox
        self.EEG = IntVar()
        self.EEG_Check = Checkbutton(self, variable = self.EEG,
            background = "gray90")
        self.EEG_Check.grid(row = 5, column = 1)

        self.EEG_Header = Label(self, text  = "EEG",
            background = "gray90", font = "Arial 14")
        self.EEG_Header.grid(row = 5, column = 3, sticky = W)

        # Respiration: Header & Checkbox
        self.Respiration = IntVar()
        self.Respiration_Check = Checkbutton(self, variable = self.Respiration,
            background = "gray90")
        self.Respiration_Check.grid(row = 6, column = 1)

        self.Respiration_Header = Label(self, text  = "Respiration",
            background = "gray90", font = "Arial 14")
        self.Respiration_Header.grid(row = 6, column = 3, sticky = W)

        # ECG: Header & Checkbox
        self.ECG= IntVar()
        self.ECG_Check = Checkbutton(self, variable = self.ECG,
            background = "gray90")
        self.ECG_Check.grid(row = 7, column = 1)

        self.ECG_Header = Label(self, text  = "ECG",
            background = "gray90", font = "Arial 14")
        self.ECG_Header.grid(row = 7, column = 3, sticky = W)

        # EDA: Header & Checkbox
        self.EDA= IntVar()
        self.EDA_Check = Checkbutton(self, variable = self.EDA,
            background = "gray90")
        self.EDA_Check.grid(row = 8, column = 1)

        self.EDA_Header = Label(self, text  = "EDA",
            background = "gray90", font = "Arial 14")
        self.EDA_Header.grid(row = 8, column = 3, sticky = W)

        # Next Button
        self.submit_sensors_button = Button(self, text = "Next",
            command = self.submit_sensors, font = "Arial 14")
        self.submit_sensors_button.grid(row = 10, column = 7)

################################################################################
# End of creating Window 1's widgets
################################################################################

# Function for Next Button
# Collects which sensors has been selected and move on to the next window
    def submit_sensors(self):

        # Add title to output
        output.append("Sensors\n")

        # Clear the list of selected sensors before
        # adding new list of selected sensors
        del selected_sensors[:]

        # If the sensor is selected, add it to output as True,
        # and False otherwise.

        # fNIRS:
        if (self.fNIRS.get() == 1):
            output.append("fNIRS: True\n")
            selected_sensors.append("fNIRS")
        else:
            output.append("fNIRS: False\n")

        # EEG:
        if (self.EEG.get() == 1):
            output.append("EEG: True\n")
            selected_sensors.append("EEG")
        else:
            output.append("EEG: False\n")

        # Respiration
        if (self.Respiration.get() == 1):
            output.append("Respiration: True\n")
            selected_sensors.append("Respiration")
        else:
            output.append("Respiration: False\n")

        # ECG
        if (self.ECG.get() == 1):
            output.append("ECG: True\n")
            selected_sensors.append("ECG")
        else:
            output.append("ECG: False\n")

        # EDA
        if (self.EDA.get() == 1):
            output.append("EDA: True\n")
            selected_sensors.append("EDA")
        else:
            output.append("EDA: False\n")

        # If at least one sensor has been selected,
        # then create and show Window 2
        if (selected_sensors != []):
            self.master.geometry("600x800")
            self.master.create_frame(window2)
            self.master.show_frame(window2)

################################################################################

# 2nd Window: Select Feature Parameters

################################################################################

class window2(Frame):
    def __init__(self, master):
        """Intitialize Frame"""
        Frame.__init__(self, master, background = "gray90")
        self.master = master
        self.grid()
        self.create_window2_widgets()

# Create Window 2's widgets
    def create_window2_widgets(self):

        # Header
        self.header = Label(self,
                            text = """Feature Parameters""", pady = 5,
                            background = "gray90", font = "Arial 15 underline")
        self.header.grid(row = 0,column = 0,
            rowspan = 1, columnspan = 10, sticky = W)

        instructions_text = "     For each sensor- select how you want to\
alter the data. If you don't want to alter the data for a specific\
sensor, do not select anything. If applicable, fill out the sampling rate\
of the sensor(s)."

        # Instructions
        self.instructions = Label(self,
                            text = instructions_text,
                            background = "gray90", font = "Arial 14",
                            wraplength = "550", justify = "left")
        self.instructions.grid(row = 2, column = 1,
            rowspan = 2, columnspan = 25, sticky = W)

        # Line Break
        self.break0 = Label(self, background = "gray90")
        self.break0.grid(row = 4, column = 0)

        # fNIRS:
        # If selected, create widgets for customizing z-score and ROI
        if "fNIRS" in selected_sensors:

            # Header
            self.fNIRS_Header = Label(self,text = "fNIRS",
                background = "gray90", font = "Arial 14 bold", justify = "left")
            self.fNIRS_Header.grid(row = 5, column = 1, sticky = W)

            # Z-score: Checkbox and Header
            self.fNIRS_zscore = IntVar()
            self.fNIRS_zscore_Check = Checkbutton(self,
                variable = self.fNIRS_zscore, background = "gray90")
            self.fNIRS_zscore_Check.grid(row = 6, column = 1, sticky = E)

            self.fNIRS_Header = Label(self,text = "  Z-score",
                background = "gray90", font = "Arial 14")
            self.fNIRS_Header.grid(row = 6, column = 2, sticky = W,
                columnspan = 3)

            # ROI: Checkbox and Header
            self.fNIRS_ROI = IntVar()
            self.fNIRS_ROI_Check = Checkbutton(self, variable = self.fNIRS_ROI,
                command = self.update_fNIRS_ROI, background = "gray90")
            self.fNIRS_ROI_Check.grid(row = 7, column = 1, sticky = E)

            self.fNIRS_ROI_Header = Label(self,
                text = "  ROI (Region Of Interest analysis)",
                background = "gray90", font = "Arial 14")
            self.fNIRS_ROI_Header.grid(row = 7, column = 2,
                columnspan = 17, sticky = W)

            # ROI: File Display Header
            self.fNIRS_ROI_display_label = Label(self, text = "fNIRS ROI Files",
                background = "gray90", font = "Arial 14 bold", state = DISABLED)
            self.fNIRS_ROI_display_label.grid(row = 8, column = 2,
                columnspan = 4, sticky = W)

            # ROI: Scrollbar and Display
            self.fNIRS_ROI_yscrollbar = Scrollbar(self)
            self.fNIRS_ROI_yscrollbar.grid(row = 9, rowspan = 5,
                column = 19, sticky = NS)

            self.fNIRS_ROI_xscrollbar = Scrollbar(self, orient = HORIZONTAL)
            self.fNIRS_ROI_xscrollbar.grid(row = 15, column = 2,
                columnspan = 17, sticky = EW)

            self.fNIRS_ROI_display = Listbox(self, height = 4, width = 35,
                background = "gray90", selectmode=EXTENDED, state = DISABLED,
                yscrollcommand=self.fNIRS_ROI_yscrollbar.set,
                xscrollcommand=self.fNIRS_ROI_xscrollbar.set)
            self.fNIRS_ROI_display.grid(row = 9, rowspan = 5, column = 2,
                columnspan = 17, sticky = W)

            self.fNIRS_ROI_yscrollbar.config(
                command = self.fNIRS_ROI_display.yview)
            self.fNIRS_ROI_xscrollbar.config(
                command = self.fNIRS_ROI_display.xview)

            # ROI: Add & Remove Files Buttons
            self.fNIRS_ROI_browse = Button(self, text = "Add ROI file",
                command = self.fNIRS_ROI_browse, font = "Arial 14",
                state = DISABLED)
            self.fNIRS_ROI_browse.grid(row = 9, column = 20)

            self.fNIRS_ROI_delete = Button(self, text = "Remove file",
                command = self.fNIRS_ROI_remove, font = "Arial 14",
                state = DISABLED)
            self.fNIRS_ROI_delete.grid(row = 10, column = 20)

            # Line Break
            self.break1 = Label(self, background = "gray90")
            self.break1.grid(row = 15, column = 0)

        # EEG:
        # If selected, create widgets for customizing z-score
        if "EEG" in selected_sensors:

            # Header
            self.EEG_Header = Label(self, text = "EEG", background = "gray90",
                font = "Arial 14 bold", justify = "left")
            self.EEG_Header.grid(row = 16, column = 1, sticky = W)

            # Z-score
            self.EEG_zscore = IntVar()
            self.EEG_zscore_Check = Checkbutton(self,
                variable = self.EEG_zscore, background = "gray90")
            self.EEG_zscore_Check.grid(row = 17, column = 1, sticky = E)
            self.EEG_zscore_Header = Label(self,text = "  Z-score",
                background = "gray90", font = "Arial 14")
            self.EEG_zscore_Header.grid(row = 17, column = 2,
                columnspan = 4,sticky = W)

            # Line Break
            self.break2 = Label(self, background = "gray90")
            self.break2.grid(row = 18, column = 0)

        # Respiration:
        # If selected, create widgets for customizing z-score and Sampling Rate
        if "Respiration" in selected_sensors:

            # Header
            self.Respiration_Header = Label(self,text = "Respiration",
                background = "gray90", font = "Arial 14 bold", justify = "left")
            self.Respiration_Header.grid(row = 19, column = 1, sticky = W)

            # Z-score
            self.Respiration_zscore = IntVar()
            self.Respiration_zscore_Check = Checkbutton(self,
                variable = self.Respiration_zscore, background = "gray90")
            self.Respiration_zscore_Check.grid(row = 20, column = 1, sticky = E)
            self.Respiration_zscore_Header = Label(self,text = "  Z-score",
                background = "gray90", font = "Arial 14")
            self.Respiration_zscore_Header.grid(row = 20, column = 2,
                sticky = W)

            # Sampling Rate
            self.Respiration_rate_Header = Label(self,text = "Sampling Rate: ",
                background = "gray90", font = "Arial 14")
            self.Respiration_rate_Header.grid(row = 21, column = 1,
                columnspan = 5, sticky = E)

            self.Respiration_rate_Entry = Entry(self, justify = "right",
                width = 8)
            self.Respiration_rate_Entry.grid(row = 21, column =7, sticky = E)
            self.Respiration_rate_Entry.insert(0, "1000") # 1000 is the default

            self.Respiration_rate_Instructions = Label(self,
                text = "Number of samples per second",
                background = "gray90", font = "Arial 11")
            self.Respiration_rate_Instructions.grid(row = 22, column = 1,
                columnspan = 7, sticky = E)

            # Line Break
            self.break3 = Label(self, background = "gray90")
            self.break3.grid(row = 22, column = 0)

        # ECG:
        # If selected, create widgets for customizing z-score and Sampling Rate
        if "ECG" in selected_sensors:

            # Header
            self.ECG_Header = Label(self,text = "ECG", background = "gray90",
                font = "Arial 14 bold", justify = "left")
            self.ECG_Header.grid(row = 24, column = 1, sticky = W)

            # Z-score
            self.ECG_zscore = IntVar()
            self.ECG_zscore_Check = Checkbutton(self,
                variable = self.ECG_zscore, background = "gray90")
            self.ECG_zscore_Check.grid(row = 25, column = 1, sticky = E)
            self.ECG_zscore_Header = Label(self,text = "  Z-score",
                background = "gray90", font = "Arial 14")
            self.ECG_zscore_Header.grid(row = 25, column = 2, sticky = W)

            # Sampling Rate
            self.ECG_rate_Header = Label(self,text = "Sampling Rate: ",
                background = "gray90", font = "Arial 14")
            self.ECG_rate_Header.grid(row = 26, column = 1,
                columnspan = 5, sticky = E)

            self.ECG_rate_Entry = Entry(self, justify = "right", width = 8)
            self.ECG_rate_Entry.grid(row = 26, column =7, sticky = E)
            self.ECG_rate_Entry.insert(0, "1000") # 1000 is the default

            self.ECG_rate_Instructions = Label(self,
                text = "Number of samples per second",
                background = "gray90", font = "Arial 11")
            self.ECG_rate_Instructions.grid(row = 27, column = 1,
                columnspan = 7, sticky = E)

            # Line Break
            self.break4 = Label(self, background = "gray90")
            self.break4.grid(row = 28, column = 0)

        # EDA:
        # If selected, create widgets for customizing z-score and Sampling Rate
        if "EDA" in selected_sensors:

            # Header
            self.EDA_Header = Label(self,text = "EDA", background = "gray90",
                font = "Arial 14 bold", justify = "left")
            self.EDA_Header.grid(row = 29, column = 1, sticky = W)

            # Z-score
            self.EDA_zscore = IntVar()
            self.EDA_zscore_Check = Checkbutton(self,
                variable = self.EDA_zscore, background = "gray90")
            self.EDA_zscore_Check.grid(row = 30, column = 1, sticky = E)
            self.EDA_zscore_Header = Label(self,text = "  Z-score",
                background = "gray90", font = "Arial 14")
            self.EDA_zscore_Header.grid(row = 30, column = 2, sticky = W)

            # Sampling Rate
            self.EDA_rate_Header = Label(self, text = "Sampling Rate: ",
                background = "gray90", font = "Arial 14")
            self.EDA_rate_Header.grid(row = 31, column = 1,
                columnspan = 5, sticky = E)

            self.EDA_rate_Entry = Entry(self, justify = "right", width = 8)
            self.EDA_rate_Entry.grid(row = 31, column =7, sticky = E)
            self.EDA_rate_Entry.insert(0, "1000") # 1000 is the default

            self.EDA_rate_Instructions = Label(self,
                text = "Number of samples per second",
                background = "gray90", font = "Arial 11")
            self.EDA_rate_Instructions.grid(row = 32,
                column = 1, columnspan = 7, sticky = E)

            #Line Break
            self.break5 = Label(self, background = "gray90")
            self.break5.grid(row = 32, column = 0)

        #Back Button (return to window1)
        self.back_button = Button(self, text = "Back",
            command = self.back_window1, font = "Arial 14")
        self.back_button.grid(row = 34, column = 1, sticky = W)

        #Next Button (move on to window 3)
        self.next_button = Button(self, text = "Next",
            command = self.next_window3, font = "Arial 14")
        self.next_button.grid(row = 34, column = 21, sticky = E)

################################################################################
# End of creating Window 2's widgets
################################################################################

# Function for fNIRS ROI Checkbox
# If selected, then ROI files can be uploaded.
# Otherwise, ROI files cannot be uploaded.
    def update_fNIRS_ROI(self):

        if (self.fNIRS_ROI.get() == 1):
            self.fNIRS_ROI_display_label["state"] = NORMAL
            self.fNIRS_ROI_display["state"] = NORMAL
            self.fNIRS_ROI_browse["state"] = NORMAL
            self.fNIRS_ROI_delete["state"] = NORMAL

        else:
            self.fNIRS_ROI_display_label["state"] = DISABLED
            self.fNIRS_ROI_display["state"] = DISABLED
            self.fNIRS_ROI_browse["state"] = DISABLED
            self.fNIRS_ROI_delete["state"] = DISABLED

# Function for fNIRS ROI Add Files Button
# Browse for ROI file and add it to the display
    def fNIRS_ROI_browse(self):

        # Browse for ROI file(s)
        filenames1 = tkFileDialog.askopenfilename(
            filetypes = [("txt files", "*.txt")],
            multiple = True, title = 'Choose a fNIRS ROI data file')

        filenames = []
        for item in filenames1:
            filenames.append(os.path.basename(item))
        # ^^^This stores only the basename
        # of the files (not the directory). Uncomment if you want this.

        # Error Checking the ROI file(s)

        # ROI Files Regular Expression
        # Checks for at least one whitespace or alphanumeric character or
        # dash '-', then a colon ':', then any number of whitespace, then
        # at any number of alphanumeric characters, then 'roi' in any case,
        # then any number of alphanumeric characters, then '.txt', followed
        # by any number of a group of one comma ',', then any number of
        # whitespace, then at any number of alphanumeric characters, then
        # 'roi' in any case, then any number of alphanumeric characters,
        # then '.txt' Finished off by at least one whitespace character.
        # Also is case-insensitive.
        ROIfilenameRE = re.compile('/?([\w\s]+/)*\w*roi\w*\.txt$',
            re.IGNORECASE)

        # Checks for at least one digit in name of filenames
        DigitCheckTXTRE = re.compile('/?([\w\s]+/)*\w*\d+\w*\.txt$')

        # If the file name is correct, then add it to the display.
        # If not, then show an error message.
        if filenames:
            filenameError = False
            for filename in filenames:
                match = ROIfilenameRE.match(filename)
                match2 = DigitCheckTXTRE.match(filename)
                if (match and match2):
                    self.fNIRS_ROI_display.insert(END, filename)
                else:
                    filenameError = True
                if (filenameError):
                    tkMessageBox.showerror("ERROR",
                        "Please provide an appropriate ROI data file.\
\nText file must have ROI in its name.")

# Function for fNIRS ROI Remove File Button
# Select a file on the display and press this button to remove it.
    def fNIRS_ROI_remove(self):
        self.fNIRS_ROI_display.delete(ANCHOR)

# Function for the Back Button
# Return to Window 1
    def back_window1(self):

        # Remove last 6 entries of output (6 added from window 1) to reset
        # for new selected output from user
        for i in range(6):
            output.pop()

        # Show Window 1 and delete Window 2
        self.master.geometry("400x250")
        self.master.show_frame(window1)
        self.master.close_frame(window2)

# Function for the Next Button
# Check if parameters are good. If they are then create and show Window 3.
    def next_window3(self):

        ROI_good = True # Boolean to keep track of correctness of ROI inputs
        rate_good = True # Boolean to keep track of corretness of
                        # Sampling Rate inputs
        error_message = "" # Initialize a string to store a customized
                        # error message to display if the paremters are wrong

        # Check that ROI text files are uploaded if fNIRS_ROI is selected,
        if "fNIRS" in selected_sensors:
            if (self.fNIRS_ROI.get() == 1):

                if (self.fNIRS_ROI_display.size() == 0):
                    error_message += "ROI is checked off,\
                     but there are no ROI files selected.\n"
                    ROI_good = False

                else:
                    ROI_list = self.fNIRS_ROI_display.get(0, END)
                    for file in ROI_list:
                        if file[-4:] != ".txt":
                            error_message += "ROI files must be text files.\n"
                            ROI_good = False
                            break

        # Check that sampling rate (if applicable) has been filled out
        # and is an integer.
        if "Respiration" in selected_sensors:
            if not self.Respiration_rate_Entry.get().isdigit():
                rate_good = False

        if "ECG" in selected_sensors:
            if not self.ECG_rate_Entry.get().isdigit():
                rate_good = False

        if "EDA" in selected_sensors:
            if not self.EDA_rate_Entry.get().isdigit():
                rate_good = False

        if not rate_good:
            error_message += "Sampling Rate must be filled out\
             as a postive integer."

        # If the ROI and Sampling Rate parameters were inputted correctly,
        # then write parameters to the output string and move on to Window 3.
        if ROI_good and rate_good:
            # Add title to output
            output.append("\nFeature Parameters\n")

            # If fNIRS was selected,
            # get the paramter values add to the output list.
            if "fNIRS" in selected_sensors:

                if (self.fNIRS_zscore.get() == 1):
                    output.append("fNIRS Z-Score: True\n")
                else:
                    output.append("fNIRS Z-Score: False\n")

                if (self.fNIRS_ROI.get() == 1):
                    output.append("fNIRS ROI: True\n")
                    ROI_string = "fNIRS ROI Filename(s): "

                    # Get every filename in the listbox
                    # (listbox.get() function returns a list of the items)
                    fNIRS_ROI_list = self.fNIRS_ROI_display.get(0, END)

                    # Append every filename in the list to the output string
                    # as well as a comma and space
                    for fNIRS_ROI_file in fNIRS_ROI_list:
                        ROI_string += (fNIRS_ROI_file + ", ")
                    ROI_string = ROI_string[:-2]    # Remove last comma & space
                    ROI_string += "\n"              # Add new line

                    # Finally add the completed string to output list
                    output.append(ROI_string)

                else:
                    output.append("fNIRS ROI: False\n")
                    output.append("fNIRS ROI Filenames:\n")

            #If fNIRS was not selected,
            # add all paramters values as False to the output list
            else:
                output.append("fNIRS Z-Score: False\n")
                output.append("fNIRS ROI: False\n")
                output.append("fNIRS ROI Filenames:\n")

            #If EEG was selected,
            # get the paramter values add to the output list.
            if "EEG" in selected_sensors:

                if (self.EEG_zscore.get() == 1):
                    output.append("EEG Z-Score: True\n")
                else:
                    output.append("EEG Z-Score: False\n")

             # If EEG was not selected,
             # add all paramters values as False to the output list
            else:
                output.append("EEG Z-Score: False\n")

            # If Respiration was selected,
            # get the paramter values add to the output list.
            if "Respiration" in selected_sensors:

                if (self.Respiration_zscore.get() == 1):
                    output.append("Respiration Z-Score: True\n")
                else:
                    output.append("Respiration Z-Score: False\n")
                output.append("Respiration Sampling Rate: " +
                    self.Respiration_rate_Entry.get() + "\n")

            # If Respiration was not selected,
            # add all paramters values as False to the output list
            else:
                output.append("Respiration Z-Score: False\n")
                output.append("Respiration Sampling Rate: 0\n")

            # If ECG was selected,
            # get the paramter values add to the output list.
            if "ECG" in selected_sensors:

                if (self.ECG_zscore.get() == 1):
                    output.append("ECG Z-Score: True\n")
                else:
                    output.append("ECG Z-Score: False\n")
                output.append("ECG Sampling Rate:  " +
                    self.ECG_rate_Entry.get() + "\n")

            #If ECG was not selected,
            #add all paramters values as False to the output list
            else:
                output.append("ECG Z-Score: False\n")
                output.append("ECG Sampling Rate: 0\n")

            #If EDA was selected, get the paramter values add to the output list.
            if "EDA" in selected_sensors:

                if (self.EDA_zscore.get() == 1):
                    output.append("EDA Z-Score: True\n")
                else:
                    output.append("EDA Z-Score: False\n")
                output.append("EDA Sampling Rate: " +
                    self.EDA_rate_Entry.get() + "\n")

            #If EDA was not selected,
            # add all paramters values as False to the output list
            else:
                output.append("EDA Z-Score: False\n")
                output.append("EDA Sampling Rate: 0\n")


            self.master.create_frame(window3)
            self.master.show_frame(window3)

        #If parameters are incorrect, show an error message.
        else:
            tkMessageBox.showerror("Invalid Entry", error_message)

################################################################################

# 3rd Window: Select SAX Parameters

################################################################################

class window3(Frame):
    def __init__(self, master):
        """Intitialize Frame"""
        Frame.__init__(self, master, background = "gray90")
        self.master= master
        self.grid()
        self.SAX_Bool = [] # Initialize a list to keep track of which sensors
                        # have SAX as True
        self.create_window3_widgets()

# Create Window 3's widgets
    def create_window3_widgets(self):

        # Header
        self.header = Label(self,
                            text = """SAX Representation""",
                            background = "gray90", font = "Arial 15 underline")
        self.header.grid(row = 0,column = 0, columnspan = 15, sticky = W)

        # Instructions
        self.instructions = Label(self,
                            text = "    For each sensor- select whether or not \
to include SAX features as feature vectors. \
If including SAX features, input a word length and number of letters.",
                            background = "gray90", font = "Arial 14",
                            wraplength = "550", justify = "left")
        self.instructions.grid(row = 1,column = 0, columnspan = 22, sticky = W)

        # Line Break
        self.break00= Label(self, background = "gray90")
        self.break00.grid(row = 2, column = 0)

        # fNIRS:
        # If selected, create widgets for customizing SAX features
        if "fNIRS" in selected_sensors:

            # Header
            self.fNIRS_Header = Label(self,text = "fNIRS", background = "gray90",
                                font = "Arial 14 bold", justify = "left")
            self.fNIRS_Header.grid(row = 3, column = 1, sticky = W)

            # SAX Checkbutton and Header
            self.fNIRS_SAX = IntVar()
            self.fNIRS_SAX_Check = Checkbutton(self, variable = self.fNIRS_SAX,
                command = self.update_fNIRS_SAX, background = "gray90")
            self.fNIRS_SAX_Check.grid(row = 4, column = 1, sticky = E)

            self.fNIRS_SAX_Header = Label(self,text = "  SAX",
                background = "gray90", font = "Arial 14")
            self.fNIRS_SAX_Header.grid(row = 4, column = 2,
                columnspan = 3, sticky = W)

            # SAX Word Header and Entry
            self.fNIRS_SAX_Word_Header = Label(self,text = "    Word Length",
                background = "gray90", font = "Arial 14", state = DISABLED)
            self.fNIRS_SAX_Word_Header.grid(row = 5, column = 2, sticky = W)

            self.fNIRS_SAX_Word = Entry(self, justify = "right",
                state = DISABLED)
            self.fNIRS_SAX_Word.grid(row = 5, column = 3)

            # SAX Letter Header, Entry, and Instructions
            self.fNIRS_SAX_Letter_Header = Label(self,
                text = "    Number of Letters", background = "gray90",
                font = "Arial 14", state = DISABLED)
            self.fNIRS_SAX_Letter_Header.grid(row = 6, column = 2, sticky = W)
            self.fNIRS_SAX_Letter = Entry(self, justify = "right",
                state = DISABLED)
            self.fNIRS_SAX_Letter.grid(row = 6, column = 3)

            self.fNIRS_Letter_instructions = Label(self,
                text = "    Letter must be between 3 and 20, non-inclusive.",
                background = "gray90", font = "Arial 11", state = DISABLED)
            self.fNIRS_Letter_instructions.grid(row = 7, column = 2,
                columnspan = 4, sticky = W)

            # Line Break
            self.break1 = Label(self, background = "gray90")
            self.break1.grid(row = 7, column = 0)

        # EEG:
        # If selected, create widgets for customizing SAX features
        if "EEG" in selected_sensors:

            # Header
            self.EEG_Header = Label(self,text = "EEG", background = "gray90",
                font = "Arial 14 bold", justify = "left")
            self.EEG_Header.grid(row = 9, column = 1, sticky = W)

            # SAX Checkbutton and Header
            self.EEG_SAX = IntVar()
            self.EEG_SAX_Check = Checkbutton(self, variable = self.EEG_SAX,
                command = self.update_EEG_SAX, background = "gray90")
            self.EEG_SAX_Check.grid(row = 10, column = 1, sticky = E)
            self.EEG_SAX_Header = Label(self,text = "  SAX",
                background = "gray90", font = "Arial 14")
            self.EEG_SAX_Header.grid(row = 10, column = 2, sticky = W)

            # SAX Word Header and Entry
            self.EEG_SAX_Word_Header = Label(self,text = "    Word Length",
                background = "gray90", font = "Arial 14", state = DISABLED)
            self.EEG_SAX_Word_Header.grid(row = 11, column = 2, sticky = W)
            self.EEG_SAX_Word = Entry(self, state = DISABLED, justify = "right")
            self.EEG_SAX_Word.grid(row = 11, column = 3)

            # SAX Letter Header, Entry, and Instructions
            self.EEG_SAX_Letter_Header = Label(self,
                text = "    Number of Letters", background = "gray90",
                font = "Arial 14", state = DISABLED)
            self.EEG_SAX_Letter_Header.grid(row = 12, column = 2, sticky = W)
            self.EEG_SAX_Letter = Entry(self, state = DISABLED,
                justify = "right")
            self.EEG_SAX_Letter.insert(END, "SAX Letter")
            self.EEG_SAX_Letter.grid(row = 12, column = 3)

            self.EEG_Letter_instructions = Label(self,
                text = "    Letter must be between 3 and 20, non-inclusive.",
                background = "gray90", font = "Arial 11", state = DISABLED)
            self.EEG_Letter_instructions.grid(row = 13, column = 2,
                columnspan = 4, sticky = W)

            # Line Break
            self.break2 = Label(self, background = "gray90")
            self.break2.grid(row = 13, column = 0)

        # Respiration:
        # If selected, create widgets for customizing SAX features
        if "Respiration" in selected_sensors:

            # Header
            self.Respiration_Header = Label(self,text = "Respiration",
                background = "gray90", font = "Arial 14 bold", justify = "left")
            self.Respiration_Header.grid(row = 15, column = 1, sticky = W)

            # SAX Checkbutton and Header
            self.Respiration_SAX = IntVar()
            self.Respiration_SAX_Check = Checkbutton(self,
                variable = self.Respiration_SAX,
                command = self.update_Respiration_SAX, background = "gray90")
            self.Respiration_SAX_Check.grid(row = 16, column = 1, sticky = E)
            self.Respiration_SAX_Header = Label(self,text = "  SAX",
                background = "gray90", font = "Arial 14")
            self.Respiration_SAX_Header.grid(row = 16, column = 2, sticky = W)

            # SAX Word Header and Entry
            self.Respiration_SAX_Word_Header = Label(self,
                text = "    Word Length", background = "gray90",
                font = "Arial 14", state = DISABLED)
            self.Respiration_SAX_Word_Header.grid(row = 17, column = 2,
                sticky = W)
            self.Respiration_SAX_Word = Entry(self, state = DISABLED,
                justify = "right")
            self.Respiration_SAX_Word.grid(row = 17, column = 3)

            # SAX Letter Header, Entry, and Instructions
            self.Respiration_SAX_Letter_Header = Label(self,
                text = "    Number of Letters", background = "gray90",
                font = "Arial 14", state = DISABLED)
            self.Respiration_SAX_Letter_Header.grid(row = 18, column = 2,
                sticky = W)
            self.Respiration_SAX_Letter = Entry(self, state = DISABLED,
                justify = "right")
            self.Respiration_SAX_Letter.grid(row = 18, column = 3)

            self.Respiration_Letter_instructions = Label(self,
                text = "    Letter must be between 3 and 20, non-inclusive.",
                background = "gray90", font = "Arial 11", state = DISABLED)
            self.Respiration_Letter_instructions.grid(row = 19, column = 2,
                columnspan = 4, sticky = W)

            # Line Break
            self.break3 = Label(self, background = "gray90")
            self.break3.grid(row = 19, column = 0)

        # ECG:
        # If selected, create widgets for customizing SAX features
        if "ECG" in selected_sensors:

            # Header
            self.ECG_Header = Label(self,text = "ECG", background = "gray90",
                font = "Arial 14 bold", justify = "left")
            self.ECG_Header.grid(row = 21, column = 1, sticky = W)

            # SAX Checkbutton and Header
            self.ECG_SAX = IntVar()
            self.ECG_SAX_Check = Checkbutton(self, variable = self.ECG_SAX,
                command = self.update_ECG_SAX, background = "gray90")
            self.ECG_SAX_Check.grid(row = 22, column = 1, sticky = E)
            self.ECG_SAX_Header = Label(self,text = "  SAX",
                background = "gray90", font = "Arial 14")
            self.ECG_SAX_Header.grid(row = 23, column = 2, sticky = W)

            # SAX Word Header and Entry
            self.ECG_SAX_Word_Header = Label(self,
                text = "    Word Length", background = "gray90",
                font = "Arial 14", state = DISABLED)
            self.ECG_SAX_Word_Header.grid(row = 24, column = 2, sticky = W)
            self.ECG_SAX_Word = Entry(self, state = DISABLED, justify = "right")
            self.ECG_SAX_Word.grid(row = 24, column = 3)

            # SAX Letter Header, Entry, and Instructions
            self.ECG_SAX_Letter_Header = Label(self,
                text = "    Number of Letters", background = "gray90",
                font = "Arial 14", state = DISABLED)
            self.ECG_SAX_Letter_Header.grid(row = 25, column = 2, sticky = W)
            self.ECG_SAX_Letter = Entry(self, state = DISABLED,
                justify = "right")
            self.ECG_SAX_Letter.grid(row = 25, column = 3)

            self.ECG_Letter_instructions = Label(self,
                text = "    Letter must be between 3 and 20, non-inclusive.",
                background = "gray90", font = "Arial 11", state = DISABLED)
            self.ECG_Letter_instructions.grid(row = 26, column = 2,
                columnspan = 4, sticky = W)

            # Line Break
            self.break4 = Label(self, background = "gray90")
            self.break4.grid(row = 26, column = 0)

        # EDA:
        # If selected, create widgets for customizing SAX features
        if "EDA" in selected_sensors:

            # Header
            self.EDA_Header = Label(self,text = "EDA",
                background = "gray90", font = "Arial 14 bold", justify = "left")
            self.EDA_Header.grid(row = 28, column = 1, sticky = W)

            # SAX Checkbutton and Header
            self.EDA_SAX = IntVar()
            self.EDA_SAX_Check = Checkbutton(self, variable = self.EDA_SAX,
                command = self.update_EDA_SAX, background = "gray90")
            self.EDA_SAX_Check.grid(row = 29, column = 1, sticky = E)
            self.EDA_SAX_Header = Label(self,text = "  SAX",
                background = "gray90", font = "Arial 14")
            self.EDA_SAX_Header.grid(row = 29, column = 2, sticky = W)

            # SAX Word Header and Entry
            self.EDA_SAX_Word_Header = Label(self,text = "    Word Length",
                background = "gray90", font = "Arial 14", state = DISABLED)
            self.EDA_SAX_Word_Header.grid(row = 30, column = 2, sticky = W)
            self.EDA_SAX_Word = Entry(self, state = DISABLED, justify = "right")
            self.EDA_SAX_Word.grid(row = 30, column = 3)

            # SAX Letter Header, Entry, and Instructions
            self.EDA_SAX_Letter_Header = Label(self,
                text = "    Number of Letters", background = "gray90",
                font = "Arial 14", state = DISABLED)
            self.EDA_SAX_Letter_Header.grid(row = 31, column = 2, sticky = W)
            self.EDA_SAX_Letter = Entry(self, state = DISABLED,
                justify = "right")
            self.EDA_SAX_Letter.grid(row = 31, column = 3)

            self.EDA_Letter_instructions = Label(self,
                text = "    Letter must be between 3 and 20, non-inclusive.",
                background = "gray90", font = "Arial 11", state = DISABLED)
            self.EDA_Letter_instructions.grid(row = 32, column = 2,
                columnspan = 4, sticky = W)

            # Line Break
            self.break5 = Label(self, background = "gray90")
            self.break5.grid(row = 32, column = 0)

        # Back Button (return to window2)
        self.back_button = Button(self, text = "Back",
            command = self.back_window2, font = "Arial 14")
        self.back_button.grid(row = 34, column = 1, sticky = W)

        # Next Button (move on to window 4)
        self.next_button = Button(self, text = "Next",
            command = self.next_window4, font = "Arial 14")
        self.next_button.grid(row = 34, column = 20)

################################################################################
#End of creating Window 3's widgets
################################################################################

# Function for fNIRS SAX Checkbutton
# Enable the widgets for SAX input if checked
# and disabled them if unchecked.
    def update_fNIRS_SAX(self):

        if (self.fNIRS_SAX.get() == 1):
            self.fNIRS_SAX_Word_Header["state"] = NORMAL
            self.fNIRS_SAX_Letter_Header["state"] = NORMAL
            self.fNIRS_SAX_Word["state"] = NORMAL
            self.fNIRS_SAX_Letter["state"] = NORMAL
            self.fNIRS_Letter_instructions["state"] = NORMAL
            self.SAX_Bool.append(self.fNIRS_SAX_Word)
            self.SAX_Bool.append(self.fNIRS_SAX_Letter)

        else:
            self.fNIRS_SAX_Word_Header["state"] = DISABLED
            self.fNIRS_SAX_Letter_Header["state"] = DISABLED
            self.fNIRS_SAX_Word["state"] = DISABLED
            self.fNIRS_SAX_Letter["state"] = DISABLED
            self.fNIRS_Letter_instructions["state"] = DISABLED
            self.SAX_Bool.remove(self.fNIRS_SAX_Word)
            self.SAX_Bool.remove(self.fNIRS_SAX_Letter)

# Function for EEG SAX Checkbutton
# Enable the widgets for SAX input if checked
# and disabled them if unchecked.
    def update_EEG_SAX(self):

        if (self.EEG_SAX.get() == 1):
            self.EEG_SAX_Word_Header["state"] = NORMAL
            self.EEG_SAX_Letter_Header["state"] = NORMAL
            self.EEG_SAX_Word["state"] = NORMAL
            self.EEG_SAX_Letter["state"] = NORMAL
            self.EEG_Letter_instructions["state"] = NORMAL
            self.SAX_Bool.append(self.EEG_SAX_Word)
            self.SAX_Bool.append(self.EEG_SAX_Letter)

        else:
            self.EEG_SAX_Word_Header["state"] = DISABLED
            self.EEG_SAX_Letter_Header["state"] = DISABLED
            self.EEG_SAX_Word["state"] = DISABLED
            self.EEG_SAX_Letter["state"] = DISABLED
            self.EEG_Letter_instructions["state"] = DISABLED
            self.SAX_Bool.remove(self.EEG_SAX_Word)
            self.SAX_Bool.remove(self.EEG_SAX_Letter)

# Function for Respiration SAX Checkbutton
# Enable the widgets for SAX input if checked
# and disabled them if unchecked.
    def update_Respiration_SAX(self):

        if (self.Respiration_SAX.get() == 1):
            self.Respiration_SAX_Word_Header["state"] = NORMAL
            self.Respiration_SAX_Letter_Header["state"] = NORMAL
            self.Respiration_SAX_Word["state"] = NORMAL
            self.Respiration_SAX_Letter["state"] = NORMAL
            self.Respiration_Letter_instructions["state"] = NORMAL
            self.SAX_Bool.append(self.Respiration_SAX_Word)
            self.SAX_Bool.append(self.Respiration_SAX_Letter)

        else:
            self.Respiration_SAX_Word_Header["state"] = DISABLED
            self.Respiration_SAX_Letter_Header["state"] = DISABLED
            self.Respiration_SAX_Word["state"] = DISABLED
            self.Respiration_SAX_Letter["state"] = DISABLED
            self.Respiration_Letter_instructions["state"] = DISABLED
            self.SAX_Bool.remove(self.Respiration_SAX_Word)
            self.SAX_Bool.remove(self.Respiration_SAX_Letter)

# Function for ECG SAX Checkbutton
# Enable the widgets for SAX input if checked
# and disabled them if unchecked.
    def update_ECG_SAX(self):

        if (self.ECG_SAX.get() == 1):
            self.ECG_SAX_Word_Header["state"] = NORMAL
            self.ECG_SAX_Letter_Header["state"] = NORMAL
            self.ECG_SAX_Word["state"] = NORMAL
            self.ECG_SAX_Letter["state"] = NORMAL
            self.ECG_Letter_instructions["state"] = NORMAL
            self.SAX_Bool.append(self.ECG_SAX_Word)
            self.SAX_Bool.append(self.ECG_SAX_Letter)

        else:
            self.ECG_SAX_Word_Header["state"] = DISABLED
            self.ECG_SAX_Letter_Header["state"] = DISABLED
            self.ECG_SAX_Word["state"] = DISABLED
            self.ECG_SAX_Letter["state"] = DISABLED
            self.ECG_Letter_instructions["state"] = DISABLED
            self.SAX_Bool.remove(self.ECG_SAX_Word)
            self.SAX_Bool.remove(self.ECG_SAX_Letter)

# Function for EDA SAX Checkbutton
# Enable the widgets for SAX input if checked
# and disabled them if unchecked.
    def update_EDA_SAX(self):

        if (self.EDA_SAX.get() == 1):
            self.EDA_SAX_Word_Header["state"] = NORMAL
            self.EDA_SAX_Letter_Header["state"] = NORMAL
            self.EDA_SAX_Word["state"] = NORMAL
            self.EDA_SAX_Letter["state"] = NORMAL
            self.EDA_Letter_instructions["state"] = NORMAL
            self.SAX_Bool.append(self.EDA_SAX_Word)
            self.SAX_Bool.append(self.EDA_SAX_Letter)
        else:
            self.EDA_SAX_Word_Header["state"] = DISABLED
            self.EDA_SAX_Letter_Header["state"] = DISABLED
            self.EDA_SAX_Word["state"] = DISABLED
            self.EDA_SAX_Letter["state"] = DISABLED
            self.EDA_Letter_instructions["state"] = DISABLED
            self.SAX_Bool.remove(self.EDA_SAX_Word)
            self.SAX_Bool.remove(self.EDA_SAX_Letter)

# Function for Back Button
# Return to Window 2
    def back_window2(self):

        # Remove last 11 entries of output (11 added from window 2) to reset
        # for new selected output from user
        for i in range(11):
            output.pop()

        #Show Window 2 and delete Window 3
        self.master.show_frame(window2)
        self.master.close_frame(window3)

# Function for Next Button
# Check if the paramters inputted are correct. If they are, then create and
# show Window 4. If they are not, then show an error message.
    def next_window4(self):

        SAX_good = True # Boolean to keep track of correctness of parameters
        error_message = "" # Initialize a string to store a customized
                        # error message to display if the paremters are wrong

        # For the sensors where SAX is True,
        # check if both SAX Word and Letter input are integers.
        for widget in self.SAX_Bool:
            if not widget.get():
                SAX_good = False
                error_message += "Both SAX Word and Letter must be filled out."
                break

            elif not widget.get().isdigit():
                SAX_good = False
                error_message += "SAX Word and Letter values must be integers."
                break

        # If SAX Word and Letter are both integers,
        # then check that SAX Letter is between 3 and 20, non-inclusive.
        if SAX_good:
            for widget in self.SAX_Bool[1::2]:
                if (int(widget.get()) <= 3) or (int(widget.get()) >= 20):
                    SAX_good = False
                    error_message += "SAX Letter must be between 3 and 20,\
 non-inclusive."
                    break

        # If the SAX parameters are good, then write the paramters to the output
        # string, and move on to Window 4.
        if SAX_good:
            output.append("\nSAX Parameters\n")

            # If fNIRS was selected and fNIRS SAX is True,
            # then add the inputted values to the output string.
            if "fNIRS" in selected_sensors:
                if (self.fNIRS_SAX.get() == 1):
                    output.append("fNIRS SAX: True\n")
                    output.append("fNIRS SAX Word: " +
                        self.fNIRS_SAX_Word.get() + "\n")
                    output.append("fNIRS SAX Letter: " +
                        self.fNIRS_SAX_Letter.get() + "\n")

            # If fNIRS was not selected or fNIRS SAX is False,
            # then output the fNIRS SAX paramters as False and 0.
                else:
                    output.append("fNIRS SAX: False\n")
                    output.append("fNIRS SAX Word: 0\n")
                    output.append("fNIRS SAX Letter: 0\n")

            else:
                output.append("fNIRS SAX: False\n")
                output.append("fNIRS SAX Word: 0\n")
                output.append("fNIRS SAX Letter: 0\n")

            # If EEG was selected and EEG SAX is True,
            # then add the inputted values to the output string.
            if "EEG" in selected_sensors:
                if (self.EEG_SAX.get() == 1):
                    output.append("EEG SAX: True\n")
                    output.append("EEG SAX Word: " +
                        self.EEG_SAX_Word.get() + "\n")
                    output.append("EEG SAX Letter: " +
                        self.EEG_SAX_Letter.get() + "\n")

            # If EEG was not selected or EEG SAX is False,
            # then output the EEG SAX paramters as False and 0.
                else:
                    output.append("EEG SAX: False\n")
                    output.append("EEG SAX Word: 0\n")
                    output.append("EEG SAX Letter: 0\n")

            else:
                output.append("EEG SAX: False\n")
                output.append("EEG SAX Word: 0\n")
                output.append("EEG SAX Letter: 0\n")

            # If Respiration was selected and Respiration SAX is True,
            # then add the inputted values to the output string.
            if "Respiration" in selected_sensors:
                if (self.Respiration_SAX.get() == 1):
                    output.append("Respiration SAX: True\n")
                    output.append("Respiration SAX Word: " +
                        self.Respiration_SAX_Word.get() + "\n")
                    output.append("Respiration SAX Letter: " +
                        self.Respiration_SAX_Letter.get() + "\n")

            # If Respiration was not selected or Respiration SAX is False,
            # then output the Respiration SAX paramters as False and 0.
                else:
                    output.append("Respiration SAX: False\n")
                    output.append("Respiration SAX Word: 0\n")
                    output.append("Respiration SAX Letter: 0\n")
            else:
                output.append("Respiration SAX: False\n")
                output.append("Respiration SAX Word: 0\n")
                output.append("Respiration SAX Letter: 0\n")

            # If ECG was selected and ECG SAX is True,
            # then add the inputted values to the output string.
            if "ECG" in selected_sensors:
                if (self.ECG_SAX.get() == 1):
                    output.append("ECG SAX: True\n")
                    output.append("ECG SAX Word: " +
                        self.ECG_SAX_Word.get() + "\n")
                    output.append("ECG SAX Letter: " +
                        self.ECG_SAX_Letter.get() + "\n")

            # If ECG was not selected or ECG SAX is False,
            # then output the ECG SAX paramters as False and 0.
                else:
                    output.append("ECG SAX: False\n")
                    output.append("ECG SAX Word: 0\n")
                    output.append("ECG SAX Letter: 0\n")
            else:
                output.append("ECG SAX: False\n")
                output.append("ECG SAX Word: 0\n")
                output.append("ECG SAX Letter: 0\n")

            # If EDA was selected and EDA SAX is True,
            # then add the inputted values to the output string.
            if "EDA" in selected_sensors:
                if (self.EDA_SAX.get() == 1):
                    output.append("EDA SAX: True\n")
                    output.append("EDA SAX Word: " +
                        self.EDA_SAX_Word.get() + "\n")
                    output.append("EDA SAX Letter: " +
                        self.EDA_SAX_Letter.get() + "\n")

            # If EDA was not selected or EDA SAX is False,
            # then output the EDA SAX paramters as False and 0.
                else:
                    output.append("EDA SAX: False\n")
                    output.append("EDA SAX Word: 0\n")
                    output.append("EDA SAX Letter: 0\n")
            else:
                output.append("EDA SAX: False\n")
                output.append("EDA SAX Word: 0\n")
                output.append("EDA SAX Letter: 0\n")


            # Create and show Window 4
            self.master.create_frame(window4)
            self.master.show_frame(window4)

        # If the SAX parameters were not inputted correctly,
        # then display a customized error message.
        else:
            tkMessageBox.showerror("Invalid Entry", error_message)

################################################################################

# 4th Window: Selecting Machine Learning Parameters, Output Options, and
#             Extension for Machine Learning Output

################################################################################

class window4(Frame):
    def __init__(self, master):
        """Intitialize Frame"""
        Frame.__init__(self, master, background = "gray90")
        self.master= master
        self.grid()
        self.create_window4_widgets()

# Create Window 4's widgets
    def create_window4_widgets(self):

        # Header
        self.header = Label(self,
                            text = """Machine Learning Parameters""",
                            background = "gray90", font = "Arial 15 underline")
        self.header.grid(row = 0,column = 0, columnspan = 15, sticky = W)

        # Instructions
        self.instructions = Label(self,
                            text = "    All fields on this page \
must be filled out.",
                            background = "gray90", font = "Arial 14",
                            wraplength = "550", justify = "left")
        self.instructions.grid(row = 1,column = 0, columnspan = 22, sticky = W)

        # Line Break
        self.break00= Label(self, background = "gray90")
        self.break00.grid(row = 2, column = 0)

        # Conditions: Header and Entry
        self.conditionsHeader = Label(self, text = "Conditions: ",
            background = "gray90", font = "Arial 14 bold")
        self.conditionsHeader.grid(row = 5, column = 1, sticky = W,
            columnspan = 2)

        self.conditions = StringVar()
        self.conditionsEntry = Entry(self, textvariable = self.conditions,
            justify = "right")
        self.conditionsEntry.grid(row = 5, column = 3, columnspan = 5, sticky = W)

        # Empty space to write error message when needed
        self.error_message1 = Label(self, background = "gray90", fg = "Red",
            font = "Arial 11", width = 33, justify = "left")
        self.error_message1.grid(row = 5, column = 9, columnspan = 7,
            sticky = W)

        # Conditions instructions
        self.conditions_instructions = Label(self,
            text = """Seperate each condition number with a comma. (e.g. 1, 2)\
\nNOTE: Must have at least 1 condition.\n""",
            background = "gray90", font = "Arial 11", wraplength = "350",
            justify = "left")
        self.conditions_instructions.grid(row = 6,column = 1,
            rowspan = 3, columnspan = 5, sticky = W)

        # Line Break
        self.break0= Label(self, background = "gray90")
        self.break0.grid(row = 8, column = 0)

        # Orange Input: neighbor(num_k)
        # neigbors(num_k) Header
        self.neighborsHeader = Label(self,
            text = "Number of Neighbors (num_k): ",
            background = "gray90", font = "Arial 14 bold")
        self.neighborsHeader.grid(row = 9, column = 1, columnspan = 8,
            sticky = W )

        # neighbors(num_k) Entry
        self.num_k = StringVar()
        self.neighborsEntry = Entry(self, textvariable = self.num_k, width = 3)
        self.neighborsEntry.insert(0, "10")
        self.neighborsEntry.grid(row = 9, column = 9, columnspan = 2,
            sticky = E)

        # neighbors(num_k_) Error Message
        self.neighbors_error_message = Label (self, background = "gray90",
            fg = "Red", font = "Arial 11", justify = "left")
        self.neighbors_error_message.grid(row = 9, column = 12, columnspan = 5,
            sticky = W)

        # Orange Input: feature selection importance(n_num)
        # feature selection importance(n_num) Header
        self.importanceHeader = Label(self,
            text = "Feature Selection Importance (n_num): ",
            background = "gray90", font = "Arial 14 bold")
        self.importanceHeader.grid(row = 10, column = 1, columnspan = 8,
            sticky = W)

        # feature selection importance(n_num) Entry
        self.n_num = StringVar()
        self.importanceEntry = Entry(self, textvariable = self.n_num, width = 4)
        self.importanceEntry.insert(0, "100")
        self.importanceEntry.grid(row = 10, column = 9, columnspan = 2,
            sticky = E)

        # feature selection importance(n_num) Error Message
        self.importance_error_message = Label (self, background = "gray90",
            fg = "Red", font = "Arial 11", justify = "left")
        self.importance_error_message.grid(row = 10, column = 12,
            columnspan = 5, sticky = W)

        # Line Break
        self.break1 = Label(self, background = "gray90")
        self.break1.grid(row = 11, column = 0)

        # Orange Input: feature selection fractions
        # feature selection fractions Header
        self.fraction_header = Label(self,
            text = "Number of top features to select \
(in terms of importance):",
            background = "gray90", font = "Arial 14 bold", justify = "left")
        self.fraction_header.grid(row = 12,column = 1, columnspan = 14,
            sticky = W)

        # feature selection fractions Instructions
        self.fraction_instruction = Label(self,
            text = "If you input '100', then the top 1/100 features will be \
selected.\nYou must input two numbers.",
            background = "gray90", font = "Arial 11", justify = "left")
        self.fraction_instruction.grid(row = 13,column = 1, columnspan = 13, sticky = W)

        # fraction 1 Entry
        self.fraction1 = StringVar()
        self.fraction1_entry= Entry(self, textvariable = self.fraction1,
            width = 6)
        self.fraction1_entry.grid( row = 12, column = 16, sticky = W)

        # fraction 2 Entry
        self.fraction2 = StringVar()
        self.fraction2_entry = Entry(self, textvariable = self.fraction2,
            width = 6)
        self.fraction2_entry.grid( row = 13, column = 16, sticky = W)

        #Line Break
        self.break2 = Label(self, background = "gray90")
        self.break2.grid(row = 14)

        # Output Options
        # Header & Instructions
        self.header = Label(self,
                            text = """Output Options""",
                            background = "gray90", font = "Arial 15 underline")
        self.header.grid(row = 15,column = 0, columnspan = 9, sticky = W)

        self.instructions = Label(self,
                            text = "    Select which files you want to output.",
                            background = "gray90", font = "Arial 14",
                            justify = "left")
        self.instructions.grid(row = 16,column = 0,
            rowspan = 2, columnspan = 15, sticky = W)

        # Line Break
        self.break3 = Label(self, background = "gray90")
        self.break3.grid(row = 19, column = 0)

        # Default Output Radiobutton & Header
        self.default_output = BooleanVar()
        self.default_output.set(True)
        self.default_button = Radiobutton(self, variable = self.default_output,
            command = self.default_options, background = "gray90", value = True)
        self.default_button.grid(row = 20, column = 1, sticky = W)
        self.default_Header= Label(self,
            text = "Default (output all the .arff and Machine Learning files,\
 does not output .tab files.)",
            background = "gray90", font = "Arial 14")
        self.default_Header.grid(row = 20, column = 2, sticky = W,
            columnspan = 20)

        #Custom Output Radiobutton & Header
        self.custom_Check = Radiobutton(self, variable = self.default_output,
            command = self.custom_options, background = "gray90", value = False)
        self.custom_Check.grid(row = 21, column = 1, sticky = W)
        self.custom_Header= Label(self,text = "Custom", background = "gray90",
            font = "Arial 14")
        self.custom_Header.grid(row = 21, column = 2, columnspan = 2,
            sticky = W)


        # Custom Output Options
        # Orginally disabled, becomes avaliable when
        # the Custom Output Radiobutton is selected

        # Checkbox to output .arff files for each subject
        self.each_ARFF = BooleanVar()
        self.each_ARFF_Check = Checkbutton(self, variable = self.each_ARFF,
            background = "gray90", state = DISABLED)
        self.each_ARFF_Check.grid(row = 22, column = 2, sticky = E)
        self.each_ARFF_Header= Label(self,
            text = "  .arff file  (for each data file)", background = "gray90",
            font = "Arial 14", state = DISABLED)
        self.each_ARFF_Header.grid(row = 22, column = 3, columnspan = 15,
            sticky = W)

        # Checkbox to output .arff files for across subjects
        self.all_ARFF = BooleanVar()
        self.all_ARFF_Check = Checkbutton(self, variable = self.all_ARFF,
            background = "gray90", state = DISABLED)
        self.all_ARFF_Check.grid(row = 23, column = 2, sticky = E)
        self.all_ARFF_Header= Label(self,
            text = "  .arff file (for across subjects)", background = "gray90",
            font = "Arial 14", state = DISABLED)
        self.all_ARFF_Header.grid(row = 23, column = 3, columnspan = 15,
            sticky = W)

        # Checkbox to output .tab files for each subject
        self.each_Tab = BooleanVar()
        self.each_Tab_Check = Checkbutton(self, variable = self.each_Tab,
            background = "gray90", state = DISABLED)
        self.each_Tab_Check.grid(row = 24, column = 2, sticky = E)
        self.each_Tab_Header= Label(self,
            text = "  arff file as a tab file (for each subject)",
            background = "gray90", font = "Arial 14", state = DISABLED)
        self.each_Tab_Header.grid(row = 24, column = 3, columnspan = 15,
            sticky = W)

        # Checkbox to output .tab files for across subjects
        self.all_Tab = BooleanVar()
        self.all_Tab_Check = Checkbutton(self, variable = self.all_Tab,
            background = "gray90", state = DISABLED)
        self.all_Tab_Check.grid(row = 25, column = 2, sticky = E)
        self.all_Tab_Header= Label(self,
            text = "  arff file as a tab file (for across subjects)",
            background = "gray90", font = "Arial 14", state = DISABLED)
        self.all_Tab_Header.grid(row = 25, column = 3, columnspan = 15,
            sticky = W)

        # Checkbox to perform machine learning on each subject
        self.each_ML = BooleanVar()
        self.each_ML_Check = Checkbutton(self, variable = self.each_ML,
            background = "gray90", state = DISABLED)
        self.each_ML_Check.grid(row = 26, column = 2, sticky = E)
        self.each_ML_Header= Label(self,
            text = "  Machine Learning results (for each subject)",
            background = "gray90", font = "Arial 14", state = DISABLED)
        self.each_ML_Header.grid(row = 26, column = 3, columnspan = 17, sticky = W)

        # Checkbox to perform machine learning on across subjects
        self.all_ML = BooleanVar()
        self.all_ML_Check = Checkbutton(self, variable = self.all_ML,
            background = "gray90", state = DISABLED)
        self.all_ML_Check.grid(row = 27, column = 2, sticky = E)
        self.all_ML_Header= Label(self,
            text = "  Machine Learning results (for across subjects)",
            background = "gray90", font = "Arial 14", state = DISABLED)
        self.all_ML_Header.grid(row = 27, column = 3, columnspan = 17,
            sticky = W)

        #Line Break
        self.break4 = Label(self, background = "gray90")
        self.break4.grid(row = 28)

        # Extension for machine learning output files
        # Header
        self.extension_header = Label(self,
            text = """     Extension for machine learning output: """,
            background = "gray90", font = "Arial 14 bold")
        self.extension_header.grid(row = 29, column = 0, columnspan = 6,
            sticky = W)

        # Instructions
        self.extension_instructions = Label(self,
            text = "     Should always end in .csv (eg. _1v2_rio_yes.csv)",
            background = "gray90", font = "Arial 11")
        self.extension_instructions.grid(row = 30, column =0, columnspan = 6,
            sticky = W)

        # Extension entry
        self.extension = StringVar()
        self.extensionEntry = Entry(self, textvariable = self.extension,
            justify = "right")
        self.extensionEntry.grid(row = 31, column = 2, columnspan = 6)

        # Extensions error message
        self.error_message2 = Label(self, background = "gray90", fg = "Red",
            font = "Arial 11", justify = "left")
        self.error_message2.grid(row = 32, column = 2, columnspan = 6)

        # Line Break
        self.break5 = Label(self, background = "gray90")
        self.break5.grid(row = 33)

        # Back Button (return to Window 3)
        self.back_button = Button(self, text = "Back",
            command = self.back_window3, font = "Arial 14")
        self.back_button.grid(row = 34, column = 1, stick = W)

        # Next Button (Move on to Window 5)
        self.next_button = Button(self, text = "Next",
            command = self.next_window5, font = "Arial 14")
        self.next_button.grid(row = 34, column = 16, sticky = E)

################################################################################
#End of creating Window 4's widgets
################################################################################

# Function for Default Output Radiobutton
# If selected, the the options for Custom Output become disabled.
    def default_options(self):
        self.default_output.set(True)
        for widget in [self.each_ARFF_Check, self.each_ARFF_Header, self.all_ARFF_Check, self.all_ARFF_Header, self.each_Tab_Check,
                    self.each_Tab_Header, self.all_Tab_Check, self.all_Tab_Header, self.each_ML_Check, self.each_ML_Header,
                    self.all_ML_Check, self.all_ML_Header]:
            widget["state"] = DISABLED

# Function for Custom Output Radiobutton
# If selected, the the options for Custom Output become accessible.
    def custom_options(self):

        self.default_output.set(False)
        for widget in [self.each_ARFF_Check, self.each_ARFF_Header, self.all_ARFF_Check, self.all_ARFF_Header, self.each_Tab_Check,
                        self.each_Tab_Header, self.all_Tab_Check, self.all_Tab_Header, self.each_ML_Check, self.each_ML_Header,
                        self.all_ML_Check, self.all_ML_Header]:
            widget["state"] = NORMAL

# Function for Back Button
# Return to Window 3
    def back_window3(self):

        # Remove last 16 entries of output (16 added from window 3) to reset
        # for new selected output from user.
        for i in range(16):
            output.pop()

        # Show Window 3 and delete Window 4
        self.master.show_frame(window3)
        self.master.close_frame(window4)

# Function for Next Button
# Move on to Window 5
    def next_window5(self):

        # Clear all in-window error messages.
        self.error_message1.config(text = "")
        self.error_message2.config(text = "")
        self.neighbors_error_message.config(text = "")
        self.importance_error_message.config(text = "")

        # Check if all the parameters entered are correct.
        # If they are, then add them to the output.
        if self.parameters_good(self.conditions.get(), self.num_k.get(),
            self.n_num.get(), self.extension.get(), self.fraction1_entry.get(),
            self.fraction2_entry.get()):

            # Add title to output
            output.append("\nMachine Learning Parameters\n")

            # Add appropriate output values
            output.append("Conditions: " + self.conditions.get() + "\n")
            output.append("num_k: " + self.num_k.get() + "\n")
            output.append("n_num: " + self.n_num.get() + "\n")
            output.append("Top Features: " + "1/" + self.fraction1_entry.get() +
             ", 1/" + self.fraction2_entry.get() + "\n")

            output.append("\nOutput\n")

            # If Default Outputs is selected,
            # then add the default outputs to the output string.
            if self.default_output.get() == True:
                 output.append("Each_arff: True\n")
                 output.append("All_arff: True\n")
                 output.append("Each_Tab: False\n")
                 output.append("All_Tab: False\n")
                 output.append("Each_ML: True\n")
                 output.append("All_ML: True\n")

            # If Custom Outputs is selected,
            # then add to the output string the selected Output Options as True
            # and the not selected Output Options as False.
            else:

                if (self.each_ARFF.get()):
                    output.append("Each_arff: True\n")
                else:
                    output.append("Each_arff: False\n")
                if (self.all_ARFF.get()):
                    output.append("All_arff: True\n")
                else:
                    output.append("All_arff: False\n")
                if (self.each_Tab.get()):
                    output.append("Each_Tab: True\n")
                else:
                    output.append("Each_Tab: False\n")
                if (self.all_Tab.get()):
                    output.append("All_Tab: True\n")
                else:
                    output.append("All_Tab: False\n")
                if (self.each_ML.get()):
                    output.append("Each_ML: True\n")
                else:
                    output.append("Each_ML: False\n")
                if (self.all_ML.get()):
                    output.append("All_ML: True\n")
                else:
                    output.append("All_ML: False\n")

            # Add the extension to the output string.
            output.append("\nExtension: " + self.extension.get() + "\n")

            # Create and show Window 5
            self.master.create_frame(window5)
            self.master.show_frame(window5)

# Function used in next_window5 to check if the paramters inputted were correct
    def parameters_good(self, conditions, num_k, n_num, extension,
        fraction1, fraction2):

        all_good = True # Boolean to keep track of correctness of the parameters

        # Check that Conditions has been filled out.
        # If not, display an error message.
        if not conditions:
            all_good = False
            self.conditionsEntry.delete(0, END)
            self.error_message1.config(
                text = "Must enter at least one condition")

        # Check if condition(s) is in int,int,int format.
        # If not, display an error message.
        else:
            conditionsRE = re.compile('\d+(,\s?\d+)*$')
            match = conditionsRE.match(conditions)
            if not (match):
                all_good = False
                self.conditionsEntry.delete(0, END)
                self.error_message1.config(text = "Incorrect conditions format")

        # Check if num_k is filled out. If not, display an error message.
        if num_k== "":
            self.neighborsEntry.delete(0, END)
            self.neighbors_error_message.config(text = "Must be an integer")
            all_good = False

        # Check if num_k is an int. If not, display an error message.
        else:
            for i in num_k:
                if i.isdigit() == False:
                    self.neighborsEntry.delete(0, END)
                    self.neighbors_error_message.config(text = "Must be an integer")
                    all_good = False
                    break

        # Check if n_num is filled out. If not, display an error message.
        if n_num == "":
            self.importanceEntry.delete(0, END)
            self.importance_error_message.config(text = "Must be an interger")
            all_good = False

        # Check if n_num is an int. If not, display an error message.
        else:
            for i in n_num:
                if i.isdigit() == False:
                    self.importanceEntry.delete(0, END)
                    self.importance_error_message.config(
                        text = "Must be an interger")
                    all_good = False
                    break

        # Check if the user correctly input the feature selection fractions.
        if fraction1 and fraction2:
            for i in fraction1:
                if not i.isdigit():
                    self.fraction1_entry.delete(0, END)
                    all_good = False
            for i in fraction2:
                if not i.isdigit():
                    self.fraction2_entry.delete(0, END)
                    all_good = False
        else:
            all_good = False

        # Check if extension ends in .csv. If not, display an error message.
        if extension[- 4:] != ".csv":
            all_good = False
            self.extensionEntry.delete(0, END)
            self.error_message2.config(text = "Extension must end in .csv")

        # If one or more entries are wrong, then display an erorr message and
        # return False.
        if all_good == False:
            tkMessageBox.showerror("Invalid Entry",
             "One or more entry is incorrect.")
            return False

        # If all the entries are correct, then return True.
        else:
            return True


################################################################################

#5th Window: Browse for datafiles

################################################################################

class window5(Frame):
    def __init__(self, master):
        """Intitialize Frame"""
        Frame.__init__(self, master, background = "gray90")
        self.master = master
        self.grid()
        self.sensor_display = []
        self.create_window5_widgets()

        # Data Filename Format Is STRICT
        # [/OptionalDirectories/][Subject#]_[Sensor]_All_Data.csv

        # Data Filename Regular Expression
        # Checks the format of data filenames and provides ability to extract
        # the crucial information of the directory, subject number, and sensor
        # type. Checks for one or no '/', then any number of a group of at least
        # one alphanumeric or whitespace character followed by a '/', then at
        # least one digit, followed by an underscore '_', then either 'fNIRS',
        # 'EEG', 'Respiration', 'ECG', or 'EDA' in any case, followed by an
        # underscore '_', then 'All' in any case, followed by an underscore '_',
        # then 'Data' in any case, finished with '.csv'.
        self.filenameRE = re.compile('(?P<directory>/?([\w\s]+/)*)(?P<subject>\d+)_(?P<sensor>(fNIRS|EEG|Respiration|ECG|EDA))_All_Data\.csv$', re.IGNORECASE)

        self.fNIRS_Subjects = []
        self.EEG_Subjects = []
        self.Respiration_Subjects = []
        self.ECG_Subjects = []
        self.EDA_Subjects = []

# Create Window 5's widgets
    def create_window5_widgets(self):

        # Header & Instructions
        self.header = Label(self,
                            text = """Data Files Selection""",
                            background = "gray90", font = "Arial 15 underline")
        self.header.grid(row = 0,column = 0, columnspan = 7, sticky = W)

        self.instructions = Label(self,
                            text = "    Select where the data and condition files are located (on local computer or server),\
 and which files you want to run machine learning on.\
 All the sensors must have data files for each of the subjects.\
 There must be at least two subjects.",
                            background = "gray90", font = "Arial 14",
                            justify = "left", wraplength = "550")
        self.instructions.grid(row = 1, column = 0,
            rowspan = 2, columnspan = 26, sticky = W)

        # Line Break
        self.break00 = Label(self, background = "gray90")
        self.break00.grid(row = 3, column = 0)

        # Datafile Selection Options (local or URL)        
        self.local = BooleanVar() # True = local, false = server
        self.local.set(False) # server is default

        # Server Radiobutton and Label
        self.URL_button = Radiobutton(self, variable = self.local, command = self.URL_cmd, background = "gray90", value = False)
        self.URL_button.grid(row = 4, column = 1, sticky = W)
        self.URL_Header= Label(self,text = "Server (Run on files saved on server)\
\nPlease provide a URL for the server.",
                               background = "gray90", font = "Arial 14", justify = "left")
        self.URL_Header.grid(row = 4, column = 2, sticky = W, rowspan = 2, columnspan = 21)

        # Server Entry
        self.URL_Entry = Entry(self, justify = "right", width = 40)
        self.URL_Entry.grid(row = 6, column = 2, sticky = W, columnspan = 20)

        # Line Break
        self.break0 = Label(self, background = "gray90")
        self.break0.grid(row = 7, column = 0)

        # Local Radiobutton and Label
        self.local_button = Radiobutton(self, variable = self.local, command = self.local_cmd, background = "gray90", value = True)
        self.local_button.grid(row = 8, column = 1, sticky = W)
        self.local_Header= Label(self, text = "Local (Run on files saved on local computer)\
\nAll files must be in the same directory as this program.",
                                 background = "gray90", font = "Arial 14", justify = "left")
        self.local_Header.grid(row = 8, column = 2, sticky = W, rowspan = 2, columnspan = 21)

        # Create the widgets for selecting local files but disable them. Only enable them when self.local is True.
        self.selection_widgets = [] # list for keeping track of what widgets to disable.
        
        # If fNIRS is selected,
        # then create widgets to select fNIRS data files
        if "fNIRS" in selected_sensors:

            # Header
            self.fNIRS_display_label = Label(self, text = "fNIRS Files",
                background = "gray90", font = "Arial 14 bold", state = DISABLED)
            self.fNIRS_display_label.grid(row = 10, column = 2,
                columnspan = 10, sticky = W)
            self.selection_widgets.append(self.fNIRS_display_label)

            # Scrollbars and Display
            self.fNIRS_yscrollbar = Scrollbar(self)
            self.fNIRS_yscrollbar.grid(row = 11, rowspan = 5, column = 17,
                sticky = NS)
            self.fNIRS_xscrollbar = Scrollbar(self, orient = HORIZONTAL)
            self.fNIRS_xscrollbar.grid(row = 16, column = 2, columnspan = 15,
                sticky = EW)

            self.fNIRS_display = Listbox(self, height = 4, width = 35,
                background = "gray90", selectmode=EXTENDED,
                yscrollcommand=self.fNIRS_yscrollbar.set,
                xscrollcommand=self.fNIRS_xscrollbar.set, state = DISABLED)
            self.fNIRS_display.grid(row = 11, rowspan = 5, column = 2,
                columnspan = 15, sticky = W)
            self.sensor_display.append(self.fNIRS_display)
            self.selection_widgets.append(self.fNIRS_display)

            self.fNIRS_yscrollbar.config(command=self.fNIRS_display.yview)
            self.fNIRS_xscrollbar.config(command=self.fNIRS_display.xview)

            # Browse and Delete Button
            self.fNIRS_browse = Button(self, text = "Add data file",
                command = self.fNIRS_browse, font = "Arial 14", state = DISABLED)
            self.fNIRS_browse.grid(row = 11, column = 18)
            self.fNIRS_delete = Button(self, text = "Remove file",
                command = self.fNIRS_remove, font = "Arial 14", state = DISABLED)
            self.fNIRS_delete.grid(row = 12, column = 18)
            self.selection_widgets.append(self.fNIRS_browse)
            self.selection_widgets.append(self.fNIRS_delete)

##            # Line Break
##            self.break1 = Label(self, background = "gray90")
##            self.break1.grid(row = 17, column = 0)

        # If EEG is selected,
        # then create widgets to select EEg data files
        if "EEG" in selected_sensors:

            # Header
            self.EEG_display_label = Label(self, text = "EEG Files",
                background = "gray90", font = "Arial 14 bold", state = DISABLED)
            self.EEG_display_label.grid(row = 18, column = 2,
                columnspan = 4, sticky = W)
            self.selection_widgets.append(self.EEG_display_label)

            # Scrollbar and Display
            self.EEG_yscrollbar = Scrollbar(self)
            self.EEG_yscrollbar.grid(row = 19, rowspan = 5, column = 17,
                sticky = NS)
            self.EEG_xscrollbar = Scrollbar(self, orient = HORIZONTAL)
            self.EEG_xscrollbar.grid(row = 24, column = 2, columnspan = 15,
                sticky = EW)

            self.EEG_display = Listbox(self, height = 4, width = 35,
                background = "gray90", selectmode=EXTENDED,
                yscrollcommand=self.EEG_yscrollbar.set,
                xscrollcommand=self.EEG_xscrollbar.set, state = DISABLED)
            self.EEG_display.grid(row =19, rowspan = 5, column = 2,
                columnspan = 15, sticky = W)
            self.sensor_display.append(self.EEG_display)
            self.selection_widgets.append(self.EEG_display)

            self.EEG_yscrollbar.config(command=self.EEG_display.yview)
            self.EEG_xscrollbar.config(command=self.EEG_display.xview)

            # Browse and Delete Buttons
            self.EEG_browse = Button(self, text = "Add data file",
                command = self.EEG_browse, font = "Arial 14", state = DISABLED)
            self.EEG_browse.grid(row = 19, column = 18)
            self.EEG_delete = Button(self, text = "Remove file",
                command = self.EEG_remove, font = "Arial 14", state = DISABLED)
            self.EEG_delete.grid(row = 20, column = 18)
            self.selection_widgets.append(self.EEG_browse)
            self.selection_widgets.append(self.EEG_delete)

##            # Line Break
##            self.break2 = Label(self, background = "gray90")
##            self.break2.grid(row = 25, column = 0)

        # If Respiration is selected,
        # then create widgets to select Respiration data files
        if "Respiration" in selected_sensors:

            # Header
            self.Respiration_display_label = Label(self,
                text = "Respiration Files", background = "gray90",
                font = "Arial 14 bold", state = DISABLED)
            self.Respiration_display_label.grid(row = 26, column = 2,
                columnspan = 5, sticky = W)
            self.selection_widgets.append(self.Respiration_display_label)

            # Scrollbar and Display
            self.Respiration_yscrollbar = Scrollbar(self)
            self.Respiration_yscrollbar.grid(row = 27, rowspan = 5, column = 17,
                sticky = NS)
            self.Respiration_xscrollbar = Scrollbar(self, orient = HORIZONTAL)
            self.Respiration_xscrollbar.grid(row = 32, column = 2,
                columnspan = 15, sticky = EW)

            self.Respiration_display = Listbox(self, height = 4, width = 35,
                background = "gray90", selectmode=EXTENDED,
                yscrollcommand=self.Respiration_yscrollbar.set,
                xscrollcommand= self.Respiration_xscrollbar.set, state = DISABLED)
            self.Respiration_display.grid(row =27, rowspan = 5, column = 2,
                columnspan = 15, sticky = W)
            self.sensor_display.append(self.Respiration_display)
            self.selection_widgets.append(self.Respiration_display)

            self.Respiration_yscrollbar.config(
                command=self.Respiration_display.yview)
            self.Respiration_xscrollbar.config(
                command=self.Respiration_display.xview)

            # Browse and Delete Buttons
            self.Respiration_browse = Button(self, text = "Add data file",
                command = self.Respiration_browse, font = "Arial 14", state = DISABLED)
            self.Respiration_browse.grid(row = 27, column = 18)
            self.Respiration_delete = Button(self, text = "Remove file",
                command = self.Respiration_remove, font = "Arial 14", state = DISABLED)
            self.Respiration_delete.grid(row = 28, column = 18)
            self.selection_widgets.append(self.Respiration_browse)
            self.selection_widgets.append(self.Respiration_delete)


##            #Line Break
##            self.break3 = Label(self, background = "gray90")
##            self.break3.grid(row = 33, column = 0)

        # If ECG is selected,
        # then create widgets to select ECG data files
        if "ECG" in selected_sensors:

            # Header
            self.ECG_display_label = Label(self, text = "ECG Files",
                background = "gray90", font = "Arial 14 bold", state = DISABLED)
            self.ECG_display_label.grid(row = 34, column = 2, columnspan = 4,
                sticky = W)
            self.selection_widgets.append(self.ECG_display_label)

            # Scrollbar and Display
            self.ECG_yscrollbar = Scrollbar(self)
            self.ECG_yscrollbar.grid(row = 35, rowspan = 5, column = 17,
                sticky = NS)
            self.ECG_xscrollbar = Scrollbar(self, orient = HORIZONTAL)
            self.ECG_xscrollbar.grid(row = 40, column = 2, columnspan = 15,
                sticky = EW)

            self.ECG_display = Listbox(self, height = 4, width = 35,
                background = "gray90", selectmode=EXTENDED,
                yscrollcommand=self.ECG_yscrollbar.set,
                xscrollcommand=self.ECG_xscrollbar.set, state = DISABLED)
            self.ECG_display.grid(row =35, rowspan = 5, column = 2,
                columnspan = 15, sticky = W)
            self.sensor_display.append(self.ECG_display)
            self.selection_widgets.append(self.ECG_display)
            
            self.ECG_yscrollbar.config(command=self.ECG_display.yview)
            self.ECG_xscrollbar.config(command=self.ECG_display.xview)

            # Browse and Delete Button
            self.ECG_browse = Button(self, text = "Add data file",
                command = self.ECG_browse, font = "Arial 14", state = DISABLED)
            self.ECG_browse.grid(row = 35, column = 18)
            self.ECG_delete = Button(self, text = "Remove file",
                command = self.ECG_remove, font = "Arial 14", state = DISABLED)
            self.ECG_delete.grid(row = 36, column = 18)
            self.selection_widgets.append(self.ECG_browse)
            self.selection_widgets.append(self.ECG_delete)

##            #Line Break
##            self.break4 = Label(self, background = "gray90")
##            self.break4.grid(row = 41, column = 0)

        # If EDA is selected,
        # then create widgets to select EDA data files
        if "EDA" in selected_sensors:

            # Header
            self.EDA_display_label = Label(self, text = "EDA Files",
                background = "gray90", font = "Arial 14 bold", state = DISABLED)
            self.EDA_display_label.grid(row = 42, column = 2, columnspan = 4,
                sticky = W)
            self.selection_widgets.append(self.EDA_display_label)

            # Scrollbar and Display
            self.EDA_yscrollbar = Scrollbar(self)
            self.EDA_yscrollbar.grid(row = 43, rowspan = 5, column = 17,
                sticky = NS)
            self.EDA_xscrollbar = Scrollbar(self, orient = HORIZONTAL)
            self.EDA_xscrollbar.grid(row =49, column = 2, columnspan = 15,
                sticky = EW)

            self.EDA_display = Listbox(self, height = 4, width = 35,
                background = "gray90", selectmode=EXTENDED,
                yscrollcommand=self.EDA_yscrollbar.set,
                xscrollcommand=self.EDA_xscrollbar.set, state = DISABLED)
            self.EDA_display.grid(row =43, rowspan = 5, column = 2,
                columnspan = 15, sticky = W)
            self.sensor_display.append(self.EDA_display)
            self.selection_widgets.append(self.EDA_display)
            
            self.EDA_yscrollbar.config(command=self.EDA_display.yview)
            self.EDA_xscrollbar.config(command=self.EDA_display.xview)

            # Browse and Delete Buttons
            self.EDA_browse = Button(self, text = "Add data file",
                command = self.EDA_browse, font = "Arial 14", state = DISABLED)
            self.EDA_browse.grid(row = 43, column = 18)
            self.EDA_delete = Button(self, text = "Remove file",
                command = self.EDA_remove, font = "Arial 14", state = DISABLED)
            self.EDA_delete.grid(row = 44, column = 18)
            self.selection_widgets.append(self.EDA_browse)
            self.selection_widgets.append(self.EDA_delete)

##            # Line Break
##            self.break4 = Label(self, background = "gray90")
##            self.break4.grid(row = 50, column = 0)

        #Back Button (return to window 4)
        self.back_button = Button(self, text = "Back", command = self.back_window4, font = "Arial 14")
        self.back_button.grid(row = 51, column = 1, stick = W)

        #Submit Button (Finish and close the .txt file. Pass the file to )
        self.submit_button = Button(self, text = "Submit", command = self.submit, font = "Arial 14")
        self.submit_button.grid(row = 51, column = 22, sticky = E)

################################################################################
#End of creating Window 5's widgets
################################################################################


# Function for URL Radiobutton
    def URL_cmd(self):
        self.local.set(False)
        self.URL_Entry["state"] = NORMAL
        for widget in self.selection_widgets:
            widget["state"] = DISABLED
           
# Function for local Radiobutton
    def local_cmd(self):
        self.local.set(True)
        self.URL_Entry.delete(0, END)
        self.URL_Entry["state"] = DISABLED
        for widget in self.selection_widgets:
            widget["state"] = NORMAL


# Function for fNIRS Browse Button
# Browse for and add data filename
    def fNIRS_browse(self):
        filenames1 = tkFileDialog.askopenfilename(
            filetypes = [("csv files", "*.csv")], multiple = True,
            title = 'Choose a fNIRS data file')

        filenames = []
        for item in filenames1:
            filenames.append(os.path.basename(item))
        
        #filename = os.path.basename(filename)
        # ^^^This stores only the basename
        # of the files (not the directory). Uncomment if you want this.

        # Check if filename is correct. If it is, add it to the display.
        # If not, display an error message.
        filenameError = False
        if filenames:
            for filename in filenames:
                match = self.filenameRE.match(filename)

                if (match):
                    if (match.group("sensor").lower() == "fnirs"):
                        self.fNIRS_display.insert(END, filename)
                        self.fNIRS_Subjects.append(int(match.group("subject")))
                    else:
                        filenameError = True
                else:
                    filenameError = True

            if (filenameError):
                tkMessageBox.showerror("ERROR",
                    "Please provide appropriate data files.\
\nCorrect Filename Format: \
\n[Subject#]_fNIRS_All_Data.csv")

# Fucntion for fNIRS Remove Button
# Remove selected data filename from display
    def fNIRS_remove(self):
        filename = self.fNIRS_display.get(ANCHOR)

        if (filename):
            match = self.filenameRE.match(filename)
            self.fNIRS_Subjects.remove(int(match.group("subject")))
            self.fNIRS_display.delete(ANCHOR)

# Function for EEG Browse Button
# Browse for and add data filename
    def EEG_browse(self):
        filenames1 = tkFileDialog.askopenfilename(
            filetypes = [("csv files", "*.csv")], multiple = True,
            title = 'Choose a EEG data file')
        
        filenames = []
        for item in filenames1:
            filenames.append(os.path.basename(item))
        # ^^^This stores only the basename
        # of the files (not the directory). Uncomment if you want this.

        # Check if filename is correct. If it is, add it to the display.
        # If not, display an error message.
        filenameError = False
        if filenames:
            for filename in filenames:
                match = self.filenameRE.match(filename)

                if (match):
                    if (match.group("sensor").lower() == "eeg"):
                        self.EEG_display.insert(END, filename)
                        self.EEG_Subjects.append(int(match.group("subject")))
                    else:
                        filenameError = True
                else:
                    filenameError = True

            if (filenameError):
                tkMessageBox.showerror("ERROR",
                    "Please provide appropriate data files.\
\nCorrect Filename Format: \
\n[Subject#]_EEG_All_Data.csv")

# Function for ECG Remove Button
# Remove the selected data filename from the display
    def EEG_remove(self):
        filename = self.EEG_display.get(ANCHOR)

        if (filename):
            match = self.filenameRE.match(filename)
            self.EEG_Subjects.remove(int(match.group("subject")))
            self.EEG_display.delete(ANCHOR)

# Function for the Resipration Browse Button
# Browse for and add data filename
    def Respiration_browse(self):
        filenames1 = tkFileDialog.askopenfilename(
            filetypes = [("csv files", "*.csv")], multiple = True,
            title = 'Choose a Respiration data file')
        
        filenames = []
        for item in filenames1:
            filenames.append(os.path.basename(item))
        # ^^^This stores only the basename
        # of the files (not the directory). Uncomment if you want this.

        # Check if filename is correct. If it is, add it to the display.
        # If not, display an error message.
        filenameError = False
        if filenames:
            for filename in filenames:
                match = self.filenameRE.match(filename)

                if (match):
                    if (match.group("sensor").lower() == "respiration"):
                        self.Respiration_display.insert(END, filename)
                        self.Respiration_Subjects.append(
                            int(match.group("subject")))
                    else:
                        filenameError = True
                else:
                    filenameError = True

            if (filenameError):
                tkMessageBox.showerror("ERROR",
                    "Please provide appropriate data files.\
\nCorrect Filename Format: \
\n[Subject#]_Respiration_All_Data.csv")

# Function for Respiration Remove Button
# Remove selected data filename from the display
    def Respiration_remove(self):
        filename = self.Respiration_display.get(ANCHOR)

        if (filename):
            match = self.filenameRE.match(filename)
            self.Respiration_Subjects.remove(int(match.group("subject")))
            self.Respiration_display.delete(ANCHOR)

# Function for ECG Browse Button
# Browse for and add data filename
    def ECG_browse(self):
        filenames1 = tkFileDialog.askopenfilename(
            filetypes = [("csv files", "*.csv")], multiple = True,
            title = 'Choose a ECG data file')

        filenames = []
        for item in filenames1:
            filenames.append(os.path.basename(item))
        # ^^^This stores only the basename
        # of the files (not the directory). Uncomment if you want this.

        # Check if filename is correct. If it is, add it to the display.
        # If not, display an error message.
        filenameError = False
        if filenames:
            for filename in filenames:
                match = self.filenameRE.match(filename)

                if (match):
                    if (match.group("sensor").lower() == "ecg"):
                        self.ECG_display.insert(END, filename)
                        self.ECG_Subjects.append(int(match.group("subject")))
                    else:
                        filenameError = True
                else:
                    filenameError = True

            if (filenameError):
                tkMessageBox.showerror("ERROR",
                    "Please provide appropriate data files.\
                    \nCorrect Filename Format: \
                    \n[Subject#]_ECG_All_Data.csv")

# Function for ECG Remove Button
# Remove selected data filename from the display
    def ECG_remove(self):
        filename = self.ECG_display.get(ANCHOR)

        if (filename):
            match = self.filenameRE.match(filename)
            self.ECG_Subjects.remove(int(match.group("subject")))
            self.ECG_display.delete(ANCHOR)

# Function for EDA Browse Button
# Browse for and add data filename
    def EDA_browse(self):
        filenames1 = tkFileDialog.askopenfilename(
            filetypes = [("csv files", "*.csv")], multiple = True,
            title = 'Choose a EDA data file')

        filenames = []
        for item in filenames1:
            filenames.append(os.path.basename(item))
        # ^^^This stores only the basename
        # of the files (not the directory). Uncomment if you want this.

        # Check if filename is correct. If it is, add it to the display.
        # If not, display an error message.
        filenameError = False
        if filenames:
            for filename in filenames:
                match = self.filenameRE.match(filename)

                if (match):
                    if (match.group("sensor").lower() == "eda"):
                        self.EDA_display.insert(END, filename)
                        self.EDA_Subjects.append(int(match.group("subject")))
                    else:
                        filenameError = True
                else:
                    filenameError = True

            if (filenameError):
                tkMessageBox.showerror("ERROR",
                    "Please provide appropriate data files.\
\nCorrect Filename Format: \
\n[Subject#]_EDA_All_Data.csv")

# Function for EDA Remove Button
# Remove selected data filename from display
    def EDA_remove(self):
        filename = self.EDA_display.get(ANCHOR)

        if (filename):
            match = self.filenameRE.match(filename)
            self.EDA_Subjects.remove(int(match.group("subject")))
            self.EDA_display.delete(ANCHOR)

# Function for Back Button
# Return to Window 4
    def back_window4(self):

        # Remove last 14 entries of output (13 added from window 4) to reset
        # for new selected output from user
        for i in range(13):
            output.pop()

        # Show Window 4 and delete Window 5.
        self.master.show_frame(window4)
        self.master.close_frame(window5)

# Function for Submit Button
# Check if a URL was given (server) or if the correct number of datafiles was selected (local).
# If it was, then close the UI and run proj.py.
    def submit(self):

        # If Local was selected, then check the number of datafiles provided.
        if self.local.get() == True:
            # Error Checking
            SensorSets = []
            Difference = []

            # Check if there is at least 2 data files for a selected sensor.
            # If not, then display an error message.
            SensorDisplayList = []

            if ("fNIRS" in selected_sensors):
                SensorDisplayList.append(self.fNIRS_display)
            if ("EEG" in selected_sensors):
                SensorDisplayList.append(self.EEG_display)
            if ("Respiration" in selected_sensors):
                SensorDisplayList.append(self.Respiration_display)
            if ("ECG" in selected_sensors):
                SensorDisplayList.append(self.ECG_display)
            if ("EDA" in selected_sensors):
                SensorDisplayList.append(self.EDA_display)

            for l in SensorDisplayList:
                if (l.size() < 2):
                    tkMessageBox.showerror("ERROR",
                        "Each sensor must have at least 2 data files.")
                    return

            # If there is more than one sensor selected, must check there are the
            # same number of data files for each sensor selected and, in addition,
            # the data files for each sensor must be for the same subject.
            if (len(selected_sensors) > 1):

                # Make each list of sensor subjects into a set and append them
                # to a list
                if ("fNIRS" in selected_sensors):
                    SensorSets.append(set(self.fNIRS_Subjects))
                if ("EEG" in selected_sensors):
                    SensorSets.append(set(self.EEG_Subjects))
                if ("Respiration" in selected_sensors):
                    SensorSets.append(set(self.Respiration_Subjects))
                if ("ECG" in selected_sensors):
                    SensorSets.append(set(self.ECG_Subjects))
                if ("EDA" in selected_sensors):
                    SensorSets.append(set(self.EDA_Subjects))

                # Extracts the differences of all the Sensor Sets if there are any
                for i in range(len(SensorSets)):

                    # Check the first Subject List with each other individual
                    # subject lists (instead of them all together at once which
                    # is not what we want)
                    for i in range(len(SensorSets) - 1):
                        Difference += list(
                            SensorSets[0].difference(SensorSets[i + 1]))

                    # Reorder SensorSets list to check from the perspective
                    # of each sensor
                    item = SensorSets.pop(0)
                    SensorSets.append(item)

                # Convert into set and back into a list and then sort the list
                # to remove duplicates and then have the subject numbers sorted
                DifferenceSet = set(Difference)
                Difference = list(DifferenceSet)
                Difference.sort()
                Missing_Subjects = ''

                for missing_subject in Difference:
                    Missing_Subjects += (str(missing_subject) + ", ")
                Missing_Subjects = Missing_Subjects[:-2]
                # If there are any differences, there is clearly an error

                if (len(Difference) > 0):
                    tkMessageBox.showerror("ERROR",
                        "Missing matching sensor data files for subjects " +
                        Missing_Subjects)
                    return
        if self.local.get() == False:
            if not self.URL_Entry.get():
                tkMessageBox.showerror("ERROR", "Missing URL link")
                return

        if (tkMessageBox.askokcancel("Confirm",
            "Click OK to close this user interface and start running \
the program.")):

            # Add appropriate output
            output_filenames.append("Data Files")

            if self.local.get() == True:
                output.append("\n" + "Local = True")
                output.append("\n" + "URL = " + self.URL_Entry.get())
                # If fNIRS is selected, get the names of the selected files and
                # add them to a string
                if "fNIRS" in selected_sensors:
                    fNIRS_string = ''

                    # Get every filename in the listbox
                    # (listbox.get() function returns a list of the items)
                    fNIRS_list = self.fNIRS_display.get(0, END)

                    # Append every filename in the list to the output string
                    # as well as a comma and space
                    for fNIRS_file in fNIRS_list:
                        fNIRS_string += ("\n" + fNIRS_file)

                    # Finally add the completed string to output list
                    output_filenames.append(fNIRS_string)

                # If EEG is selected, get the names of the selected files and
                # add them to a string.
                if "EEG" in selected_sensors:
                    EEG_string = ''

                    # Get every filename in the listbox
                    # (listbox.get() function returns a list of the items)
                    EEG_list = self.EEG_display.get(0, END)

                    # Append every filename in the list to the output string
                    # as well as a comma and space
                    for EEG_file in EEG_list:
                        EEG_string += ("\n" + EEG_file)

                    # Finally add the completed string to output list
                    output_filenames.append(EEG_string)

                # If Respiration is selected, get the names of the selected files
                # and add them to a string.
                if "Respiration" in selected_sensors:
                    Respiration_string = ''

                    # Get every filename in the listbox
                    # (listbox.get() function returns a list of the items)
                    Respiration_list = self.Respiration_display.get(0, END)

                    # Append every filename in the list to the output string
                    # as well as a comma and space
                    for Respiration_file in Respiration_list:
                        Respiration_string += ("\n" + Respiration_file)

                    # Finally add the completed string to output list
                    output_filenames.append(Respiration_string)

                # If ECG is selected, get the names of the selected files and
                # add them to a string.
                if "ECG" in selected_sensors:
                    ECG_string = ''

                    # Get every filename in the listbox
                    # (listbox.get() function returns a list of the items)
                    ECG_list = self.ECG_display.get(0, END)

                    # Append every filename in the list to the output string
                    # as well as a comma and space.
                    for ECG_file in ECG_list:
                        ECG_string += ("\n" + ECG_file)

                    # Finally add the completed string to output list.
                    output_filenames.append(ECG_string)

                # If EDA is selected, get the names of the selected files and
                # add them to a string.
                if "EDA" in selected_sensors:
                    EDA_string = ''

                    # Get every filename in the listbox.
                    # (listbox.get() function returns a list of the items)
                    EDA_list = self.EDA_display.get(0, END)

                    # Append every filename in the list to the output string
                    # as well as a comma and space.
                    for EDA_file in EDA_list:
                        EDA_string += ("\n" + EDA_file)

                    # Finally add the completed string to output list.
                    output_filenames.append(EDA_string)

                    
            if self.local.get() == False:
                output_filenames.append("""
DELETE THIS LINE AND WRITE THE FILES YOU WANT TO BE USED IN PROJ.PY CHECK MANUAL FOR FORMAT"""
                                        )
                output.append("\n" + "Local = False")
                output.append("\n" + "URL = " + self.URL_Entry.get())

            # Write contents of output string to text file.
            file = open("parameters.txt", "w")
            for line in output:
                file.write(line)
            file.close()    # Make sure to clean-up and close the file

            # Write contents of output filenames list to test file.
            file = open("data_filenames.txt", "w")
            for line in output_filenames:
                file.write(line)
            file.close()    # Make sure to clean-up and close the file

            # Close the window (graphical interface)
            app.destroy()

            # Run the main project program
            if self.local.get() == True:
                proj.main()

#================================== MAIN ======================================#

app = Application()

# This code prompts user to make sure if they want to quit the program and,
# if so, makes sure to clean-up and close the file the program writes to.
def on_closing():

    if tkMessageBox.askokcancel("Quit", "Are you sure you want to cancel and quit?"):
        # Clost the window (graphical interface)
        app.destroy()

app.protocol("WM_DELETE_WINDOW", on_closing)

# Run the GUI Interface program
app.mainloop()
