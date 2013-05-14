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

markerTypes = { 
    'exposed': ("Exposed marker", "0183c0b8-6a6d-42c5-bedb-94bbc8ca5329"),
    'baffled': ("Baffled marker", "0415bae0-0c88-4ec6-8169-aeb117318618")
	}

def expose(card, x = 0, y = 0):
    mute()
    if card.markers[markerTypes['exposed']] == 0:
        notify("{} becomes Exposed.".format(card))
        card.markers[markerTypes['exposed']] = 1
    else:
        notify("{} is not Exposed anymore.".format(card))
        card.markers[markerTypes['exposed']] = 0


def baffle(card, x = 0, y = 0):
    mute()
    if card.markers[markerTypes['baffled']] == 0:
       notify("{} becomes Baffled and is considered Exposed until the end of the mission.".format(card))
       card.markers[markerTypes['exposed']] += 1
       card.markers[markerTypes['baffled']] += 1
    else:
       notify("{} is not baffled anymore.".format(card))
       card.markers[markerTypes['exposed']] -= 1
       card.markers[markerTypes['baffled']] -= 1

AbilityColor = "#FF0000"

def ability(card, x = 0, y = 0):
    mute()
    card.highlight = AbilityColor
    notify('{} activates the ability on {}'.format(me, card))

def download_o8c(group,x=0,y=0):
   openUrl("http://dbzer0.com/pub/SpycraftCCG/sets/SpycraftCCG-Sets-Bundle.o8c")
    