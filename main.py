import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox as msgbox

class FileOrganizer:
    def __init__(self, master=tk.Tk):
        #Set up the window
        self.master = master
        self.master.title("File Organizer")
        self.master.geometry("1080x720+420+180")
        self.master.iconbitmap("icon.ico")
        #Create the widgets
        self.create_widgets()
        #Credits
        print("Made by pancracium @ github (https://www.github.com/pancracium)")
    
    def create_widgets(self):
        """Create the widgets."""
        #Entry for the name of the folder where the files will be organized
        self.folder_label = ttk.Label(self.master, text="Folder name:")
        self.folder_entry = ttk.Entry(self.master, width=50)
        self.folder_button = ttk.Button(self.master, text="Select folder", command=self.get_folder)
        #Button for creating rows for new file types
        self.row_frames = []
        self.create_row_frame()
        self.add_row_button = ttk.Button(self.master, text="Add Row", command=self.create_row_frame)
        #Button for actually organizing the files
        self.organize_button = ttk.Button(self.master, text="Organize", command=self.organize_files)
        #Place the widgets
        self.folder_label.place(relx=0.1, rely=0.02, anchor=tk.CENTER)
        self.folder_button.place(relx=0.5, rely=0.02, anchor=tk.CENTER)
        self.folder_entry.grid(row=0, column=1, padx=5, pady=5)
        self.add_row_button.place(relx=0.6, rely=0.02, anchor=tk.CENTER)
        self.organize_button.place(relx=0.7, rely=0.02, anchor=tk.CENTER)
    
    def get_folder(self):
        """Prompt the user for a folder."""
        folder_name = filedialog.askdirectory(
            initialdir="~/Desktop",
            title="Select folder"
        )
        self.folder_entry.delete(0, tk.END)
        self.folder_entry.insert(0, folder_name)

    def create_row_frame(self):
        """Create a new row for another file type."""
        #Check if there are too many rows
        if len(self.row_frames) > 16:
            msgbox.showerror(title="Error", message="Too many rows! Maximum is 17.")
            return "TooManyRows"
        #Create a frame for the rows
        row_frame = ttk.Frame(self.master)
        #Create each row's widgets
        extension_label = ttk.Label(row_frame, text="Extension:")
        extension_entry = ttk.Entry(row_frame)
        folder_label = ttk.Label(row_frame, text="Folder Name:")
        folder_entry = ttk.Entry(row_frame)
        exception_label = ttk.Label(row_frame, text="Exceptions:")
        exception_entry = ttk.Entry(row_frame)
        #Place the widgets
        extension_label.grid(row=0, column=0, padx=5, pady=5)
        extension_entry.grid(row=0, column=1, padx=5, pady=5)
        folder_label.grid(row=0, column=2, padx=5, pady=5)
        folder_entry.grid(row=0, column=3, padx=5, pady=5)
        exception_label.grid(row=0, column=4, padx=5, pady=5)
        exception_entry.grid(row=0, column=5, padx=5, pady=5)
        row_frame.grid(row=len(self.row_frames)+3, column=1, padx=5, pady=5)
        self.row_frames.append((extension_entry, folder_entry, exception_entry))

    def organize_files(self):
        """Organize the files."""
        #Get the folder's name
        folder_name = self.folder_entry.get()
        if not folder_name:
                msgbox.showerror(title="Error", message="Please provide a folder name!")
                return "NoFolderName"
        #Create a folder if it does not exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        #Get every widget's entry
        for extension_entry, folder_entry, exception_entry in self.row_frames:
            extension = extension_entry.get()
            folder = folder_entry.get()
            exceptions = exception_entry.get().split(',')
            #Check for errors
            if not extension:
                msgbox.showerror(title="Error", message="Please provide an extension for the files!")
                return "NoExtension"
            if not extension.startswith("."):
                extension = "." + extension
            if not folder:
                msgbox.showerror(title="Error", message="Please provide a name for the new folder where the files will be!")
                return "NoFolderNames"
            exceptions_list = [exceptions]
            for separator in [", ", " ,", " , "]:
                if not any(exceptions_list):
                    exceptions_list = exceptions.split(separator)
            exceptions = exceptions_list[0] if exceptions_list[0] else None
            #Create a folder if it does not exist
            if not os.path.exists(os.path.join(folder_name, folder)):
                os.makedirs(os.path.join(folder_name, folder))
            #Move files to their folder
            for file in os.listdir(folder_name):
                if file.endswith(extension) and file not in exceptions:
                    shutil.move(os.path.join(folder_name, file), os.path.join(folder_name, folder, file))
                    msgbox.showinfo(title="Success!", message="The files were succesfully organized!")
                    return "Success"

#Create a window for the app
root = tk.Tk()
app = FileOrganizer(master=root)
app.master.mainloop()