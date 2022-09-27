from backend.utils.globals import *

def settle_trick(cards,trumps):
    if cards[0].suit==trumps:
        if cards[1].suit==trumps:
            if cards[2].suit==trumps:
                return max([0,1,2],key=lambda i: cards[i])
            else:
                return max([0,1],key=lambda i: cards[i])
        else:
            if cards[2].suit==trumps:
                return max([0,2],key=lambda i: cards[i])
            else:
                return 0
    else:
        if cards[1].suit==trumps:
            if cards[2].suit==trumps:
                return max([1,2],key=lambda i: cards[i])
            else:
                return 1
        else:
            if cards[2].suit==trumps:
                return 2
            else:
                return settle_trick(cards,cards[0].suit)


def _settle_trick(suit_strings,suit_1,suit_2,suit_3,trumps):
    proxy_kind_1 = suit_strings[suit_1].index(str(TRICK_1))
    proxy_kind_2 = suit_strings[suit_2].index(str(TRICK_2))
    proxy_kind_3 = suit_strings[suit_3].index(str(TRICK_3))
    proxy_kinds = [proxy_kind_1, proxy_kind_2, proxy_kind_3]
    if suit_1==trumps:
        if suit_2==trumps:
            if suit_3==trumps:
                return max([0,1,2],key=lambda i: proxy_kinds[i])
            else:
                return max([0,1],key=lambda i: proxy_kinds[i])
        else:
            if suit_3==trumps:
                return max([0,2],key=lambda i: proxy_kinds[i])
            else:
                return 0
    else:
        if suit_2==trumps:
            if suit_3==trumps:
                return max([1,2],key=lambda i: proxy_kinds[i])
            else:
                return 1
        else:
            if suit_3==trumps:
                return 2
            else:
                return _settle_trick(suit_strings,suit_1,suit_2,suit_3,suit_1)


def adjust_left(suit_strings,to_adjust,player):
    for i,suit_string in enumerate(suit_strings.values()):
        if to_adjust in suit_string:
            suit_string=list(suit_string)
            idx=suit_string.index(to_adjust)
            while idx>0 and suit_string[idx-1]==player:
                suit_string[idx]=player
                suit_string[idx-1]=to_adjust
                idx=suit_string.index(to_adjust)
            suit_strings[i]=''.join(suit_string)
    return suit_strings


def options(game_string, trumps):
    suit_string, turn, type, trumps_indicator = game_string.split('.')
    suit_strings = suit_string.split(' ')
    trick_1_suit = None
    trick_2_suit = None
    for i,suit_str in enumerate(suit_strings):
        if str(TRICK_1) in suit_str:
            trick_1_suit = i
        if str(TRICK_2) in suit_str:
            trick_2_suit = i
    if trick_1_suit is not None and turn in suit_strings[trick_1_suit]:
        allowed_suits = [trick_1_suit]
    elif trumps is not None and trick_1_suit is not None and turn in suit_strings[trumps]:
        allowed_suits = [trumps]
    else:
        allowed_suits = [0,1,2,3]
    new_game_strings = []
    new_game_results = []
    if trick_2_suit is not None:
        next_trick_card = TRICK_3
    elif trick_1_suit is not None:
        next_trick_card = TRICK_2
    else:
        next_trick_card = TRICK_1
    for suit in allowed_suits:
        tokens = list(suit_strings[suit])
        new_block = True
        for j,token in enumerate(tokens):
            if new_block and token==turn:
                new_game_result = [0,0,0]
                new_suit_string = list(suit_strings[suit])
                new_suit_string[j] = str(next_trick_card)
                new_suit_string=''.join(new_suit_string)
                new_suit_strings = suit_string.split(' ')
                new_suit_strings[suit] = new_suit_string
                if next_trick_card==TRICK_3:
                    winner = _settle_trick(new_suit_strings,trick_1_suit,trick_2_suit,suit,trumps)
                    new_turn = (int(turn)+winner-2)%3
                    new_game_result[new_turn]+=1
                    new_suit_strings[trick_1_suit]=new_suit_strings[trick_1_suit].replace(str(TRICK_1),'')
                    new_suit_strings[trick_2_suit]=new_suit_strings[trick_2_suit].replace(str(TRICK_2),'')
                    new_suit_strings[suit]=new_suit_strings[suit].replace(str(TRICK_3),'')
                else:
                    new_turn = (int(turn)+1)%3
                new_suit_strings = ' '.join(new_suit_strings)
                new_game_string = '.'.join([new_suit_strings, str(new_turn), type, trumps_indicator])
                new_game_strings.append(new_game_string)
                new_game_results.append(new_game_result)
                new_block = False
            elif token!=turn:
                new_block = True
    return new_game_strings, new_game_results