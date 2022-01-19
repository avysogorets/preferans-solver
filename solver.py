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

def play(hands,turn):
    running_outcome=[0,0,0]
    key_string=' '.join([hand.to_string() for hand in hands])+f' {turn}'
    print(f"[Game: {'MISERE' if game_params['game_type']=='M' else 'PLAY'}]. Player {turn+1} to start; major suit {SUITS_TO_READ[game_params['major_suit']]}.")
    for i,hand in enumerate(hands[:3]):
        print(f"Hand #{i+1} [{'PASS' if i!=game_params['player'] else 'PLAY'}] {hand.to_string()}"+f" ({str(dp[key_string]['num_tricks'][i])})")   
    for round in range(10):
        card_1=dp[key_string]['card']
        turn_1=dp[key_string]['turn']
        _,turn=hands[turn].play_card(CARDS[tuple(card_1.split(':'))],turn,hands[3])
        key_string=' '.join([hand.to_string() for hand in hands])+f' {turn}'
        card_2=dp[key_string]['card']
        turn_2=dp[key_string]['turn']
        _,turn=hands[turn].play_card(CARDS[tuple(card_2.split(':'))],turn,hands[3])
        key_string=' '.join([hand.to_string() for hand in hands])+f' {turn}'
        card_3=dp[key_string]['card']
        turn_3=dp[key_string]['turn']
        winners,turn=hands[turn].play_card(CARDS[tuple(card_3.split(':'))],turn,hands[3])
        key_string=' '.join([hand.to_string() for hand in hands])+f' {turn}'
        running_outcome=[prev+curr for prev,curr in zip(running_outcome,winners)]
        hand_1='\033[1m'+f'{turn_1+1} {card_1+" " if "10" not in card_1 else card_1}'+'\033[0m' if winners[turn_1] else f'{turn_1+1} {card_1+" " if "10" not in card_1 else card_1}'
        hand_2='\033[1m'+f'{turn_2+1} {card_2+" " if "10" not in card_2 else card_2}'+'\033[0m' if winners[turn_2] else f'{turn_2+1} {card_2+" " if "10" not in card_2 else card_2}'
        hand_3='\033[1m'+f'{turn_3+1} {card_3+" " if "10" not in card_3 else card_3}'+'\033[0m' if winners[turn_3] else f'{turn_3+1} {card_3+" " if "10" not in card_3 else card_3}'
        print(f"[{'0' if round<9 else ''}{round+1}] [{hand_1}][{hand_2}][{hand_3}] -> {running_outcome}")

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
    def options(self,other_card):
        options=[]
        if other_card.suit is None:
            for i in range(len(self.cards)):
                if not (i<len(self.cards)-1 and self.cards[i].suit==self.cards[i+1].suit and abs(self.cards[i].kind-self.cards[i+1].kind)==1):
                    options.append(self.cards[i])
        if other_card.suit is not None:
            for i in range(len(self.cards)):
                if not (i<len(self.cards)-1 and self.cards[i].suit==self.cards[i+1].suit and abs(self.cards[i].kind-self.cards[i+1].kind)==1) and other_card.suit==self.cards[i].suit:
                    options.append(self.cards[i])
        if len(options)==0:
            for i in range(len(self.cards)):
                if not (i<len(self.cards)-1 and self.cards[i].suit==self.cards[i+1].suit and abs(self.cards[i].kind-self.cards[i+1].kind)==1) and game_params['major_suit']==self.cards[i].suit:
                    options.append(self.cards[i])
        if len(options)==0:
            for i in range(len(self.cards)):
                if not (i<len(self.cards)-1 and self.cards[i].suit==self.cards[i+1].suit and abs(self.cards[i].kind-self.cards[i+1].kind)==1):
                    options.append(self.cards[i])
        return options
    def sort_cards(self):
        self.cards=sorted(self.cards,key=lambda x: (x.suit,x.kind),reverse=game_params['game_type']=='M')
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
        if game_params['game_type']=='P':
            if game_params['player']==turn and ((hands[3].cards[0].suit is not None and current_objective<new_tricks[game_params['player']]) or (hands[3].cards[0].suit is None and current_objective<=new_tricks[game_params['player']])):
                current_objective=new_tricks[game_params['player']]
                dp[key_string]={'card':card.to_string,'turn':turn,'num_tricks':new_tricks}
            if game_params['player']!=turn and ((hands[3].cards[0].suit is not None and current_objective<100-new_tricks[game_params['player']]) or (hands[3].cards[0].suit is None and current_objective<=100-new_tricks[game_params['player']])):
                current_objective=100-new_tricks[game_params['player']]
                dp[key_string]={'card':card.to_string,'turn':turn,'num_tricks':new_tricks}
        if game_params['game_type']=='M':
            if game_params['player']==turn and ((hands[3].cards[0].suit is not None and current_objective<100-new_tricks[game_params['player']]) or (hands[3].cards[0].suit is None and current_objective<=100-new_tricks[game_params['player']])):
                current_objective=100-new_tricks[game_params['player']]
                dp[key_string]={'card':card.to_string,'turn':turn,'num_tricks':new_tricks}
            if game_params['player']!=turn and ((hands[3].cards[0].suit is not None and current_objective<new_tricks[game_params['player']]) or (hands[3].cards[0].suit is None and current_objective<=new_tricks[game_params['player']])):
                current_objective=new_tricks[game_params['player']]
                dp[key_string]={'card':card.to_string,'turn':turn,'num_tricks':new_tricks}

def main():
    accept_inputs=False
    global dp,game_params
    dp,game_params=dict(),dict()
    print('Welcome to Preference solver! Use S, C, D, H for spades, clubs, diamonds, and hearts, respectively.')
    while not accept_inputs:
        hands=[]
        hands.append(input('Enter cards for hand #1 (format SUIT:KIND) separated by the space key: ').upper()) # H:9 H:8 D:9 D:8 D:7 C:8 S:10 S:9 S:8 S:7
        hands.append(input('Enter cards for hand #2 (format SUIT:KIND) separated by the space key: ').upper()) # S:K S:A C:10 C:J C:Q D:A H:10 H:Q H:K H:A
        hands.append(input('Enter cards for hand #3 (format SUIT:KIND) separated by the space key: ').upper()) # S:J S:Q C:7 C:9 D:10 D:J D:Q D:K H:7 H:J
        game_params['game_type']=input('Indicate the game type (P for play or M for misere): ').upper() # M
        game_params['player']=input('Indicate the playing hand (1, 2, or 3): ') # 1
        turn=input('Indicate the short hand (1, 2, or 3): ') # 3
        game_params['major_suit']=input('Indicate the major suit (S, C, D, H, or -): ').upper() if game_params['game_type']!='M' else '-' # C # D
        try:
            hands=[Hand([CARDS[tuple(card.split(':'))] for card in hand.split(' ')]) for hand in hands]
            assert len(hands[0].cards)==len(hands[1].cards)
            assert len(hands[1].cards)==len(hands[2].cards)
            assert game_params['player'] in ['1','2','3']
            assert turn in ['1','2','3']
            assert game_params['major_suit'] in ['S','C','D','H','-']
            assert game_params['game_type'] in ['P','M']
            accept_inputs=True
            turn=int(turn)-1
            game_params['player']=int(game_params['player'])-1
            game_params['major_suit']=SUITS_TO_CODE[game_params['major_suit']]
            hands.append(Hand([CARDS[('-','-')],CARDS[('-','-')]]))
        except:
            print('Please check your inputs and try again.')
    print("Copy that! Wait while the problem is being solved; this may take a few minutes...")
    for i,hand in enumerate(hands):
        hand.sort_cards()
    start_time=time.time()
    solver(hands,turn)
    print('------------------------ BEGIN SOLUTION ------------------------')
    play(hands,turn)
    print(f'Processed {len(dp):,} subgames in {(time.time()-start_time)//60:.0f} minute(s) {(time.time()-start_time)%60:.0f} second(s).')
    print('------------------------- END SOLUTION -------------------------')

if __name__=="__main__":
    main()
