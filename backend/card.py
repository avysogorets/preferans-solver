class Card:
    def __init__(self,suit,kind):
        self.suit=suit
        self.kind=kind
        self.highlight='normal'
        self.to_string='_'.join([str(suit),str(kind)])
    def __lt__(self,other):
        return (self.suit,self.kind)<(other.suit,other.kind)