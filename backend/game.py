from backend.hand import Hand
from backend.utils.globals import *
from backend.utils.utils import settle_trick, adjust_left
from copy import deepcopy

class Game(object):

    def __init__(self,type=None,turn=None,player=None,trumps=None):
        self.past_tricks=[0,0,0]
        self.future_tricks=None
        self.hands=[Hand([]),Hand([]),Hand([])]
        self.hands.append(Hand([],trick_flag=True,auto_flush=False))
        self.params={'type':type,
                'turn':turn,
                'player':player,
                'trumps':trumps}
        
    def initialize(self):
        if self.params['trumps']!='-' and self.params['trumps'] is not None:
            self.suits = {(i+self.params['trumps'])%4: i for i in range(4)}
        else:
            self.suits = {i: i for i in range(4)}
        self.players = {(i+self.params['player'])%3: i for i in range(3)}
        self.players_reverse = {val:key for val,key in self.players.items()}
        self.trumps = 0 if self.params['trumps']!='-' else None

    def copy(self):
        new_game = Game(self.params['type'],
                self.params['turn'],
                self.params['player'],
                self.params['trumps'])
        new_game.hands=[Hand(hand.cards) for hand in self.hands[:TRICK]]
        new_game.hands.append(Hand(self.hands[TRICK].cards,
                             trick_flag=True,
                             auto_flush=False))
        new_game.past_tricks=deepcopy(self.past_tricks)
        new_game.future_tricks=deepcopy(self.future_tricks)
        return new_game

    def play_card(self,card):
        assert len(self.hands[TRICK].cards)<3
        assert card in self.hands[self.params['turn']].cards
        new_tricks,new_turn=self.hands[self.params['turn']].play_card(card,
                self.params['turn'],
                self.hands[TRICK],
                self.params['trumps'])
        self.params['turn']=new_turn
        return new_tricks

    def flush(self):
        assert len(self.hands[TRICK].cards)==3
        num_tricks=[0,0,0]
        trick_order=[(self.params['turn']-2)%3,
                (self.params['turn']-1)%3,
                self.params['turn']] 
        winner=trick_order[settle_trick(self.hands[TRICK].cards,
                self.params['trumps'])]
        num_tricks[winner]+=1
        self.params['turn']=winner
        self.hands[TRICK].cards=[]
        self.hands[TRICK].cards=[]
        return num_tricks

    def to_string(self):
        """ A string describing the current subgame.
        Player assignments:
            0 - player in the game;
            1 - short hand (following the player cw);
            2 - long hand (following the short hand cw).
        Suit assignments:
            - trump suit is listed first (spades if N/A);
            - other suits follow trumps in order (cw) 
        Note that non-trump suits in this representation
        are distinguishable as they follow this order!
        """
        suit_strings = {suit:'' for suit in self.suits.values()}
        for card in CARDS:
            for player,i in self.players.items():
                if card in self.hands[player].cards:
                    suit_strings[self.suits[card.suit]]+=str(i)
            if card in self.hands[TRICK].cards:
                if self.hands[TRICK].cards[0]==card:
                    suit_strings[self.suits[card.suit]]+='3'
                else:
                    suit_strings[self.suits[card.suit]]+='4'
        turn=self.params['turn']
        if len(self.hands[TRICK].cards)==2:
            suit_strings=adjust_left(suit_strings,'3',str((self.players[turn]-2)%3))
            suit_strings=adjust_left(suit_strings,'4',str((self.players[turn]-1)%3))
        if len(self.hands[TRICK].cards)==1:
            suit_strings=adjust_left(suit_strings,'3',str((self.players[turn]-1)%3))
        suits_string = ' '.join(suit_strings.values())
        # in order distinguish cases when trumps is none or spades
        if self.params['trumps'] in [SPADES,DIAMONDS,CLUBS,HEARTS]:
            trumps_indicator = '1'
        else:
            trumps_indicator = '0'
        turn = str(self.players[self.params['turn']])
        game_string = '.'.join([suits_string, turn, self.params['type'], trumps_indicator])
        return game_string