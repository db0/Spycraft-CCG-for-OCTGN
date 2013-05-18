    # Python Scripts for the Spycraft CCG definition for OCTGN
    # Copyright (C) 2013  Konstantine Thoukydides and Lord Nat

    # This python script is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.

    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with this script.  If not, see <http://www.gnu.org/licenses/>.

#---------------------------------------------------------------------------
# Global Variables
#---------------------------------------------------------------------------

Faction = None

    
#---------------------------------------------------------------------------
# Game Setup
#---------------------------------------------------------------------------

def gameSetup(group, x = 0, y = 0): # WiP
   debugNotify(">>> gameSetup()") #Debug
   if debugVerbosity >= 1: notify(">>> gameSetup(){}".format(extraASDebug())) #Debug
   mute()
   global Faction
   if Faction and not confirm("Are you sure you want to setup for a new game? (This action should only be done after a table reset)"): return
   resetAll()
   chooseSide()
   deck = me.piles['Deck']
   leadersDeck = me.piles['Leaders']
   missionDeck = shared.Missions
   debugNotify("Arranging Leaders",2)
   if len(leadersDeck) < 4 and not confirm(":::Illegal Deck:::\n\nYou must have at least 4 leaders in your leader deck.\n\nProceed Anyway?"): return
   for leader in leadersDeck:
      leader.moveTo(leadersDeck,num(leader.level)) # This function will move each leader card at the index of the leader deck, according to its level. So level 1 leader will be top, and level 4 will be bottom
      if not Faction: Faction = leader.Faction
      elif Faction != leader.Faction:
         if not confirm(":::Illegal Deck:::\n\nYou have leader of different factions in your leader deck.\n\nProceed Anyway?"): return
         else: notify(":::Warning::: {}'s Leader deck has different factions!".format(me))
   debugNotify("Setting Reference Cards",2)
   if Faction == "Banshee Net": table.create("9f291494-8713-4b7e-bc7c-36b428fc0dd1",(playerside * -380) - 25, (playerside * 20) + yaxisMove,1,True) # Creating a the player's faction reference card.
   if Faction == "Bloodvine": table.create("8e2ff010-98b5-4884-a39b-100940d4f702",(playerside * -380) - 25, (playerside * 20) + yaxisMove,1,True) # Creating a the player's faction reference card.
   if Faction == "Franchise": table.create("6d131915-cb6a-43ca-b2f1-64ac040b0eec",(playerside * -380) - 25, (playerside * 20) + yaxisMove,1,True) # Creating a the player's faction reference card.
   if Faction == "The Krypt": table.create("0d058ed6-51e8-42c7-9cbb-67a3d267c618",(playerside * -380) - 25, (playerside * 20) + yaxisMove,1,True) # Creating a the player's faction reference card.
   if Faction == "Nine Tiger": table.create("49f5d0ad-60e2-4810-86b6-5f962f99d9bd",(playerside * -380) - 25, (playerside * 20) + yaxisMove,1,True) # Creating a the player's faction reference card.
   if Faction == "Shadow Patriots": table.create("bf4bfecd-1d84-4a6f-a787-0986a0fe06b1",(playerside * -380) - 25, (playerside * 20) + yaxisMove,1,True) # Creating a the player's faction reference card.
   debugNotify("Moving First Leader to table",2)
   leadersDeck.top().moveToTable(0, (playerside * 100) + yaxisMove()) # Top card in the leaders deck should be the player's level 1 leader.
   debugNotify("Preparing Mission Deck",2)
   currMissionsVar = getGlobalVariable('currentMissions')
   if currMissionsVar != 'CHECKED OUT':
      currentMissions = eval(currMissionsVar)
      if len(currentMissions) == 0: 
         shuffle(missionDeck)
         startingMissions = missionDeck.top(5)
         for mission in startingMissions: prepMission(mission, True)
      else: debugNotify("Missions already setup by another player. Aborting mission deck setup",4)
   else: debugNotify("Missions currently being setup by another player",4)
   shuffle(deck)
   drawMany(deck, 7, silent = True)
   debugNotify("<<< gameSetup()") #Debug
    
#---------------------------------------------------------------------------
# Rest
#---------------------------------------------------------------------------
    
def roll6(group, x = 0, y = 0):
    mute()
    n = rnd(1, 6)
    notify("{} rolls {} on a 6-sided die.".format(me, n))

def draw(group, x = 0, y = 0):
    if len(group) == 0: return
    mute()
    group[0].moveTo(me.hand)
    notify("{} draws a card.".format(me))

def drawMany(group = me.piles['Deck'], count = None, destination = None, silent = False):
   debugNotify(">>> drawMany()") #Debug
   debugNotify("source: {}".format(group.name),2)
   debugNotify("destination: {}".format(destination.name),2)
   mute()
   if destination == None: destination = me.hand
   SSize = len(group)
   if SSize == 0: return 0
   if count == None: count = askInteger("Draw how many cards?", 5)
   if count == None: return 0
   if count > SSize : 
      count = SSize
      delayed_whisper("You do not have enough cards in your deck to complete this action. Will draw as many as possible")
   for c in group.top(count): 
      c.moveTo(destination)
   if not silent: notify("{} draws {} cards.".format(me, count))
   debugNotify("<<< drawMany() with return: {}".format(count))
   return count

    
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

def expose(card, x = 0, y = 0):
    mute()
    if card.markers[mdict['exposed']] == 0:
        notify("{} becomes Exposed.".format(card))
        card.markers[mdict['exposed']] = 1
    else:
        notify("{} is not Exposed anymore.".format(card))
        card.markers[mdict['exposed']] = 0


def baffle(card, x = 0, y = 0):
    mute()
    if card.markers[mdict['baffled']] == 0:
       notify("{} becomes Baffled and is considered Exposed until the end of the mission.".format(card))
       card.markers[mdict['exposed']] += 1
       card.markers[mdict['baffled']] += 1
    else:
       notify("{} is not baffled anymore.".format(card))
       card.markers[mdict['exposed']] -= 1
       card.markers[mdict['baffled']] -= 1

def ability(card, x = 0, y = 0):
    mute()
    card.highlight = AbilityColor
    notify('{} activates the ability on {}'.format(me, card))

def download_o8c(group,x=0,y=0):
   openUrl("http://dbzer0.com/pub/SpycraftCCG/sets/SpycraftCCG-Sets-Bundle.o8c")
    