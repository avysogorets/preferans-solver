import time
from copy import deepcopy

SUITS_TO_READ={0:'S',1:'D',2:'C',3:'H'}
KINDS_TO_READ={0:'7',1:'8',2:'9',3:'10',4:'J',5:'Q',6:'K',7:'A'}
SUITS_TO_CODE={'S':0,'D':1,'C':2,'H':3}
KINDS_TO_CODE={'7':0,'8':1,'9':2,'10':3,'J':4,'Q':5,'K':6,'A':7}
SOUTH,WEST,EAST,TRICK=0,1,2,3

class Card:
    def __init__(self,suit,kind):
        self.suit=SUITS_TO_CODE[suit]
        self.kind=KINDS_TO_CODE[kind]
        self.highlight='normal'
        self.to_string='_'.join([SUITS_TO_READ[self.suit],KINDS_TO_READ[self.kind]])
    def __lt__(self,other):
        return (self.suit,self.kind)<(other.suit,other.kind)
    def __gt__(self,other):
        return (self.suit,self.kind)>(other.suit,other.kind)

CARDS=dict()
for suit in ['S','D','C','H']:
    for kind in ['7','8','9','10','J','Q','K','A']:
        CARDS['_'.join([suit,kind])]=Card(suit,kind)

def settle_trick(cards,trumps):
    if cards[0].suit==trumps:
        if cards[1].suit!=trumps and cards[2].suit!=trumps:
            return 0
        if cards[1].suit!=trumps and cards[2].suit==trumps:
            return 0 if cards[0].kind>cards[2].kind else 2
        if cards[1].suit==trumps and cards[2].suit!=trumps:
            return 0 if cards[0].kind>cards[1].kind else 1
        if cards[1].suit==trumps and cards[2].suit==trumps:
            if cards[0].kind>cards[1].kind and cards[0].kind>cards[2].kind:
                return 0
            if cards[1].kind>cards[0].kind and cards[1].kind>cards[2].kind:
                return 1
            if cards[2].kind>cards[0].kind and cards[2].kind>cards[1].kind:
                return 2
    if cards[0].suit!=trumps:
        if cards[1].suit==trumps and cards[2].suit==trumps:
            return 1 if cards[1].kind>cards[2].kind else 2
        if cards[1].suit==trumps and cards[2].suit!=trumps:
            return 1
        if cards[1].suit!=trumps and cards[2].suit==trumps:
            return 2
        if cards[1].suit!=trumps and cards[2].suit!=trumps:
            if cards[1].suit==cards[0].suit and cards[2].suit==cards[0].suit:
                if cards[0].kind>cards[1].kind and cards[0].kind>cards[2].kind:
                    return 0
                if cards[1].kind>cards[0].kind and cards[1].kind>cards[2].kind:
                    return 1
                if cards[2].kind>cards[0].kind and cards[2].kind>cards[1].kind:
                    return 2
            if cards[1].suit==cards[0].suit and cards[2].suit!=cards[0].suit:
                return 0 if cards[0].kind>cards[1].kind else 1
            if cards[1].suit!=cards[0].suit and cards[2].suit==cards[0].suit:
                return 0 if cards[0].kind>cards[2].kind else 2
            if cards[1].suit!=cards[0].suit and cards[2].suit!=cards[0].suit:
                return 0

def execute_turn(hands,turn,solution):
    key_string=' '.join([hand.to_string() for hand in hands])+f' {turn}' 
    card_key=solution[key_string]['card']
    turn=solution[key_string]['turn']
    _,_=hands[turn].play_card(CARDS[card_key],turn,hands[3])

class Game(object):
    def __init__(self,game=None):
        self.hands={'real':{},'virtual':{}}
        self.past_tricks=[0,0,0]
        self.future_tricks=None
        if game is None:
            for mode in ['real','virtual']:
                for player in [SOUTH,WEST,EAST]:
                    self.hands[mode][player]=Hand([])
                self.hands[mode][TRICK]=Hand([],trick_flag=True,auto_flush=False)
                self.params={'type':None,'turn':None,'player':None,'trumps':None}
                self.past_tricks=[0,0,0]
                self.future_tricks=None
        else:
            for mode in ['real','virtual']:
                for player in [SOUTH,WEST,EAST]:
                    self.hands[mode][player]=Hand(game.hands[mode][player].cards)
                self.hands[mode][TRICK]=Hand(game.hands[mode][TRICK].cards,trick_flag=True,auto_flush=False)
                self.params=deepcopy(game.params)
                self.past_tricks=deepcopy(game.past_tricks)
                self.future_tricks=deepcopy(game.future_tricks)
    def play_card(self,cards):
        new_tricks={'real':None,'virtual':None}
        for mode in ['real','virtual']:
            assert len(self.hands[mode][TRICK].cards)<3
            assert cards[mode] in self.hands[mode][self.params['turn']].cards
            assert cards[mode] in self.hands[mode][self.params['turn']].options(self.hands[mode][TRICK],all=True)
            new_tricks[mode],new_turn=self.hands[mode][self.params['turn']].play_card(cards[mode],self.params['turn'],self.hands[mode][TRICK])
        self.params['turn']=new_turn
        assert new_tricks['real']==new_tricks['virtual']
        return new_tricks['real']
    def flush(self):
        assert len(self.hands['real'][TRICK].cards)==3
        num_tricks=[0,0,0]
        trick_order=[(self.params['turn']-2)%3,(self.params['turn']-1)%3,self.params['turn']] 
        winner=trick_order[settle_trick(self.hands['real'][TRICK].cards,game_params['trumps'])]
        num_tricks[winner]+=1
        self.params['turn']=winner
        self.hands['real'][TRICK].cards=[]
        self.hands['virtual'][TRICK].cards=[]
        return num_tricks
    def to_string(self,mode='virtual'):
        return ', '.join([self.hands[mode][hand_key].to_string() for hand_key in [SOUTH,WEST,EAST]]+[f'{self.params["turn"]}']+[self.hands[mode][TRICK].to_string()])

class Hand(object):
    def __init__(self,cards,trick_flag=False,auto_flush=True):
        self.cards=[card for card in cards]
        self.trick_flag=trick_flag
        self.auto_flush=auto_flush
        self.highlight=False
        if not self.trick_flag:
            self.cards=sorted(self.cards)
    def add(self,card):
        assert len(self.cards)<10
        if card not in self.cards:
            self.cards.append(card)
        if not self.trick_flag:
            self.cards=sorted(self.cards)
    def remove(self,card):
        self.cards.remove(card)
    def play_card(self,card,turn,trick):
        assert len(trick.cards)<=3
        assert not self.trick_flag
        num_tricks=[0,0,0]
        self.remove(card)
        if len(trick.cards)==2:
            if trick.auto_flush:
                trick_order=[(turn-2)%3,(turn-1)%3,turn]                  
                winner=trick_order[settle_trick(trick.cards+[card],game_params['trumps'])]
                num_tricks[winner]+=1
                new_turn=winner
                trick.cards=[]
            else:
                trick.cards.append(card)
                new_turn=turn
        else:
            new_turn=(turn+1)%3
            trick.cards.append(card)
        return num_tricks,new_turn
    def options(self,trick,all=False):
        options=[]
        if len(trick.cards)==0:
            for i in range(len(self.cards)):
                if all or not (i<len(self.cards)-1 and self.cards[i].suit==self.cards[i+1].suit and abs(self.cards[i].kind-self.cards[i+1].kind)==1):
                    options.append(self.cards[i])
        if len(trick.cards)>0:
            for i in range(len(self.cards)):
                if (all or not (i<len(self.cards)-1 and self.cards[i].suit==self.cards[i+1].suit and abs(self.cards[i].kind-self.cards[i+1].kind)==1)) and trick.cards[0].suit==self.cards[i].suit:
                    options.append(self.cards[i])
        if len(options)==0:
            for i in range(len(self.cards)):
                if (all or not (i<len(self.cards)-1 and self.cards[i].suit==self.cards[i+1].suit and abs(self.cards[i].kind-self.cards[i+1].kind)==1)) and game_params['trumps']==self.cards[i].suit:
                    options.append(self.cards[i])
        if len(options)==0:
            for i in range(len(self.cards)):
                if all or not (i<len(self.cards)-1 and self.cards[i].suit==self.cards[i+1].suit and abs(self.cards[i].kind-self.cards[i+1].kind)==1):
                    options.append(self.cards[i])
        return options
    def to_string(self):
        return ' '.join([card.to_string for card in self.cards])

def solver(hands,turn):
    hand_strings=[hand.to_string() for hand in hands]
    key_string=', '.join(hand_strings[:3]+[f'{turn}']+[hand_strings[3]])
    if sum([len(hand.cards) for hand in hands[:3]])==0:
        dp[key_string]={'card':None,'turn':turn,'num_tricks':(0,0,0)}
    current_objective=-1
    for card in hands[turn].options(hands[3]):
        virtual_hand=Hand(hands[turn].cards)
        virtual_trick=Hand(hands[3].cards,trick_flag=True)
        tricks,virtual_turn=virtual_hand.play_card(card,turn,virtual_trick)
        virtual_key_string=', '.join(hand_strings[:turn]+[virtual_hand.to_string()]+hand_strings[turn+1:-1]+[f'{virtual_turn}']+[virtual_trick.to_string()])
        if virtual_key_string not in dp:
            virtual_hands=hands[:turn]+[virtual_hand]+hands[turn+1:-1]+[virtual_trick]
            solver(virtual_hands,virtual_turn)
        new_tricks=[future_tricks+trick for future_tricks,trick in zip(dp[virtual_key_string]['num_tricks'],tricks)]
        if game_params['type']=='P':
            if game_params['player']==turn and ((len(hands[3].cards)>0 and current_objective<new_tricks[game_params['player']]) or (len(hands[3].cards)==0 and current_objective<=new_tricks[game_params['player']])):
                current_objective=new_tricks[game_params['player']]
                dp[key_string]={'card':card.to_string,'turn':turn,'num_tricks':new_tricks}
            if game_params['player']!=turn and ((len(hands[3].cards)>0 and current_objective<100-new_tricks[game_params['player']]) or (len(hands[3].cards)==0 and current_objective<=100-new_tricks[game_params['player']])):
                current_objective=100-new_tricks[game_params['player']]
                dp[key_string]={'card':card.to_string,'turn':turn,'num_tricks':new_tricks}
        if game_params['type']=='M':
            if game_params['player']==turn and ((len(hands[3].cards)>0 and current_objective<100-new_tricks[game_params['player']]) or (len(hands[3].cards)==0 and current_objective<=100-new_tricks[game_params['player']])):
                current_objective=100-new_tricks[game_params['player']]
                dp[key_string]={'card':card.to_string,'turn':turn,'num_tricks':new_tricks}
            if game_params['player']!=turn and ((len(hands[3].cards)>0 and current_objective<new_tricks[game_params['player']]) or (len(hands[3].cards)==0 and current_objective<=new_tricks[game_params['player']])):
                current_objective=new_tricks[game_params['player']]
                dp[key_string]={'card':card.to_string,'turn':turn,'num_tricks':new_tricks}

def solve_dp(game):
    global dp,game_params
    dp,game_params=dict(),game.params
    hands=[game.hands['real'][hand_key] for hand_key in [SOUTH,WEST,EAST]]
    hands.append(Hand([],trick_flag=True))
    start_time=time.time()
    solver(hands,game_params['turn'])
    info={'subgames':len(dp),'time':time.time()-start_time}
    solution={'solution':dp,'info':info}
    return solution
