def roll6(group, x = 0, y = 0):
    mute()
    n = rnd(1, 6)
    notify("{} rolls {} on a 6-sided die.".format(me, n))

def draw(group, x = 0, y = 0):
    if len(group) == 0: return
    mute()
    group[0].moveTo(me.hand)
    notify("{} draws a card.".format(me))

def drawMany(group, count = None):
    if len(group) == 0: return
    mute()
    if count == None: count = askInteger("Draw how many cards?", 7)
    for c in group.top(count): c.moveTo(me.hand)
    notify("{} draws {} cards.".format(me, count))
def shuffle(group, x = 0, y = 0):
    group.shuffle()

def play(card, x = 0, y = 0):
    mute()
    src = card.group
    card.moveToTable(0, 90)
    card.isFaceUp = False
    notify("{} plays a card face-down from his hand.".format(me))

def retire(card, x = 0, y = 0):
    mute()
    src = card.group
    card.moveTo(me.Discard)
    notify("{} retires {}.".format(me, card))

def shuffleIntoDeck(group = me.Discard):
    mute()
    Deck = me.Deck
    for c in group: c.moveTo(Deck)
    random = rnd(100, 1000)
    Deck.shuffle()
    notify("{} shuffles his {} into his Deck.".format(me, group.name))

def act(card, x = 0, y = 0):
    mute()
    if card.isFaceUp:
        notify("{} Deactivates {}".format(me, card))
        card.isFaceUp = False
    else:
        card.isFaceUp = True
        notify("{} Activates {}".format(me, card))

def wound(card, x = 0, y = 0):
    mute()
    card.orientation ^= Rot90
    if card.orientation & Rot90 == Rot90:
        notify('{} is wounded.'.format(card))
    else:
        notify('{} is unwounded.'.format(card))

def clear(card, x = 0, y = 0):
    notify("{} clears {}.".format(me, card))
    card.highlight = None
    card.target(False)