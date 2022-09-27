import platform
import tkinter as tk
import tkinter.font as tkf
from backend.utils.globals import MESSAGE_FONT

def Button(parent,**kwargs):
    if 'disabledbackground'not in kwargs:
        kwargs['disabledbackground']='grey80'
    if 'highlightthickness' not in kwargs:
        kwargs['highlightthickness']=0
    if platform.system()=='Darwin':
        from tkmacosx import Button as MacButton
        if 'font' not in kwargs:
            kwargs['font']=tkf.Font(family="Garamond",size=int(MESSAGE_FONT*(3/4)))
        if 'borderless' not in kwargs:
            kwargs['borderless']=True
        return MacButton(parent,**kwargs)
    else:
        if 'font' not in kwargs:
            kwargs['font']=tkf.Font(family="Garamond",size=int(MESSAGE_FONT*(3/4)))
        return tk.Button(parent,**kwargs)