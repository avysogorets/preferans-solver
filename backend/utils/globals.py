import platform
import itertools
from backend.card import Card

if platform.system() == "Darwin":
    MESSAGE_FONT=24
else:
    MESSAGE_FONT=18
X_SIZE,Y_SIZE=960,640
CARD_X_SIZE=X_SIZE//12
CARD_Y_SIZE=CARD_X_SIZE*890//634
CARD_STEP_X=CARD_X_SIZE//2.5
CARD_STEP_Y=CARD_Y_SIZE//2.8
BACKGROUND_COLOR='maroon'
PLAYER_X_SIZE=50
PLAYER_Y_SIZE=30
BORDER_THICKNESS=CARD_X_SIZE//30
IMG_DIR='frontend/images/card_imgs_normal'
IMG_DIR_DISABLED='frontend/images/card_imgs_disabled'
IMG_DIR_OPTIMAL='frontend/images/card_imgs_optimal'
IMG_DIR_UTILS='frontend/images/card_utils'
IMG_INFO='frontend/images/info.png'

CARDS=[]
for card in itertools.product(*[range(4),range(8)]):
    suit,kind = card[0], card[1]
    CARDS.append(Card(suit,kind))
SOUTH,WEST,EAST,TRICK = 0,1,2,3
SPADES,DIAMONDS,CLUBS,HEARTS = 0,1,2,3
TRICK_1,TRICK_2,TRICK_3 = 3,4,5