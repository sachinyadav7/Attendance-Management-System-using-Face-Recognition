import pandas as pd
from glob import glob
import os
import tkinter as tk
import csv
from tkinter import *
import tkinter.messagebox as messagebox

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get().strip()  # Strip whitespace from input
        
        if not Subject:
            t = 'Please enter the subject name.'
            text_to_speech(t)
            messagebox.showerror("Error", t)
            return

        # Path for the subject's attendance folder
        subject_path = os.path.join("Attendance", Subject)

        if not os.path.exists(subject_path):
            t = f"The folder for subject '{Subject}' does not exist."
            text_to_speech(t)
            messagebox.showerror("Error", t)
            return

        # Look for CSV files in the folder
        filenames = glob(os.path.join(subject_path, f"{Subject}*.csv"))
        
        if not filenames:
            t = f"No attendance files found for subject '{Subject}'."
            text_to_speech(t)
            messagebox.showerror("Error", t)
            return

        # Load and merge CSV files
        df = [pd.read_csv(f) for f in filenames]
        newdf = df[0]
        for i in range(1, len(df)):
            newdf = newdf.merge(df[i], how="outer")
        
        newdf.fillna(0, inplace=True)
        newdf["Attendance"] = 0
        for i in range(len(newdf)):
            newdf["Attendance"].iloc[i] = f"{int(round(newdf.iloc[i, 2:-1].mean() * 100))}%"

        # Save the consolidated attendance data
        consolidated_csv_path = os.path.join(subject_path, "attendance.csv")
        newdf.to_csv(consolidated_csv_path, index=False)

        # Display attendance in a new Tkinter window
        root = tk.Tk()
        root.title("Attendance of " + Subject)
        root.configure(background="black")

        with open(consolidated_csv_path) as file:
            reader = csv.reader(file)
            r = 0
            for col in reader:
                c = 0
                for row in col:
                    label = tk.Label(
                        root,
                        width=15,
                        height=1,
                        fg="yellow",
                        font=("times", 15, " bold "),
                        bg="black",
                        text=row,
                        relief=tk.RIDGE,
                    )
                    label.grid(row=r, column=c)
                    c += 1
                r += 1
        
        root.mainloop()
        print(newdf)

    def Attf():
        sub = tx.get().strip()
        if not sub:
            t = "Please enter the subject name!!!"
            text_to_speech(t)
            messagebox.showerror("Error", t)
        else:
            subject_path = os.path.join("Attendance", sub)
            if not os.path.exists(subject_path):
                t = f"The folder for subject '{sub}' does not exist."
                text_to_speech(t)
                messagebox.showerror("Error", t)
            else:
                os.startfile(subject_path)

    # Main Tkinter window for subject selection
    subject = Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")

    titl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)
    
    titl = tk.Label(
        subject,
        text="Which Subject of Attendance?",
        bg="black",
        fg="green",
        font=("arial", 25),
    )
    titl.place(x=100, y=12)

    sub = tk.Label(
        subject,
        text="Enter Subject",
        width=10,
        height=2,
        bg="black",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("times new roman", 15),
    )
    sub.place(x=50, y=100)

    tx = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="black",
        fg="yellow",
        relief=RIDGE,
        font=("times", 30, "bold"),
    )
    tx.place(x=190, y=100)

    fill_a = tk.Button(
        subject,
        text="View Attendance",
        command=calculate_attendance,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=12,
        relief=RIDGE,
    )
    fill_a.place(x=195, y=170)

    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=10,
        relief=RIDGE,
    )
    attf.place(x=360, y=170)

    subject.mainloop()
