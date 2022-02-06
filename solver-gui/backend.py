import time

SUITS_TO_READ={0:'S',1:'C',2:'D',3:'H',None:'-'}
KINDS_TO_READ={0:'7',1:'8',2:'9',3:'10',4:'J',5:'Q',6:'K',7:'A',None:'-'}
SUITS_TO_CODE={'S':0,'C':1,'D':2,'H':3,'-':None}
KINDS_TO_CODE={'7':0,'8':1,'9':2,'10':3,'J':4,'Q':5,'K':6,'A':7,'-':None}

class Card(object):
    def __init__(self,suit,kind):
        self.suit=SUITS_TO_CODE[suit]
        self.kind=KINDS_TO_CODE[kind]
        self.to_string=':'.join([SUITS_TO_READ[self.suit],KINDS_TO_READ[self.kind]])
    def __lt__(self,other):
        return (self.suit,self.kind)<(other.suit,other.kind)
    def __gt__(self,other):
        return (self.suit,self.kind)>(other.suit,other.kind)

CARDS=dict()
for suit in SUITS_TO_CODE.keys():
    for kind in KINDS_TO_CODE.keys():
        CARDS[(suit,kind)]=Card(suit,kind)

def settle_trick(cards,major_suit):
    if cards[0].suit==major_suit:
        if cards[1].suit!=major_suit and cards[2].suit!=major_suit:
            return 0
        if cards[1].suit!=major_suit and cards[2].suit==major_suit:
            return 0 if cards[0].kind>cards[2].kind else 2
        if cards[1].suit==major_suit and cards[2].suit!=major_suit:
            return 0 if cards[0].kind>cards[1].kind else 1
        if cards[1].suit==major_suit and cards[2].suit==major_suit:
            if cards[0].kind>cards[1].kind and cards[0].kind>cards[2].kind:
                return 0
            if cards[1].kind>cards[0].kind and cards[1].kind>cards[2].kind:
                return 1
            if cards[2].kind>cards[0].kind and cards[2].kind>cards[1].kind:
                return 2
    if cards[0].suit!=major_suit:
        if cards[1].suit==major_suit and cards[2].suit==major_suit:
            return 1 if cards[1].kind>cards[2].kind else 2
        if cards[1].suit==major_suit and cards[2].suit!=major_suit:
            return 1
        if cards[1].suit!=major_suit and cards[2].suit==major_suit:
            return 2
        if cards[1].suit!=major_suit and cards[2].suit!=major_suit:
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
    card=solution[key_string]['card']
    turn=solution[key_string]['turn']
    _,_=hands[turn].play_card(CARDS[tuple(card.split(':'))],turn,hands[3])

class Hand(object):
    def __init__(self,cards):
        self.cards=[card for card in cards]
    def remove(self,other_card):
        for i,card in enumerate(self.cards):
            if card.suit==other_card.suit and card.kind==other_card.kind:
                self.cards=self.cards[:i]+self.cards[i+1:]
    def play_card(self,card,turn,flop):
        tricks=[0,0,0]
        self.remove(card)
        if flop.cards[-1].suit is not None:
            trick_order=[(turn-2)%3,(turn-1)%3,turn]                  
            winner=trick_order[settle_trick(flop.cards+[card],game_params['major_suit'])]
            tricks[winner]+=1
            new_turn=winner
            flop.cards[0]=CARDS[('-','-')]
            flop.cards[1]=CARDS[('-','-')]
        elif flop.cards[-2].suit is not None:                              
            new_turn=(turn+1)%3
            flop.cards[1]=card
        else:        
            new_turn=(turn+1)%3
            flop.cards[0]=card
        return tricks,new_turn
    def options(self,other_card,all=False):
        options=[]
        if other_card.suit is None:
            for i in range(len(self.cards)):
                if all or not (i<len(self.cards)-1 and self.cards[i].suit==self.cards[i+1].suit and abs(self.cards[i].kind-self.cards[i+1].kind)==1):
                    options.append(self.cards[i])
        if other_card.suit is not None:
            for i in range(len(self.cards)):
                if (all or not (i<len(self.cards)-1 and self.cards[i].suit==self.cards[i+1].suit and abs(self.cards[i].kind-self.cards[i+1].kind)==1)) and other_card.suit==self.cards[i].suit:
                    options.append(self.cards[i])
        if len(options)==0:
            for i in range(len(self.cards)):
                if (all or not (i<len(self.cards)-1 and self.cards[i].suit==self.cards[i+1].suit and abs(self.cards[i].kind-self.cards[i+1].kind)==1)) and game_params['major_suit']==self.cards[i].suit:
                    options.append(self.cards[i])
        if len(options)==0:
            for i in range(len(self.cards)):
                if all or not (i<len(self.cards)-1 and self.cards[i].suit==self.cards[i+1].suit and abs(self.cards[i].kind-self.cards[i+1].kind)==1):
                    options.append(self.cards[i])
        return options
    def sort_cards(self):
        self.cards=sorted(self.cards,key=lambda x: (x.suit,x.kind),reverse=game_params['type']=='M')
    def to_string(self):
        return ' '.join([card.to_string for card in self.cards])

def solver(hands,turn):
    hand_strings=[hand.to_string() for hand in hands]
    key_string=' '.join(hand_strings)+f' {turn}'
    if sum([len(hand.cards) for hand in hands[:3]])==0:
        dp[key_string]={'card':'-:-','turn':turn,'num_tricks':(0,0,0)}
    current_objective=-1
    for card in hands[turn].options(hands[3].cards[0]):
        virtual_hand=Hand(hands[turn].cards)
        virtual_flop=Hand(hands[3].cards)
        tricks,virtual_turn=virtual_hand.play_card(card,turn,virtual_flop)
        virtual_key_string=' '.join(hand_strings[:turn]+[virtual_hand.to_string()]+hand_strings[turn+1:-1]+[virtual_flop.to_string()])+f' {virtual_turn}'
        if virtual_key_string not in dp:
            virtual_hands=hands[:turn]+[virtual_hand]+hands[turn+1:-1]+[virtual_flop]
            solver(virtual_hands,virtual_turn)
        new_tricks=[future_tricks+trick for future_tricks,trick in zip(dp[virtual_key_string]['num_tricks'],tricks)]
        if game_params['type']=='P':
            if game_params['player']==turn and ((hands[3].cards[0].suit is not None and current_objective<new_tricks[game_params['player']]) or (hands[3].cards[0].suit is None and current_objective<=new_tricks[game_params['player']])):
                current_objective=new_tricks[game_params['player']]
                dp[key_string]={'card':card.to_string,'turn':turn,'num_tricks':new_tricks}
            if game_params['player']!=turn and ((hands[3].cards[0].suit is not None and current_objective<100-new_tricks[game_params['player']]) or (hands[3].cards[0].suit is None and current_objective<=100-new_tricks[game_params['player']])):
                current_objective=100-new_tricks[game_params['player']]
                dp[key_string]={'card':card.to_string,'turn':turn,'num_tricks':new_tricks}
        if game_params['type']=='M':
            if game_params['player']==turn and ((hands[3].cards[0].suit is not None and current_objective<100-new_tricks[game_params['player']]) or (hands[3].cards[0].suit is None and current_objective<=100-new_tricks[game_params['player']])):
                current_objective=100-new_tricks[game_params['player']]
                dp[key_string]={'card':card.to_string,'turn':turn,'num_tricks':new_tricks}
            if game_params['player']!=turn and ((hands[3].cards[0].suit is not None and current_objective<new_tricks[game_params['player']]) or (hands[3].cards[0].suit is None and current_objective<=new_tricks[game_params['player']])):
                current_objective=new_tricks[game_params['player']]
                dp[key_string]={'card':card.to_string,'turn':turn,'num_tricks':new_tricks}

def solve_dp(params):
    global dp,game_params
    dp,game_params=dict(),params
    hands=[Hand([CARDS[tuple(card.split(':'))] for card in game_params['hands'][i]]) for i in range(3)]
    game_params['major_suit']=SUITS_TO_CODE[game_params['major_suit']]
    hands.append(Hand([CARDS[('-','-')],CARDS[('-','-')]]))
    for hand in hands:
        hand.sort_cards()
    start_time=time.time()
    solver(hands,game_params['turn'])
    return hands,dp,{'subgames':len(dp),'time':time.time()-start_time}
