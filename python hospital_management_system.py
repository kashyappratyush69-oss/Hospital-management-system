import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime

# ==================== DATABASE SETUP ====================
conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    disease TEXT,
    admission_date TEXT,
    bill REAL
)
""")
conn.commit()

# ==================== FUNCTIONS ====================
def add_patient():
    name = entry_name.get()
    age = entry_age.get()
    gender = gender_var.get()
    disease = entry_disease.get()
    bill = entry_bill.get()
    date = datetime.now().strftime("%Y-%m-%d")

    if not name or not age or not gender or not disease or not bill:
        messagebox.showerror("Error", "Please fill all fields!")
        return

    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO patients (name, age, gender, disease, admission_date, bill) VALUES (?, ?, ?, ?, ?, ?)",
                   (name, age, gender, disease, date, bill))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", f"Patient added successfully!\nDate: {date}\nBill: ₹{bill}")
    clear_entries()
    display_patients()

def delete_patient():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a patient to delete!")
        return
    patient_id = tree.item(selected)["values"][0]

    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE id=?", (patient_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Deleted", "Patient record deleted successfully!")
    display_patients()

def display_patients():
    for row in tree.get_children():
        tree.delete(row)
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    for patient in cursor.fetchall():
        tree.insert("", END, values=patient)
    conn.close()

def clear_entries():
    entry_name.delete(0, END)
    entry_age.delete(0, END)
    gender_var.set("")
    entry_disease.delete(0, END)
    entry_bill.delete(0, END)

# ==================== GUI SETUP ====================
root = Tk()
root.title("🏥 Hospital Management System")
root.geometry("950x600")
root.configure(bg="#f8f9fa")

title_label = Label(root, text="🏥 Hospital Management System", bg="#007BFF", fg="white",
                    font=("Arial", 18, "bold"), pady=10)
title_label.pack(fill=X)

form_frame = Frame(root, bg="#f8f9fa")
form_frame.pack(pady=20)

label_style = {"bg": "#f8f9fa", "font": ("Arial", 12, "bold")}
entry_style = {"font": ("Arial", 11)}

Label(form_frame, text="Name:", **label_style).grid(row=0, column=0, padx=10, pady=5, sticky=E)
entry_name = Entry(form_frame, **entry_style)
entry_name.grid(row=0, column=1, padx=10, pady=5)

Label(form_frame, text="Age:", **label_style).grid(row=1, column=0, padx=10, pady=5, sticky=E)
entry_age = Entry(form_frame, **entry_style)
entry_age.grid(row=1, column=1, padx=10, pady=5)

Label(form_frame, text="Gender:", **label_style).grid(row=2, column=0, padx=10, pady=5, sticky=E)
gender_var = StringVar()
OptionMenu(form_frame, gender_var, "Male", "Female", "Other").grid(row=2, column=1, padx=10, pady=5, sticky=W)

Label(form_frame, text="Disease:", **label_style).grid(row=3, column=0, padx=10, pady=5, sticky=E)
entry_disease = Entry(form_frame, **entry_style)
entry_disease.grid(row=3, column=1, padx=10, pady=5)

Label(form_frame, text="Bill Amount (₹):", **label_style).grid(row=4, column=0, padx=10, pady=5, sticky=E)
entry_bill = Entry(form_frame, **entry_style)
entry_bill.grid(row=4, column=1, padx=10, pady=5)

btn_style = {"font": ("Arial", 11, "bold"), "width": 15, "pady": 5}

Button(form_frame, text="Add Patient", command=add_patient, bg="#28a745", fg="white", **btn_style).grid(row=5, column=0, pady=10)
Button(form_frame, text="Delete Patient", command=delete_patient, bg="#dc3545", fg="white", **btn_style).grid(row=5, column=1, pady=10)

# ==================== TABLE ====================
tree_frame = Frame(root)
tree_frame.pack(pady=20)

columns = ("ID", "Name", "Age", "Gender", "Disease", "Admission Date", "Bill (₹)")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor=CENTER, width=120)
tree.pack()

display_patients()

root.mainloop()
