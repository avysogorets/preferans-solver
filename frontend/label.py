import tkinter as tk
import tkinter.font as tkf
from backend.utils.globals import MESSAGE_FONT

def Label(parent,**kwargs):
    if 'font' not in kwargs:
        kwargs['font']=tkf.Font(family="Garamond",size=MESSAGE_FONT)
    kwargs['bd']=0
    return tk.Label(parent,**kwargs)