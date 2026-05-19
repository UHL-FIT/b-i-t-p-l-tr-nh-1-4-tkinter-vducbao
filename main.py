import tkinter as tk
from model import StudentModel
from view import StudentView
from controller import StudentController

if __name__ == "__main__":
    root = tk.Tk()
    
    model = StudentModel()
    view = StudentView(root)
    controller = StudentController(model, view)
    
    root.mainloop()