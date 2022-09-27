from backend.utils.globals import *
from backend.solver import Solver
from backend.game import Game
from frontend.label import Label
from frontend.button import Button
import tkinter as tk
import tkinter.font as tkf
from PIL import Image,ImageTk
from functools import partial
import numpy as np
import os
    

class GUI:
    def __init__(self,root):
        self.root=root
        self.games=[Game()]
        self.solution=None
        self.current_game=0
        self.equivalence_classes={}
        self.images={}
        images={card.to_string:Image.open(IMG_DIR+f"/{card.to_string}.png") for card in CARDS}
        self.images['normal']={card_key:ImageTk.PhotoImage(img.resize((CARD_X_SIZE,CARD_Y_SIZE),Image.ANTIALIAS)) for card_key,img in images.items()}
        images={card.to_string:Image.open(IMG_DIR_DISABLED+f"/{card.to_string}.png") for card in CARDS}
        self.images['disabled']={card_key:ImageTk.PhotoImage(img.resize((CARD_X_SIZE,CARD_Y_SIZE),Image.ANTIALIAS)) for card_key,img in images.items()}
        images={card.to_string:Image.open(IMG_DIR_OPTIMAL+f"/{card.to_string}.png") for card in CARDS}
        self.images['optimal']={card_key:ImageTk.PhotoImage(img.resize((CARD_X_SIZE,CARD_Y_SIZE),Image.ANTIALIAS)) for card_key,img in images.items()}
        images={filename.split('.')[0]:Image.open(os.path.join(IMG_DIR_UTILS,filename)) for filename in os.listdir(IMG_DIR_UTILS)}
        self.images['utils']={key:ImageTk.PhotoImage(img.resize((int(MESSAGE_FONT*(3/4)),int(MESSAGE_FONT*(3/4))),Image.ANTIALIAS)) for key,img in images.items()}
        self.info_image=ImageTk.PhotoImage(Image.open(IMG_INFO).resize((X_SIZE//30,X_SIZE//30),Image.ANTIALIAS))
        self.phase='deal'

    def random_deal(self):
        cards_to_deal=[card for card in CARDS if card not in self.games[self.current_game].hands[SOUTH].cards and card not in self.games[self.current_game].hands[WEST].cards and card not in self.games[self.current_game].hands[EAST].cards]
        cards_to_deal=np.random.permutation(cards_to_deal)
        for card in cards_to_deal:
            if len(self.games[self.current_game].hands[SOUTH].cards)<10:
                self.action(card=card)
            elif len(self.games[self.current_game].hands[WEST].cards)<10:
                self.action(card=card)
            elif len(self.games[self.current_game].hands[EAST].cards)<10:
                self.action(card=card)

    def draw_players(self):
        frame=tk.Frame(self.root,bg=BACKGROUND_COLOR,bd=0,height=1.4*CARD_Y_SIZE+2*BORDER_THICKNESS,width=9*CARD_STEP_X+CARD_X_SIZE+2*BORDER_THICKNESS)
        frame.place(relx=0.5,rely=0.83,anchor='center')
        container=tk.Frame(frame,bg=BACKGROUND_COLOR,highlightbackground='#78b1e8' if self.games[self.current_game].hands[SOUTH].highlight else 'white',highlightthickness=BORDER_THICKNESS,height=CARD_Y_SIZE+2*BORDER_THICKNESS,width=9*CARD_STEP_X+CARD_X_SIZE+2*BORDER_THICKNESS)
        container.place(x=0,y=0)
        for i,card in enumerate(sorted(self.games[self.current_game].hands[SOUTH].cards)):
            button=tk.Button(container,image=self.images[card.highlight][card.to_string],borderwidth=0,highlightthickness=0,pady=0,padx=0,command=partial(self.action,card=card))
            button.place(x=i*CARD_STEP_X-BORDER_THICKNESS//2,y=-BORDER_THICKNESS//2)
            if not self.games[self.current_game].hands[SOUTH].highlight or card.highlight=='disabled':
                button["state"]='disabled'
        Label(frame,text='SOUTH',fg='#78b1e8' if self.games[self.current_game].hands[SOUTH].highlight else 'white',bg=BACKGROUND_COLOR).place(relx=0.5,rely=0.86,anchor='center')
        frame=tk.Frame(self.root,bg=BACKGROUND_COLOR,bd=0,height=9*CARD_STEP_Y+CARD_Y_SIZE+2*BORDER_THICKNESS+0.3*CARD_Y_SIZE,width=CARD_X_SIZE+2*BORDER_THICKNESS)
        frame.place(relx=0.14,rely=0.49,anchor='center')
        container=tk.Frame(frame,bg=BACKGROUND_COLOR,highlightbackground='#78b1e8' if self.games[self.current_game].hands[WEST].highlight else 'white',highlightthickness=BORDER_THICKNESS,height=9*CARD_STEP_Y+CARD_Y_SIZE+2*BORDER_THICKNESS,width=CARD_X_SIZE+2*BORDER_THICKNESS)
        container.place(x=0,y=0)
        for i,card in enumerate(sorted(self.games[self.current_game].hands[WEST].cards)):
            button=tk.Button(container,image=self.images[card.highlight][card.to_string],highlightthickness=0,borderwidth=0,pady=0,padx=0,command=partial(self.action,card=card))
            button.place(x=-BORDER_THICKNESS//4,y=i*CARD_STEP_Y-BORDER_THICKNESS//4)
            if not self.games[self.current_game].hands[WEST].highlight or card.highlight=='disabled':
                button["state"]='disabled'
        Label(frame,text='WEST',fg='#78b1e8' if self.games[self.current_game].hands[WEST].highlight else 'white',bg=BACKGROUND_COLOR).place(relx=0.5,rely=0.975,anchor='center')
        frame=tk.Frame(self.root,bg=BACKGROUND_COLOR,bd=0,height=9*CARD_STEP_Y+CARD_Y_SIZE+2*BORDER_THICKNESS+0.3*CARD_Y_SIZE,width=CARD_X_SIZE+2*BORDER_THICKNESS)
        frame.place(relx=0.86,rely=0.49,anchor='center')
        container=tk.Frame(frame,bg=BACKGROUND_COLOR,highlightbackground='#78b1e8' if self.games[self.current_game].hands[EAST].highlight else 'white',highlightthickness=BORDER_THICKNESS,height=9*CARD_STEP_Y+CARD_Y_SIZE+2*BORDER_THICKNESS,width=CARD_X_SIZE+2*BORDER_THICKNESS)
        container.place(relx=0,rely=0)
        for i,card in enumerate(sorted(self.games[self.current_game].hands[EAST].cards)):
            button=tk.Button(container,image=self.images[card.highlight][card.to_string],borderwidth=0,highlightthickness=0,pady=0,padx=0,command=partial(self.action,card=card))
            button.place(x=-BORDER_THICKNESS//4,y=i*CARD_STEP_Y-BORDER_THICKNESS//4)
            if not self.games[self.current_game].hands[EAST].highlight or card.highlight=='disabled':
                button["state"]='disabled'
        Label(frame,text='EAST',fg='#78b1e8' if self.games[self.current_game].hands[EAST].highlight else 'white',bg=BACKGROUND_COLOR).place(relx=0.5,rely=0.975,anchor='center')

    def transition_phase(self):
        if self.phase=='deal':
            self.phase='setup'
        elif self.phase=='setup':
            self.phase='solve'
        elif self.phase=='solve':
            self.phase='play'
        elif self.phase=='play':
            self.phase='conclude'
        self.action()
    
    def undo_action(self):
        self.current_game-=1
        self.action()

    def redo_action(self):
        self.current_game+=1
        self.action()

    def quit(self):
        self.root.destroy()

    def flush(self):
        self.games=self.games[:self.current_game+1]
        new_game=self.games[self.current_game].copy()
        new_game.initialize()
        self.games.append(new_game)
        self.current_game+=1
        new_tricks=self.games[self.current_game].flush()
        self.games[self.current_game].past_tricks=[past+new for past,new in zip(self.games[self.current_game].past_tricks,new_tricks)]
        if sum([len(self.games[self.current_game].hands[hand_key].cards) for hand_key in [SOUTH,WEST,EAST]])==0:
            self.transition_phase()
        self.action()
    
    def show_info(self,*args):
        for widget in self.root.winfo_children():
            if '!toplevel' in str(widget):
                return
        contract_interpreter={'M':'MISERE','P':'PLAY'}
        player_interpreter={0:'SOUTH',1:'WEST',2:'EAST'}
        suits_interpreter={0:'SPADES',1:'DIAMONDS',2:'CLUBS',3:'HEARTS','-':'NONE'}
        info_window=tk.Toplevel(self.root)
        info_window.geometry(f"{int(X_SIZE//2.7)}x{X_SIZE//5}")
        info_window.title("Game info")
        frame=tk.Frame(info_window,bd=0,bg='pink3')
        frame.pack(fill='both',side=tk.TOP,expand=True)
        Label(frame,anchor='w',text=f' CONTRACT TYPE:',bg='pink3',fg='white').pack(fill='both',side=tk.LEFT,expand=True,ipady=MESSAGE_FONT//6)
        Label(frame,anchor='e',text=f'{contract_interpreter[self.games[self.current_game].params["type"]]} ',bg='pink3',font=tkf.Font(family="Garamond",size=MESSAGE_FONT),fg='white').pack(fill='both',side=tk.RIGHT,expand=True,ipady=MESSAGE_FONT//6)
        frame=tk.Frame(info_window,bd=0,bg='white')
        frame.pack(fill='both',side=tk.TOP,expand=True)
        Label(frame,anchor='w',text=f' PLAYING HAND:',bg='white',fg='pink3').pack(fill='both',side=tk.LEFT,expand=True,ipady=MESSAGE_FONT//6)
        Label(frame,anchor='e',text=f'{player_interpreter[self.games[self.current_game].params["player"]]} ',bg='white',font=tkf.Font(family="Garamond",size=MESSAGE_FONT),fg='pink3').pack(fill='both',side=tk.RIGHT,expand=True,ipady=MESSAGE_FONT//6)
        frame=tk.Frame(info_window,bd=0,bg='pink3')
        frame.pack(fill='both',side=tk.TOP,expand=True)
        Label(frame,anchor='w',text=f' FIRST HAND:',bg='pink3',fg='white').pack(fill='both',side=tk.LEFT,expand=True,ipady=MESSAGE_FONT//6)
        Label(frame,anchor='e',text=f'{player_interpreter[self.games[0].params["turn"]]} ',bg='pink3',fg='white').pack(fill='both',side=tk.RIGHT,expand=True,ipady=MESSAGE_FONT//6)
        frame=tk.Frame(info_window,bd=0,bg='white')
        frame.pack(fill='both',side=tk.TOP,expand=True)
        Label(frame,anchor='w',text=f' TRUMP SUIT:',bg='white',fg='pink3').pack(fill='both',side=tk.LEFT,expand=True,ipady=MESSAGE_FONT//6)
        Label(frame,anchor='e',text=f'{suits_interpreter[self.games[self.current_game].params["trumps"]]} ',bg='white',fg='pink3').pack(fill='both',side=tk.RIGHT,expand=True,ipady=MESSAGE_FONT//6)
        info_window.mainloop()

    def action(self,**kwargs):
        if self.phase=='deal':
            if 'card' in kwargs:
                self.games=self.games[:self.current_game+1]
                new_game=self.games[self.current_game].copy()
                self.games.append(new_game)
                self.current_game+=1
                if len(self.games[self.current_game].hands[SOUTH].cards)<10:
                    self.games[self.current_game].hands[SOUTH].add(kwargs['card'])
                elif len(self.games[self.current_game].hands[WEST].cards)<10:
                    self.games[self.current_game].hands[WEST].add(kwargs['card'])
                elif len(self.games[self.current_game].hands[EAST].cards)<10:
                    self.games[self.current_game].hands[EAST].add(kwargs['card'])
            if len(self.games[self.current_game].hands[SOUTH].cards)+len(self.games[self.current_game].hands[WEST].cards)+len(self.games[self.current_game].hands[EAST].cards)==30:
                self.games=[self.games[self.current_game]]
                self.current_game=0
                self.transition_phase()
        elif self.phase=='setup':
            if 'param' in kwargs:
                self.games[self.current_game].params[kwargs['param']]=kwargs['val']
                if self.games[self.current_game].params['type']=='M':
                    self.games[self.current_game].params['trumps']='-'
        elif self.phase=='solve':
            self.draw()
            self.root.update()
            self.games[self.current_game].initialize()
            solver = Solver(self.games[self.current_game])
            self.solution_stats=solver.solve()
            self.solution=solver.dp
        elif self.phase=='play':
            if 'card' in kwargs:
                self.games=self.games[:self.current_game+1]
                new_game=self.games[self.current_game].copy()
                new_game.initialize()
                self.games.append(new_game)
                self.current_game+=1
                new_tricks = self.games[self.current_game].play_card(kwargs['card'])
                self.games[self.current_game].past_tricks=[past+new for past,new in zip(self.games[self.current_game].past_tricks,new_tricks)]
            if len(self.games[self.current_game].hands[TRICK].cards)<3:
                solution=self.solution[self.games[self.current_game].to_string()]
                optimal_tricks=[solution[self.games[self.current_game].players[SOUTH]],
                                solution[self.games[self.current_game].players[WEST]],
                                solution[self.games[self.current_game].players[EAST]]]
                self.games[self.current_game].future_tricks=optimal_tricks
                for card in CARDS:
                    card.highlight='normal'
                for card in self.games[self.current_game].hands[self.games[self.current_game].params['turn']].cards:
                    if card in self.games[self.current_game].hands[self.games[self.current_game].params['turn']].options(self.games[self.current_game].hands[TRICK],self.games[self.current_game].params['trumps']):
                        virtual_game=self.games[self.current_game].copy()
                        virtual_game.initialize()
                        virtual_game.hands[TRICK].auto_flush=True
                        virtual_new_tricks=virtual_game.play_card(card)
                        #if len(virtual_game.hands[TRICK].cards)==3:
                        #    virtual_new_tricks=virtual_game.flush()
                        solution=self.solution[virtual_game.to_string()]
                        potential_tricks=[solution[virtual_game.players[SOUTH]],
                                        solution[virtual_game.players[WEST]],
                                        solution[virtual_game.players[EAST]]]
                        if potential_tricks[self.games[self.current_game].params['player']]+virtual_new_tricks[self.games[self.current_game].params['player']]==optimal_tricks[self.games[self.current_game].params['player']]:
                            card.highlight='optimal'
                    else:
                        card.highlight='disabled'
            else:
                for card in CARDS:
                    card.highlight='disabled'
            for hand_key in [SOUTH,WEST,EAST]:
                self.games[self.current_game].hands[hand_key].highlight=self.games[self.current_game].params['turn']==hand_key and len(self.games[self.current_game].hands[TRICK].cards)<3
        self.draw()

    def draw(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            del widget
        if self.phase=='deal':
            self.draw_players()
            if len(self.games[self.current_game].hands[SOUTH].cards)<10:
                message=f'SELECT {10-len(self.games[self.current_game].hands[SOUTH].cards)} CARDS FOR SOUTH'
            elif len(self.games[self.current_game].hands[WEST].cards)<10:
                message=f'SELECT {10-len(self.games[self.current_game].hands[WEST].cards)} CARDS FOR WEST'
            elif len(self.games[self.current_game].hands[EAST].cards)<10:
                message=f'SELECT {10-len(self.games[self.current_game].hands[EAST].cards)} CARDS FOR EAST'
            Label(self.root,text=message,fg='white',bg=BACKGROUND_COLOR).place(relx=0.5,rely=0.14,anchor='center')
            container=tk.Frame(self.root,bg=BACKGROUND_COLOR,bd=0,height=2.16*CARD_Y_SIZE,width=15*CARD_STEP_X/1.5+2.05*CARD_X_SIZE)
            container.place(relx=0.5,rely=0.37,anchor='center')
            for i,card in enumerate(CARDS):
                if card not in self.games[self.current_game].hands[SOUTH].cards and card not in self.games[self.current_game].hands[WEST].cards and card not in self.games[self.current_game].hands[EAST].cards:
                    button=tk.Button(container,image=self.images['normal'][card.to_string],borderwidth=0,bg=BACKGROUND_COLOR,highlightthickness=0,pady=0,padx=0,command=partial(self.action,card=card))
                    button.place(x=(CARD_STEP_X/1.5)*(i%16)+CARD_X_SIZE*(i%16>7),y=(1.15*CARD_Y_SIZE)*(i>=16))
            button=Button(self.root,text='RANDOM DEAL',fg=BACKGROUND_COLOR, bg='white',pady=0,padx=0,command=self.random_deal)
            button.place(relx=0.5,rely=0.37+1.1*CARD_Y_SIZE/Y_SIZE+0.05,anchor='center')
            button=Button(self.root,text='UNDO',fg=BACKGROUND_COLOR,bg='white',pady=0,padx=0,command=self.undo_action)
            button.place(relx=0.35,rely=0.37+1.1*CARD_Y_SIZE/Y_SIZE+0.05,anchor='center')
            if self.current_game==0:
                button['state']='disabled'
            button=Button(self.root,text='REDO',fg=BACKGROUND_COLOR,bg='white',pady=0,padx=0,command=self.redo_action)
            button.place(relx=0.65,rely=0.37+1.1*CARD_Y_SIZE/Y_SIZE+0.05,anchor='center')
            if self.current_game==len(self.games)-1:
                button['state']='disabled'
        if self.phase=='setup':
            self.draw_players()
            container=tk.Frame(self.root,bg=BACKGROUND_COLOR,bd=0,height=Y_SIZE//2,width=X_SIZE//2.5)
            container.place(relx=0.5,rely=0.4,anchor='center')
            container.grid_propagate(0)
            for col in range(6):
                container.grid_columnconfigure(col,weight=1,uniform='_')
            Label(container,text="CONTRACT TYPE:",bg=BACKGROUND_COLOR,fg='white').grid(row=0,columnspan=6,sticky=tk.W)
            button=Button(container,bg='white',text="PLAY",fg=BACKGROUND_COLOR,command=partial(self.action,param='type',val='P'))
            button.grid(row=1,column=0,columnspan=3,sticky=tk.NSEW)
            if self.games[self.current_game].params['type']=='P':
                button.config(bg='#78b1e8',fg='white')
            button=Button(container,bg='white',text="MISERE",fg=BACKGROUND_COLOR,command=partial(self.action,param='type',val='M'))
            button.grid(row=1,column=3,columnspan=3,sticky=tk.NSEW)
            if self.games[self.current_game].params['type']=='M':
                button.config(bg='#78b1e8',fg='white')
            Label(container,text="PLAYING HAND:",bg=BACKGROUND_COLOR,fg='white').grid(row=2,columnspan=6,sticky=tk.W)
            button=Button(container,bg='white',text="SOUTH",fg=BACKGROUND_COLOR,command=partial(self.action,param='player',val=0))
            button.grid(row=3,column=0,columnspan=2,sticky=tk.NSEW)
            if self.games[self.current_game].params['player']==SOUTH:
                button.config(bg='#78b1e8',fg='white')
            button=Button(container,bg='white',text="WEST",fg=BACKGROUND_COLOR,command=partial(self.action,param='player',val=1))
            button.grid(row=3,column=2,columnspan=2,sticky=tk.NSEW)
            if self.games[self.current_game].params['player']==WEST:
                button.config(bg='#78b1e8',fg='white')
            button=Button(container,bg='white',text="EAST",fg=BACKGROUND_COLOR,command=partial(self.action,param='player',val=2))
            button.grid(row=3,column=4,columnspan=2,sticky=tk.NSEW)
            if self.games[self.current_game].params['player']==EAST:
                button.config(bg='#78b1e8',fg='white')
            Label(container,text="FIRST HAND:",bg=BACKGROUND_COLOR,fg='white').grid(row=4,columnspan=6,sticky=tk.W)
            button=Button(container,bg='white',text="SOUTH",fg=BACKGROUND_COLOR,command=partial(self.action,param='turn',val=0))
            button.grid(row=5,columnspan=2,column=0,sticky=tk.NSEW)
            if self.games[self.current_game].params['turn']==SOUTH:
                button.config(bg='#78b1e8',fg='white')
            button=Button(container,bg='white',text="WEST",fg=BACKGROUND_COLOR,command=partial(self.action,param='turn',val=1))
            button.grid(row=5,columnspan=2,column=2,sticky=tk.NSEW)
            if self.games[self.current_game].params['turn']==WEST:
                button.config(bg='#78b1e8',fg='white')
            button=Button(container,bg='white',text="EAST",fg=BACKGROUND_COLOR,command=partial(self.action,param='turn',val=2))
            button.grid(row=5,columnspan=2,column=4,sticky=tk.NSEW)
            if self.games[self.current_game].params['turn']==EAST:
                button.config(bg='#78b1e8',fg='white')
            Label(container,text="TRUMP SUIT:",bg=BACKGROUND_COLOR,fg='white').grid(row=6,columnspan=6,sticky=tk.W)
            button=Button(container,bg='white',image=self.images['utils']['Sb'],fg=BACKGROUND_COLOR,command=partial(self.action,param='trumps',val=SPADES))
            button.grid(row=7,column=0,sticky=tk.NSEW)
            if self.games[self.current_game].params['trumps']==SPADES:
                button.config(bg='#78b1e8',image=self.images['utils']['Sw'])
            if self.games[self.current_game].params['type']=='M':
                button["state"]="disabled"
            button=Button(container,bg='white',image=self.images['utils']['Cb'],fg=BACKGROUND_COLOR,command=partial(self.action,param='trumps',val=CLUBS))
            button.grid(row=7,column=1,sticky=tk.NSEW)
            if self.games[self.current_game].params['trumps']==CLUBS:
                button.config(bg='#78b1e8',image=self.images['utils']['Cw'])      
            if self.games[self.current_game].params['type']=='M':
                button["state"]="disabled"
            button=Button(container,bg='white',image=self.images['utils']['Db'],fg=BACKGROUND_COLOR,command=partial(self.action,param='trumps',val=DIAMONDS))
            button.grid(row=7,column=2,sticky=tk.NSEW)
            if self.games[self.current_game].params['trumps']==DIAMONDS:
                button.config(bg='#78b1e8',image=self.images['utils']['Dw']) 
            if self.games[self.current_game].params['type']=='M':
                button["state"]="disabled"
            button=Button(container,bg='white',image=self.images['utils']['Hb'],fg=BACKGROUND_COLOR,command=partial(self.action,param='trumps',val=HEARTS))
            button.grid(row=7,column=3,sticky=tk.NSEW)
            if self.games[self.current_game].params['trumps']==HEARTS:
                button.config(bg='#78b1e8',image=self.images['utils']['Hw']) 
            if self.games[self.current_game].params['type']=='M':
                button["state"]='disabled'
            button=Button(container,bg='white',text='NONE',fg=BACKGROUND_COLOR,command=partial(self.action,param='trumps',val='-'))
            button.grid(row=7,column=4,columnspan=2,sticky=tk.NSEW)
            if self.games[self.current_game].params['trumps']=='-':
                button.config(bg='#78b1e8',fg='white')
            if all([param is not None for param in list(self.games[self.current_game].params.values())]):
                frame=tk.Frame(container,bd=0,height=Y_SIZE//20,width=X_SIZE//2.5,bg=BACKGROUND_COLOR)
                frame.grid(row=8,column=0,columnspan=6,sticky=tk.W)
                button=Button(container,text='OK',bg='white',fg=BACKGROUND_COLOR,command=self.transition_phase)
                button.grid(row=9,column=2,columnspan=2,sticky=tk.NSEW)
        elif self.phase=='solve':
            self.draw_players()
            if self.solution is None:
                Label(self.root,text="SOLUTION IN PROGRESS...",bg=BACKGROUND_COLOR,fg='white').place(relx=0.5,rely=0.15,anchor='center')
            else:
                Label(self.root,text=f'SOLVED {self.solution_stats["subgames"]:,} SUBGAMES IN {self.solution_stats["time"]:.1f} SEC',bg=BACKGROUND_COLOR,fg='white').place(relx=0.5,rely=0.15,anchor='center')
                Button(self.root,text='START',bg='white',fg=BACKGROUND_COLOR,command=self.transition_phase).place(relx=0.5,rely=0.24,anchor='center')
        elif self.phase=='play':
            self.draw_players()
            frame=tk.Frame(self.root,bg=BACKGROUND_COLOR,highlightbackground='white',highlightthickness=BORDER_THICKNESS,height=CARD_Y_SIZE+2*BORDER_THICKNESS,width=CARD_X_SIZE+2*BORDER_THICKNESS)
            frame.place(relx=0.5,rely=0.45,anchor='center')
            container=Label(frame,width=CARD_X_SIZE,height=CARD_Y_SIZE,bg=BACKGROUND_COLOR)
            container.place(x=0,y=0,width=CARD_X_SIZE,height=CARD_Y_SIZE)
            for card in self.games[self.current_game].hands[TRICK].cards:
                if card in self.games[0].hands[SOUTH].cards:
                    container.config(image=self.images['normal'][card.to_string])
            canvas=tk.Canvas(self.root,width=CARD_STEP_Y*9+CARD_STEP_Y,height=CARD_STEP_X,bg=BACKGROUND_COLOR,bd=0,highlightthickness=0)
            canvas.place(relx=0.5,rely=0.68,anchor='center')
            current_tricks=self.games[self.current_game].past_tricks[SOUTH]
            total_tricks=self.games[self.current_game].future_tricks[SOUTH]
            canvas.create_text(CARD_STEP_Y*9//2+CARD_STEP_Y//2,CARD_STEP_X//1.3,angle=0,text=f"current/projected: {current_tricks}/{current_tricks+total_tricks}",fill='#78b1e8' if self.games[self.current_game].hands[SOUTH].highlight else 'white',font=tkf.Font(family="Garamond",size=MESSAGE_FONT),anchor='s',justify=tk.CENTER)
            frame=tk.Frame(self.root,bg=BACKGROUND_COLOR,highlightbackground='white',highlightthickness=BORDER_THICKNESS,height=CARD_Y_SIZE+2*BORDER_THICKNESS,width=CARD_X_SIZE+2*BORDER_THICKNESS)
            frame.place(relx=0.5-CARD_X_SIZE/(2*X_SIZE)-3*BORDER_THICKNESS/X_SIZE,rely=0.45-CARD_Y_SIZE/Y_SIZE-6*BORDER_THICKNESS/Y_SIZE,anchor='center')
            container=Label(frame,width=CARD_X_SIZE,height=CARD_Y_SIZE,bg=BACKGROUND_COLOR)
            container.place(x=0,y=0,width=CARD_X_SIZE,height=CARD_Y_SIZE)
            for card in self.games[self.current_game].hands[TRICK].cards:
                if card in self.games[0].hands[WEST].cards:
                    container.config(image=self.images['normal'][card.to_string])        
            canvas=tk.Canvas(self.root,width=CARD_STEP_X,height=CARD_STEP_Y*9+CARD_STEP_Y,bg=BACKGROUND_COLOR,bd=0,highlightthickness=0)
            canvas.place(relx=0.205,rely=0.47,anchor='center')
            current_tricks=self.games[self.current_game].past_tricks[WEST]
            total_tricks=self.games[self.current_game].future_tricks[WEST]
            canvas.create_text(CARD_STEP_X//1.3,CARD_STEP_Y*9//2+CARD_STEP_Y//2,angle=90,text=f"current/projected: {current_tricks}/{current_tricks+total_tricks}",fill='#78b1e8' if self.games[self.current_game].hands[WEST].highlight else 'white',font=tkf.Font(family="Garamond",size=MESSAGE_FONT),anchor='s',justify=tk.CENTER)
            frame=tk.Frame(self.root,bg=BACKGROUND_COLOR,highlightbackground='white',highlightthickness=BORDER_THICKNESS,height=CARD_Y_SIZE+2*BORDER_THICKNESS,width=CARD_X_SIZE+2*BORDER_THICKNESS)
            frame.place(relx=0.5+CARD_X_SIZE/(2*X_SIZE)+3*BORDER_THICKNESS/X_SIZE,rely=0.45-CARD_Y_SIZE/Y_SIZE-6*BORDER_THICKNESS/Y_SIZE,anchor='center')
            container=Label(frame,bg=BACKGROUND_COLOR)
            container.place(x=0,y=0,width=CARD_X_SIZE,height=CARD_Y_SIZE)
            for card in self.games[self.current_game].hands[TRICK].cards:
                if card in self.games[0].hands[EAST].cards:
                    container.config(image=self.images['normal'][card.to_string])
            canvas=tk.Canvas(self.root,width=CARD_STEP_X,height=CARD_STEP_Y*9+CARD_STEP_Y,bg=BACKGROUND_COLOR,bd=0,highlightthickness=0)
            canvas.place(relx=0.79,rely=0.47,anchor='center')
            current_tricks=self.games[self.current_game].past_tricks[EAST]
            total_tricks=self.games[self.current_game].future_tricks[EAST]
            canvas.create_text(CARD_STEP_X,CARD_STEP_Y*9//2+CARD_STEP_Y//2,angle=90,text=f"current/projected: {current_tricks}/{current_tricks+total_tricks}",fill='#78b1e8' if self.games[self.current_game].hands[EAST].highlight else 'white',font=tkf.Font(family="Garamond",size=MESSAGE_FONT),anchor='s',justify=tk.CENTER)
            button=Button(self.root,text='UNDO',bg='white',fg=BACKGROUND_COLOR,command=self.undo_action)
            button.place(relx=0.37,rely=0.6,anchor='center')
            if self.current_game==0:
                button["state"]='disabled'
            button=Button(self.root,text='REDO',bg='white',fg=BACKGROUND_COLOR,command=self.redo_action)
            button.place(relx=0.63,rely=0.6,anchor='center')
            if self.current_game==len(self.games)-1:
                button["state"]='disabled'
            if len(self.games[self.current_game].hands[TRICK].cards)==3:
                Button(self.root,text='CONTINUE',bg='white',fg=BACKGROUND_COLOR,command=self.flush).place(relx=0.5,rely=0.6,anchor='center')
            info=Label(self.root,image=self.info_image)
            info.bind('<Button-1>',self.show_info)
            info.place(relx=0.96,rely=0.95,anchor='center')
        elif self.phase=='conclude':
            frame=tk.Frame(self.root,bg=BACKGROUND_COLOR,height=Y_SIZE//2,width=X_SIZE//2)
            frame.place(relx=0.5,rely=0.5,anchor='center')
            container=Label(frame,bg=BACKGROUND_COLOR)
            container.place(x=0,y=0,height=Y_SIZE//1.9,width=X_SIZE//1.9)
            container.grid_propagate(0)
            container.grid_columnconfigure(0,weight=2,uniform='_')
            for col in range(1,4):
                container.grid_columnconfigure(col,weight=1,uniform='_')
            Label(container,text="SOUTH",bg=BACKGROUND_COLOR,fg='#78b1e8' if self.games[0].params['player']==SOUTH else 'white').grid(row=0,column=1,sticky=tk.NSEW,pady=MESSAGE_FONT//3)
            Label(container,text="WEST",bg=BACKGROUND_COLOR,fg='#78b1e8' if self.games[0].params['player']==WEST else 'white').grid(row=0,column=2,sticky=tk.NSEW,pady=MESSAGE_FONT//3)
            Label(container,text="EAST",bg=BACKGROUND_COLOR,fg='#78b1e8' if self.games[0].params['player']==EAST else 'white').grid(row=0,column=3,sticky=tk.NSEW,pady=MESSAGE_FONT//3)
            Label(container,text="FINAL TRICKS",bg=BACKGROUND_COLOR,fg='white').grid(row=1,column=0,sticky=tk.W,pady=MESSAGE_FONT//3)
            Label(container,text="OPTIMAL TRICKS",bg=BACKGROUND_COLOR,fg='white').grid(row=2,column=0,sticky=tk.W,pady=MESSAGE_FONT//3)
            Label(container,text=f"{self.games[-1].past_tricks[SOUTH]}",font=tkf.Font(family="Garamond",size=2*MESSAGE_FONT),bg=BACKGROUND_COLOR,fg='#78b1e8' if self.games[0].params['player']==SOUTH else 'white').grid(row=1,column=1,sticky=tk.NSEW,pady=MESSAGE_FONT//3)
            Label(container,text=f"{self.games[-1].past_tricks[WEST]}",font=tkf.Font(family="Garamond",size=2*MESSAGE_FONT),bg=BACKGROUND_COLOR,fg='#78b1e8' if self.games[0].params['player']==WEST else 'white').grid(row=1,column=2,sticky=tk.NSEW,pady=MESSAGE_FONT//3)
            Label(container,text=f"{self.games[-1].past_tricks[EAST]}",font=tkf.Font(family="Garamond",size=2*MESSAGE_FONT),bg=BACKGROUND_COLOR,fg='#78b1e8' if self.games[0].params['player']==EAST else 'white').grid(row=1,column=3,sticky=tk.NSEW,pady=MESSAGE_FONT//3)
            Label(container,text=f"{self.solution[self.games[0].to_string()][self.players[SOUTH]]}",font=tkf.Font(family="Garamond",size=2*MESSAGE_FONT),bg=BACKGROUND_COLOR,fg='#78b1e8' if self.games[0].params['player']==SOUTH else 'white').grid(row=2,column=1,sticky=tk.NSEW,pady=MESSAGE_FONT//3)
            Label(container,text=f"{self.solution[self.games[0].to_string()][self.players[WEST]]}",font=tkf.Font(family="Garamond",size=2*MESSAGE_FONT),bg=BACKGROUND_COLOR,fg='#78b1e8' if self.games[0].params['player']==WEST else 'white').grid(row=2,column=2,sticky=tk.NSEW,pady=MESSAGE_FONT//3)
            Label(container,text=f"{self.solution[self.games[0].to_string()][self.players[EAST]]}",font=tkf.Font(family="Garamond",size=2*MESSAGE_FONT),bg=BACKGROUND_COLOR,fg='#78b1e8' if self.games[0].params['player']==EAST else 'white').grid(row=2,column=3,sticky=tk.NSEW,pady=MESSAGE_FONT//3)
            Button(self.root,text='QUIT',bg='white',fg=BACKGROUND_COLOR,command=self.quit).place(relx=0.5,rely=0.7,anchor='center')  