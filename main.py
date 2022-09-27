from backend.utils.globals import *
from frontend.gui import GUI
import tkinter as tk


def main():
    root=tk.Tk()
    root.geometry(f"{X_SIZE}x{Y_SIZE}")
    root.configure(background=BACKGROUND_COLOR)
    root.title("Preferans solver")
    gui=GUI(root)
    gui.draw()
    root.mainloop()

if __name__=="__main__":
    main()