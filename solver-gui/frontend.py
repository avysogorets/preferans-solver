import time
import tkinter as tk
import tkinter.font as tkf
from PIL import Image,ImageTk
from preferans_backend import *
from functools import partial
import numpy as np
from tkmacosx import Button as MacButton

X_SIZE,Y_SIZE=960,640
CARD_X_SIZE=X_SIZE//12
CARD_Y_SIZE=CARD_X_SIZE*890//634
CARD_STEP_X=CARD_X_SIZE//2.5
CARD_STEP_Y=CARD_Y_SIZE//2.8
BACKGROUND_COLOR='maroon'
PLAYER_X_SIZE=50
PLAYER_Y_SIZE=30
BORDER_THICKNESS=CARD_X_SIZE//30
IMG_DIR='preferans_cards'
IMG_DIR_INACTIVE='preferans_cards_inactive'
IMG_DIR_OPTIMAL='preferans_cards_optimal'

def equivalence_classes(hand):
    classes=[]
    for i,card in enumerate(sorted(hand.cards)):
        if i>0 and sorted(hand.cards)[i-1].suit==card.suit and sorted(hand.cards)[i-1].kind==card.kind-1:
            classes[-1].append(card)
        else:
            classes.append([card])
    return classes

def deal_card(key):
    buttons[key].destroy()
    del buttons[key]
    if len(buttons)>22:
        deal_message.set(f'Select {(len(buttons)-2)%10 if (len(buttons)-2)%10>0 else 10} card{"s" if (len(buttons)-2)%10!=1 else ""} for SOUTH')
    if len(buttons)<=22 and len(buttons)>12:
        deal_message.set(f'Select {(len(buttons)-2)%10 if (len(buttons)-2)%10>0 else 10} card{"s" if (len(buttons)-2)%10!=1 else ""} for WEST')
    if len(buttons)<=12:
        deal_message.set(f'Select {(len(buttons)-2)%10 if (len(buttons)-2)%10>0 else 10} card{"s" if (len(buttons)-2)%10!=1 else ""} for EAST')
    if len(buttons)<32 and len(buttons)>=22:
        curr_index=0
        sorted_cards=sorted(south_buttons.items(),key=lambda item:CARDS[tuple(item[0].split(':'))])
        while curr_index<len(south_buttons) and CARDS[tuple(sorted_cards[curr_index][0].split(':'))]<CARDS[tuple(key.split(':'))]:
            curr_index+=1
        south_buttons[key]=tk.Button(south_cards_container,image=images[key],borderwidth=0,bg=BACKGROUND_COLOR,highlightthickness=0,pady=0,padx=0,command=partial(play_card_wrapper,key))
        south_buttons[key].place(x=curr_index*CARD_STEP_X-BORDER_THICKNESS//2,y=-BORDER_THICKNESS//2)
        while curr_index<len(south_buttons)-1:
            sorted_cards[curr_index][1].place(x=(curr_index+1)*CARD_STEP_X-BORDER_THICKNESS//2,y=-BORDER_THICKNESS//2)
            sorted_cards[curr_index][1].tkraise()
            curr_index+=1
    if len(buttons)<22 and len(buttons)>=12:
        curr_index=0
        sorted_cards=sorted(west_buttons.items(),key=lambda item:CARDS[tuple(item[0].split(':'))])
        while curr_index<len(west_buttons) and CARDS[tuple(sorted_cards[curr_index][0].split(':'))]<CARDS[tuple(key.split(':'))]:
            curr_index+=1
        west_buttons[key]=tk.Button(west_cards_container,image=images[key],borderwidth=0,bg=BACKGROUND_COLOR,highlightthickness=0,pady=0,padx=0,command=partial(play_card_wrapper,key))
        west_buttons[key].place(x=-BORDER_THICKNESS//4,y=curr_index*CARD_STEP_Y-BORDER_THICKNESS//2)
        while curr_index<len(west_buttons)-1:
            sorted_cards[curr_index][1].place(x=-BORDER_THICKNESS//4,y=(curr_index+1)*CARD_STEP_Y-BORDER_THICKNESS//4)
            sorted_cards[curr_index][1].tkraise()
            curr_index+=1
    if len(buttons)<12 and len(buttons)>=2:
        curr_index=0
        sorted_cards=sorted(east_buttons.items(),key=lambda item:CARDS[tuple(item[0].split(':'))])
        while curr_index<len(east_buttons) and CARDS[tuple(sorted_cards[curr_index][0].split(':'))]<CARDS[tuple(key.split(':'))]:
            curr_index+=1
        east_buttons[key]=tk.Button(east_cards_container,image=images[key],borderwidth=0,bg=BACKGROUND_COLOR,highlightthickness=0,pady=0,padx=0,command=partial(play_card_wrapper,key))
        east_buttons[key].place(x=-BORDER_THICKNESS//4,y=curr_index*CARD_STEP_Y-BORDER_THICKNESS//4)
        while curr_index<len(east_buttons)-1:
            sorted_cards[curr_index][1].place(x=-BORDER_THICKNESS//4,y=(curr_index+1)*CARD_STEP_Y-BORDER_THICKNESS//4)
            sorted_cards[curr_index][1].tkraise()
            curr_index+=1
    if len(buttons)==2:
        for widget in deal_cards_container.winfo_children():
            widget.destroy()
        deal_cards_container.destroy()
        deal_message_container.destroy()
        global game_params,params_buttons,set_up_container,suit_imgs,params_msgs,card_buttons
        card_buttons={0:south_buttons,1:west_buttons,2:east_buttons}
        game_params,params_buttons,suit_imgs,params_msgs=dict(),dict(),dict(),dict()
        game_params['hands']={0:south_buttons.keys(),1:west_buttons.keys(),2:east_buttons.keys()}
        set_up_container=tk.Frame(root,bg=BACKGROUND_COLOR,bd=0,height=Y_SIZE//1.7,width=X_SIZE//2.5)
        set_up_container.place(relx=0.5,rely=0.375,anchor='center')
        set_up_container.grid_propagate(0)
        for col in range(6):
            set_up_container.grid_columnconfigure(col,weight=1,uniform='_')
        for suit in SUITS_TO_CODE.keys():
            if suit!='-':
                suit_imgs[suit]=Image.open(IMG_DIR+f"/{suit}.png")
                suit_imgs[suit+'-white']=Image.open(IMG_DIR+f"/{suit}-white.png")
        for key,image in suit_imgs.items():
            suit_imgs[key]=ImageTk.PhotoImage(image.resize((20,int(image.size[1]*(20/image.size[0]))),Image.ANTIALIAS))
        type_setup()
        player_setup()
        turn_setup()
        major_suit_setup()
        button_random.destroy()

def play_card_wrapper(card_key):
    global continue_button
    card_buttons[game_params['turn']][card_key].destroy()
    del card_buttons[game_params['turn']][card_key]
    trick_containers[game_params['turn']].config(image=images[card_key])
    for equiv_class in classes[game_params['turn']]:
        if CARDS[tuple(card_key.split(':'))] in equiv_class:
            current_equivalence_class=equiv_class
    for card in current_equivalence_class:
        local_hand=Hand(virtual_hands[game_params['turn']].cards)
        local_flop=Hand(virtual_hands[3].cards)
        _,new_turn=local_hand.play_card(card,game_params['turn'],local_flop)
        key_string=' '.join([hand.to_string() for hand in virtual_hands[:game_params['turn']]+[local_hand]+virtual_hands[game_params['turn']+1:-1]+[local_flop]])+f' {new_turn}'
        if key_string in solution:
            virtual_hands[game_params['turn']].play_card(card,game_params['turn'],virtual_hands[3])
            break
    history[game_params['turn']].append(card_key)
    tricks,game_params['turn']=game_params['hands'][game_params['turn']].play_card(CARDS[tuple(card_key.split(':'))],game_params['turn'],game_params['hands'][3])
    num_tricks=solution[key_string]['num_tricks']
    current_tricks[0]=current_tricks[0]+tricks[0]
    current_tricks[1]=current_tricks[1]+tricks[1]
    current_tricks[2]=current_tricks[2]+tricks[2]
    optimal_cards=[]
    for card in game_params['hands'][game_params['turn']].options(game_params['hands'][3].cards[0],all=True):
        for equiv_class in classes[game_params['turn']]:
            if card in equiv_class:
                current_equivalence_class=equiv_class
        for card in current_equivalence_class:
            local_hand=Hand(virtual_hands[game_params['turn']].cards)
            local_flop=Hand(virtual_hands[3].cards)
            new_tricks,new_turn=local_hand.play_card(card,game_params['turn'],local_flop)
            key_string=' '.join([hand.to_string() for hand in virtual_hands[:game_params['turn']]+[local_hand]+virtual_hands[game_params['turn']+1:-1]+[local_flop]])+f' {new_turn}'
            if key_string in solution and [future+current for future,current in zip(solution[key_string]['num_tricks'],new_tricks)][game_params['player']]==num_tricks[game_params['player']]:
                for card in current_equivalence_class:
                    optimal_cards.append(card)
    hand_info_canvases[0].itemconfig(hand_info_texts[0],text=f"current/projected: {current_tricks[0]}/{current_tricks[0]+num_tricks[0]}")
    hand_info_canvases[1].itemconfig(hand_info_texts[1],text=f"current/projected: {current_tricks[1]}/{current_tricks[1]+num_tricks[1]}")
    hand_info_canvases[2].itemconfig(hand_info_texts[2],text=f"current/projected: {current_tricks[2]}/{current_tricks[2]+num_tricks[2]}")
    if sum(len(card_button.items()) for card_button in card_buttons.values())%3==0 and sum(len(card_button.items()) for card_button in card_buttons.values())<30:
        continue_button=tk.Button(root,text='CONTINUE',borderwidth=0,bg='white',font=tkf.Font(family="Garamond",size=24),fg=BACKGROUND_COLOR,highlightthickness=0)
        continue_button.config(command=partial(erase_tricks,optimal_cards,game_params['hands'][3].cards[0]))
        continue_button.place(relx=0.5,rely=0.6,anchor='center')
        for card_button in card_buttons.values():
            for button in card_button.values():
                button["state"]="disable"
        history['num_tricks'].append(num_tricks)
    else:
        highlight(optimal_cards,game_params['hands'][3].cards[0])

def random_deal():
    card_keys=np.random.choice([card.to_string for card in CARDS.values() if '-' not in card.to_string],size=len(buttons)-2,replace=False)
    for card_key in card_keys:
        deal_card(card_key)
    

def highlight(optimal_cards,flop):
    for key,card_button in card_buttons[(game_params['turn']+1)%3].items():
        card_button.config(image=images[key])
        card_button["state"]="disabled"
    for key,card_button in card_buttons[(game_params['turn']+2)%3].items():
        card_button.config(image=images[key])
        card_button["state"]="disabled"
    for key,card_button in card_buttons[game_params['turn']].items():
        card_button.config(image=images_inactive[key])
        card_button["state"]="disabled"
    for card in game_params['hands'][game_params['turn']].options(flop,all=True):
        if card.to_string in [card.to_string for card in optimal_cards] and card.to_string not in history[game_params['turn']]:
            card_buttons[game_params['turn']][card.to_string].config(image=images_optimal[card.to_string])
        else:
            card_buttons[game_params['turn']][card.to_string].config(image=images[card.to_string])
        card_buttons[game_params['turn']][card.to_string]["state"]="normal"

def play_setup():
    start_button.destroy()
    info_message_container.destroy()
    global trick_containers,tricks,card_key,history,hand_info_canvases,hand_info_texts,current_tricks
    south_card_container=tk.Frame(root,bg=BACKGROUND_COLOR,highlightbackground='white',highlightthickness=BORDER_THICKNESS,height=CARD_Y_SIZE+2*BORDER_THICKNESS,width=CARD_X_SIZE+2*BORDER_THICKNESS)
    south_card_container.place(relx=0.5,rely=0.45,anchor='center')
    south_card=tk.Label(south_card_container,width=CARD_X_SIZE,height=CARD_Y_SIZE,bg=BACKGROUND_COLOR)
    south_card.place(x=0,y=0,width=CARD_X_SIZE,height=CARD_Y_SIZE)
    west_card_container=tk.Frame(root,bg=BACKGROUND_COLOR,highlightbackground='white',highlightthickness=BORDER_THICKNESS,height=CARD_Y_SIZE+2*BORDER_THICKNESS,width=CARD_X_SIZE+2*BORDER_THICKNESS)
    west_card_container.place(relx=0.5-CARD_X_SIZE/(2*X_SIZE)-3*BORDER_THICKNESS/X_SIZE,rely=0.45-CARD_Y_SIZE/Y_SIZE-6*BORDER_THICKNESS/Y_SIZE,anchor='center')
    west_card=tk.Label(west_card_container,width=CARD_X_SIZE,height=CARD_Y_SIZE,bg=BACKGROUND_COLOR)
    west_card.place(x=0,y=0,width=CARD_X_SIZE,height=CARD_Y_SIZE)
    east_card_container=tk.Frame(root,bg=BACKGROUND_COLOR,highlightbackground='white',highlightthickness=BORDER_THICKNESS,height=CARD_Y_SIZE+2*BORDER_THICKNESS,width=CARD_X_SIZE+2*BORDER_THICKNESS)
    east_card_container.place(relx=0.5+CARD_X_SIZE/(2*X_SIZE)+3*BORDER_THICKNESS/X_SIZE,rely=0.45-CARD_Y_SIZE/Y_SIZE-6*BORDER_THICKNESS/Y_SIZE,anchor='center')
    east_card=tk.Label(east_card_container,bg=BACKGROUND_COLOR)
    east_card.place(x=0,y=0,width=CARD_X_SIZE,height=CARD_Y_SIZE)
    trick_containers=[south_card,west_card,east_card]
    key_string=' '.join([hand.to_string() for hand in game_params['hands']])+f' {game_params["turn"]}'
    history={0:[],1:[],2:[],'num_tricks':[solution[key_string]['num_tricks']]}
    optimal_num_tricks=solution[key_string]['num_tricks']
    optimal_cards=[]
    for card in game_params['hands'][game_params['turn']].options(game_params['hands'][3].cards[0],all=True):
        for equiv_class in classes[game_params['turn']]:
            if card in equiv_class:
                current_equivalence_class=equiv_class
        for card in current_equivalence_class:
            local_hand=Hand(virtual_hands[game_params['turn']].cards)
            local_flop=Hand(virtual_hands[3].cards)
            _,new_turn=local_hand.play_card(card,game_params['turn'],local_flop)
            key_string=' '.join([hand.to_string() for hand in virtual_hands[:game_params['turn']]+[local_hand]+virtual_hands[game_params['turn']+1:-1]+[local_flop]])+f' {new_turn}'
            if key_string in solution and solution[key_string]['num_tricks'][game_params['player']]==optimal_num_tricks[game_params['player']]:
                for card in current_equivalence_class:
                    optimal_cards.append(card)
    highlight(optimal_cards,game_params['hands'][3].cards[0])
    canvas_west=tk.Canvas(root,width=CARD_STEP_X,height=CARD_STEP_Y*9+CARD_STEP_Y,bg=BACKGROUND_COLOR,bd=0,highlightthickness=0)
    west_info=canvas_west.create_text(CARD_STEP_X//1.3,CARD_STEP_Y*9//2+CARD_STEP_Y//2,angle=90,text=f"current/projected: 0/{optimal_num_tricks[1]}",fill="white",font=tkf.Font(family="Garamond",size=24),anchor='s',justify=tk.CENTER)
    canvas_west.place(relx=0.205,rely=0.47,anchor='center')
    canvas_east=tk.Canvas(root,width=CARD_STEP_X,height=CARD_STEP_Y*9+CARD_STEP_Y,bg=BACKGROUND_COLOR,bd=0,highlightthickness=0)
    east_info=canvas_east.create_text(CARD_STEP_X,CARD_STEP_Y*9//2+CARD_STEP_Y//2,angle=90,text=f"current/projected: 0/{optimal_num_tricks[2]}",fill="white",font=tkf.Font(family="Garamond",size=24),anchor='s',justify=tk.CENTER)
    canvas_east.place(relx=0.79,rely=0.47,anchor='center')
    canvas_south=tk.Canvas(root,width=CARD_STEP_Y*9+CARD_STEP_Y,height=CARD_STEP_X,bg=BACKGROUND_COLOR,bd=0,highlightthickness=0)
    south_info=canvas_south.create_text(CARD_STEP_Y*9//2+CARD_STEP_Y//2,CARD_STEP_X//1.3,angle=0,text=f"current/projected: 0/{optimal_num_tricks[0]}",fill="white",font=tkf.Font(family="Garamond",size=24),anchor='s',justify=tk.CENTER)
    canvas_south.place(relx=0.5,rely=0.68,anchor='center')
    hand_info_texts=[south_info,west_info,east_info]
    hand_info_canvases=[canvas_south,canvas_west,canvas_east]
    current_tricks=[0,0,0]

def erase_tricks(cards,flop):
    for trick_container in trick_containers:
        trick_container.config(image='')
    highlight(cards,flop)
    continue_button.destroy()

def solve():
    for widget in set_up_container.winfo_children():
        widget.destroy()
    set_up_container.destroy()
    global info_message_container,info_message,start_button,solution,classes,virtual_hands
    info_message_container=tk.Label(root,bd=0,font=tkf.Font(family="Garamond",size=44),fg='white',bg=BACKGROUND_COLOR)
    info_message=tk.StringVar(info_message_container,"Solution in progress...")
    info_message_container.config(textvariable=info_message)
    info_message_container.place(relx=0.5,rely=0.15,anchor='center')
    root.update()
    game_params['hands'],solution,info=solve_dp(game_params)
    virtual_hands=[Hand(hand.cards) for hand in game_params['hands']]
    classes=[equivalence_classes(hand) for hand in game_params['hands'][:3]]
    info_message_container.config(font=tkf.Font(family="Garamond",size=32))
    info_message.set(f"Solved {info['subgames']:,} subgames in {info['time']:.0f} sec(s).")
    start_button=tk.Button(root,text='START',borderwidth=0,bg='white',font=tkf.Font(family="Garamond",size=32),fg=BACKGROUND_COLOR,highlightthickness=0,command=play_setup)
    start_button.place(relx=0.5,rely=0.24,anchor='center')

def process_selection(param,val):
    if param=='type':
        for button in params_buttons[param].values():
            button.config(bg='white',fg=BACKGROUND_COLOR)
        params_buttons[param][val].config(bg='pink3',fg='white')
        if val=='M':
            process_selection('major_suit','-')
    if param=='player':
        for button in params_buttons[param].values():
            button.config(bg='white',fg=BACKGROUND_COLOR)
        params_buttons[param][val].config(bg='pink3',fg='white')
    if param=='turn':
        for button in params_buttons[param].values():
            button.config(bg='white',fg=BACKGROUND_COLOR)
        params_buttons[param][val].config(bg='pink3',fg='white')
    if param=='major_suit' and ('type' not in game_params or game_params['type']=='P'):
        for key,button in params_buttons[param].items():
            if key!='-':
                button.config(bg='white',image=suit_imgs[key])
            else:
                button.config(bg='white',fg=BACKGROUND_COLOR)
        if val!='-':
            params_buttons[param][val].config(bg='pink3',image=suit_imgs[f'{val}-white'])
        else:
            params_buttons[param][val].config(bg='pink3',fg='white')
    game_params[param]=val
    if 'type' in game_params and 'major_suit' in game_params and 'player' in game_params and 'turn' in game_params:
        accept_setup()

def type_setup():
    type_question_message=tk.Label(set_up_container,text="Contract type:",bd=0,bg=BACKGROUND_COLOR,font=tkf.Font(family="Garamond",size=34),fg='white')
    type_question_message.grid(row=0,columnspan=6,sticky=tk.W)
    button_play=MacButton(set_up_container,borderless=True,bg='white',text="PLAY",font=tkf.Font(family="Garamond",size=18),fg=BACKGROUND_COLOR,command=partial(process_selection,'type','P'))
    button_play.grid(row=1,column=0,columnspan=3,sticky=tk.NSEW)
    button_misere=MacButton(set_up_container,borderless=True,bg='white',text="MISERE",font=tkf.Font(family="Garamond",size=18),fg=BACKGROUND_COLOR,command=partial(process_selection,'type','M'))
    button_misere.grid(row=1,column=3,columnspan=3,sticky=tk.NSEW)
    params_buttons['type']={'P':button_play,'M':button_misere}

def player_setup():
    player_question_message=tk.Label(set_up_container,text="Playing hand:",bd=0,bg=BACKGROUND_COLOR,font=tkf.Font(family="Garamond",size=34),fg='white')
    player_question_message.grid(row=2,columnspan=6,sticky=tk.W)
    button_south=MacButton(set_up_container,borderless=True,bg='white',text="SOUTH",font=tkf.Font(family="Garamond",size=18),fg=BACKGROUND_COLOR,command=partial(process_selection,'player',0))
    button_south.grid(row=3,column=0,columnspan=2,sticky=tk.NSEW)
    button_west=MacButton(set_up_container,borderless=True,bg='white',text="WEST",font=tkf.Font(family="Garamond",size=18),fg=BACKGROUND_COLOR,command=partial(process_selection,'player',1))
    button_west.grid(row=3,column=2,columnspan=2,sticky=tk.NSEW)
    button_east=MacButton(set_up_container,borderless=True,bg='white',text="EAST",font=tkf.Font(family="Garamond",size=18),fg=BACKGROUND_COLOR,command=partial(process_selection,'player',2))
    button_east.grid(row=3,column=4,columnspan=2,sticky=tk.NSEW)
    params_buttons['player']={0:button_south,1:button_west,2:button_east}

def turn_setup():
    turn_question_message=tk.Label(set_up_container,text="Short hand:",bd=0,bg=BACKGROUND_COLOR,font=tkf.Font(family="Garamond",size=34),fg='white')
    turn_question_message.grid(row=4,columnspan=6,sticky=tk.W)
    button_south=MacButton(set_up_container,borderless=True,bg='white',text="SOUTH",font=tkf.Font(family="Garamond",size=18),fg=BACKGROUND_COLOR,command=partial(process_selection,'turn',0))
    button_south.grid(row=5,columnspan=2,column=0,sticky=tk.NSEW)
    button_west=MacButton(set_up_container,borderless=True,bg='white',text="WEST",font=tkf.Font(family="Garamond",size=18),fg=BACKGROUND_COLOR,command=partial(process_selection,'turn',1))
    button_west.grid(row=5,columnspan=2,column=2,sticky=tk.NSEW)
    button_east=MacButton(set_up_container,borderless=True,bg='white',text="EAST",font=tkf.Font(family="Garamond",size=18),fg=BACKGROUND_COLOR,command=partial(process_selection,'turn',2))
    button_east.grid(row=5,columnspan=2,column=4,sticky=tk.NSEW)
    params_buttons['turn']={0:button_south,1:button_west,2:button_east}

def major_suit_setup():
    major_suit_question_message=tk.Label(set_up_container,text="Major suit:",bd=0,bg=BACKGROUND_COLOR,font=tkf.Font(family="Garamond",size=34),fg='white')
    major_suit_question_message.grid(row=6,columnspan=6,sticky=tk.W)
    button_spades=MacButton(set_up_container,borderless=True,bg='white',image=suit_imgs['S'],font=tkf.Font(family="Garamond",size=18),fg=BACKGROUND_COLOR,command=partial(process_selection,'major_suit','S'))
    button_spades.grid(row=7,column=0,sticky=tk.NSEW)
    button_clubs=MacButton(set_up_container,borderless=True,bg='white',image=suit_imgs['C'],font=tkf.Font(family="Garamond",size=18),fg=BACKGROUND_COLOR,command=partial(process_selection,'major_suit','C'))
    button_clubs.grid(row=7,column=1,sticky=tk.NSEW)
    button_diamonds=MacButton(set_up_container,borderless=True,bg='white',image=suit_imgs['D'],font=tkf.Font(family="Garamond",size=18),fg=BACKGROUND_COLOR,command=partial(process_selection,'major_suit','D'))
    button_diamonds.grid(row=7,column=2,sticky=tk.NSEW)
    button_hearts=MacButton(set_up_container,borderless=True,bg='white',image=suit_imgs['H'],font=tkf.Font(family="Garamond",size=18),fg=BACKGROUND_COLOR,command=partial(process_selection,'major_suit','H'))
    button_hearts.grid(row=7,column=3,sticky=tk.NSEW)
    button_none=MacButton(set_up_container,borderless=True,bg='white',text="NONE",font=tkf.Font(family="Garamond",size=18),fg=BACKGROUND_COLOR,command=partial(process_selection,'major_suit','-'))
    button_none.grid(row=7,column=4,columnspan=2,sticky=tk.NSEW)
    params_buttons['major_suit']={'S':button_spades,'C':button_clubs,'D':button_diamonds,'H':button_hearts,'-':button_none}

def accept_setup():
    params_buttons['blank']=tk.Frame(set_up_container,bd=0,height=Y_SIZE//20,width=X_SIZE//2.5,bg=BACKGROUND_COLOR)
    params_buttons['blank'].grid(row=8,column=0,columnspan=6,sticky=tk.W)
    params_buttons['ok']=MacButton(set_up_container,highlightbackground='white',highlightthickness=3,bd=0,bg='grey40',text="OK",font=tkf.Font(family="Garamond",size=18),fg='white',command=solve)
    params_buttons['ok'].grid(row=9,column=2,columnspan=2,sticky=tk.NSEW)

root=tk.Tk()
root.geometry(f"{X_SIZE}x{Y_SIZE}")
root.configure(background=BACKGROUND_COLOR)
root.title("Preferans solver")
deal_message=tk.StringVar(root,"Select 10 cards for SOUTH")
deal_message_container=tk.Label(root,textvariable=deal_message,bd=0,font=tkf.Font(family="Garamond",size=44),fg='white',bg=BACKGROUND_COLOR)
deal_message_container.place(relx=0.5,rely=0.1,anchor='center')
deal_cards_container=tk.Frame(root,bg=BACKGROUND_COLOR,bd=0,height=2.16*CARD_Y_SIZE,width=15*CARD_STEP_X/1.5+2.05*CARD_X_SIZE)
deal_cards_container.place(relx=0.5,rely=0.4,anchor='center')
south=tk.Frame(root,bg=BACKGROUND_COLOR,bd=0,height=1.4*CARD_Y_SIZE+2*BORDER_THICKNESS,width=9*CARD_STEP_X+CARD_X_SIZE+2*BORDER_THICKNESS)
south.place(relx=0.5,rely=0.83,anchor='center')
south_cards_container=tk.Frame(south,bg=BACKGROUND_COLOR,highlightbackground='white',highlightthickness=BORDER_THICKNESS,height=CARD_Y_SIZE+2*BORDER_THICKNESS,width=9*CARD_STEP_X+CARD_X_SIZE+2*BORDER_THICKNESS)
south_cards_container.place(x=0,y=0)
south_message=tk.StringVar(south,"SOUTH")
south_message_container=tk.Label(south,textvariable=south_message,bd=0,font=tkf.Font(family="Garamond",size=22),fg='white',bg=BACKGROUND_COLOR)
south_message_container.place(relx=0.5,rely=0.86,anchor='center')
west=tk.Frame(root,bg=BACKGROUND_COLOR,bd=0,height=9*CARD_STEP_Y+CARD_Y_SIZE+2*BORDER_THICKNESS+0.3*CARD_Y_SIZE,width=CARD_X_SIZE+2*BORDER_THICKNESS)
west.place(relx=0.14,rely=0.49,anchor='center')
west_cards_container=tk.Frame(west,bg=BACKGROUND_COLOR,highlightbackground='white',highlightthickness=BORDER_THICKNESS,height=9*CARD_STEP_Y+CARD_Y_SIZE+2*BORDER_THICKNESS,width=CARD_X_SIZE+2*BORDER_THICKNESS)
west_cards_container.place(x=0,y=0)
west_message=tk.StringVar(west,"WEST")
west_message_container=tk.Label(west,textvariable=west_message,bd=0,font=tkf.Font(family="Garamond",size=22),fg='white',bg=BACKGROUND_COLOR)
west_message_container.place(relx=0.5,rely=0.975,anchor='center')
east=tk.Frame(root,bg=BACKGROUND_COLOR,bd=0,height=9*CARD_STEP_Y+CARD_Y_SIZE+2*BORDER_THICKNESS+0.3*CARD_Y_SIZE,width=CARD_X_SIZE+2*BORDER_THICKNESS)
east.place(relx=0.86,rely=0.49,anchor='center')
east_cards_container=tk.Frame(east,bg=BACKGROUND_COLOR,highlightbackground='white',highlightthickness=BORDER_THICKNESS,height=9*CARD_STEP_Y+CARD_Y_SIZE+2*BORDER_THICKNESS,width=CARD_X_SIZE+2*BORDER_THICKNESS)
east_cards_container.place(relx=0,rely=0)
east_message=tk.StringVar(east,"EAST")
east_message_container=tk.Label(east,textvariable=east_message,bd=0,font=tkf.Font(family="Garamond",size=22),fg='white',bg=BACKGROUND_COLOR)
east_message_container.place(relx=0.5,rely=0.975,anchor='center')
raw_images={card.to_string:Image.open(IMG_DIR+f"/{card.to_string.replace(':','')}.png") for key,card in CARDS.items() if '-' not in key}
images={key:ImageTk.PhotoImage(img.resize((CARD_X_SIZE,CARD_Y_SIZE),Image.ANTIALIAS)) for key,img in raw_images.items()}
raw_images_inactive={card.to_string:Image.open(IMG_DIR_INACTIVE+f"/{card.to_string.replace(':','')}.png") for key,card in CARDS.items() if '-' not in key}
images_inactive={key:ImageTk.PhotoImage(img.resize((CARD_X_SIZE,CARD_Y_SIZE),Image.ANTIALIAS)) for key,img in raw_images_inactive.items()}
raw_images_optimal={card.to_string:Image.open(IMG_DIR_OPTIMAL+f"/{card.to_string.replace(':','')}.png") for key,card in CARDS.items() if '-' not in key}
images_optimal={key:ImageTk.PhotoImage(img.resize((CARD_X_SIZE,CARD_Y_SIZE),Image.ANTIALIAS)) for key,img in raw_images_optimal.items()}
buttons={key:tk.Button(deal_cards_container,image=image,borderwidth=0,bg=BACKGROUND_COLOR,highlightthickness=0,pady=0,padx=0) for key,image in images.items()}
for i,(key,button) in enumerate(buttons.items()):
    button.config(command=partial(deal_card,key))
    button.place(x=(CARD_STEP_X/1.5)*(i%16)+CARD_X_SIZE*(i%16>7),y=(1.15*CARD_Y_SIZE)*(i>=16))
button_random=MacButton(root,text='RANDOM',font=tkf.Font(family="Garamond",size=22),fg=BACKGROUND_COLOR,borderless=True,bg='white',highlightthickness=0,pady=0,padx=0,command=random_deal)
button_random.place(relx=0.5,rely=0.4+1.1*CARD_Y_SIZE/Y_SIZE+0.05,anchor='center')
south_buttons,west_buttons,east_buttons=dict(),dict(),dict()
root.mainloop()