from backend.utils.utils import settle_trick

class Hand(object):

    def __init__(self,
                cards,
                trick_flag=False,
                auto_flush=True):
        # self.cards=cards is shallow copying!
        self.cards=list(cards)
        self.trick_flag=trick_flag
        self.auto_flush=auto_flush
        self.highlight=False

    def add(self,card):
        self.cards.append(card)

    def remove(self,card):
        self.cards.remove(card)

    def play_card(self,card,turn,trick,trumps):
        assert len(trick.cards)<=3
        assert not self.trick_flag
        num_tricks=[0,0,0]
        self.remove(card)
        if len(trick.cards)==2:
            if trick.auto_flush:
                trick_order=[(turn-2)%3,(turn-1)%3,turn]                  
                winner=settle_trick(trick.cards+[card],trumps)
                winner=trick_order[winner]
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

    def options(self,trick,trumps):
        options=[]
        if len(trick.cards)==0:
            return self.cards
        if len(trick.cards)>0:
            for card in self.cards:
                if trick.cards[0].suit==card.suit:
                    options.append(card)
        if len(options)==0:
            for card in self.cards:
                if trumps==card.suit:
                    options.append(card)
        if len(options)==0:
            return self.cards
        return options