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


import re

#---------------------------------------------------------------------------
# Global Variables
#---------------------------------------------------------------------------

Faction = None
leadersDict = {} # A dictionary which holds card IDs of all the player's leaders according to their level.
    
#---------------------------------------------------------------------------
# Game Setup
#---------------------------------------------------------------------------

def gameSetup(group, x = 0, y = 0): # WiP
   debugNotify(">>> gameSetup()") #Debug
   mute()
   global Faction, leadersDict
   if Faction and not confirm("Are you sure you want to setup for a new game? (This action should only be done after a table reset)"): return
   debugNotify("Resetting All", 2) #Debug
   debugNotify("Choosing Side", 2) #Debug
   resetAll()
   chooseSide()
   debugNotify("Setting Deck Variables", 2) #Debug
   deck = me.piles['Deck']
   missionDeck = shared.Missions
   if len(missionDeck) == 0 or len(missionDeck) > 24: 
      delayed_whisper(":::ERROR::: Please load the mission deck properly before setting up the game")
      return
   debugNotify("Checking hand size",2)
   if len(me.hand) < 4 and not confirm(":::Illegal Deck:::\n\nYou must have at least 4 leaders in your deck.\n\nProceed Anyway?"): return
   debugNotify("Arranging Leaders",2)
   for leader in me.hand:
      if leader.Type != 'Leader':
         delayed_whisper("You're only allowed to hold leaders during setup. Shuffling {} into your deck".format(leader))
         leader.moveTo(deck)
         continue
      debugNotify("Checking Faction",2)
      if not Faction: Faction = leader.Faction
      elif Faction != leader.Faction:
         if not confirm(":::Illegal Deck:::\n\nYou have leader of different factions in your leader deck.\n\nProceed Anyway?"): return
         else: 
            notify(":::Warning::: {}'s Leader deck has different factions!".format(me))
            Faction = leader.Faction
      #debugNotify("Moving {} ({}) to pos {}".format(leader, leader.level, num(leader.level) - 1),2)
      debugNotify("Checking Leader Levels",2)
      if num(leader.Level) == 1:
         debugNotify("Moving First Leader to table",2)
         leadersDict[1] = leader._id
         leader.moveToTable(0, (playerside * 130) + yaxisMove()) # Level 1 leader is moved to the table
         leader.markers[mdict['Fresh']] += 1
      else:
         debugNotify("Moving high level Leader to table",2)
         leadersDict[num(leader.Level)] = leader._id
         leader.moveToTable(playerside * -1 * (350 + cwidth()),(playerside * cwidth() * (4 - num(leader.Level))) + yaxisMove(), True)
         leader.orientation = Rot90
         leader.peek()
         # We move the level 2-4 leaders face down to the table, behind the reference card. Highest level leader is on the top
   for iter in range(4): # We do a quick check to see we indeed have leaders 1-4
      if not leadersDict.get(iter + 1,None): notify(":::WARNING::: {} is missing their level {} leader!".format(iter + 1))
   debugNotify("Setting Reference Cards",2)
   if Faction == "Banshee Net": table.create("9f291494-8713-4b7e-bc7c-36b428fc0dd1",playerside * -330, (playerside * 20) + yaxisMove(),1,True) # Creating a the player's faction reference card.
   if Faction == "Bloodvine": table.create("8e2ff010-98b5-4884-a39b-100940d4f702",playerside * -330, (playerside * 20) + yaxisMove(),1,True) # Creating a the player's faction reference card.
   if Faction == "Franchise": table.create("6d131915-cb6a-43ca-b2f1-64ac040b0eec",playerside * -330, (playerside * 20) + yaxisMove(),1,True) # Creating a the player's faction reference card.
   if Faction == "The Krypt": table.create("0d058ed6-51e8-42c7-9cbb-67a3d267c618",playerside * -330, (playerside * 20) + yaxisMove(),1,True) # Creating a the player's faction reference card.
   if Faction == "Nine Tiger": table.create("49f5d0ad-60e2-4810-86b6-5f962f99d9bd",playerside * -330, (playerside * 20) + yaxisMove(),1,True) # Creating a the player's faction reference card.
   if Faction == "Shadow Patriots": table.create("bf4bfecd-1d84-4a6f-a787-0986a0fe06b1",playerside * -330, (playerside * 20) + yaxisMove(),1,True) # Creating a the player's faction reference card.
   debugNotify("Preparing Mission Deck",2)
   currMissionsVar = getGlobalVariable('currentMissions')
   debugNotify("currMissionsVar = {}".format(currMissionsVar),2)
   if currMissionsVar != 'CHECKED OUT':
      currentMissions = eval(currMissionsVar)
      debugNotify("currentMissions = {}".format(currentMissions),4)
      if len(currentMissions) == 0: 
         shuffle(missionDeck)
         startingMissions = missionDeck.top(5)
         for mission in startingMissions: prepMission(mission, True)
      else: debugNotify("Missions already setup by another player. Aborting mission deck setup",4)
   else: debugNotify("Missions currently being setup by another player",4)
   if PlayerColor == "#": defPlayerColor()
   shuffle(deck)
   drawMany(deck, 7, silent = True)
   debugNotify("<<< gameSetup()") #Debug
    

#---------------------------------------------------------------------------
# Table Card Actions
#---------------------------------------------------------------------------

def defaultAction(card, x = 0, y = 0):
   debugNotify(">>> defaultAction()") #Debug
   mute()
   for c in table:
      if c.Type == 'Mission' and c.highlight: missionInProgress = True
      else: missionInProgress = False
      if missionInProgress: break
   debugNotify("Checking for activation",2) #Debug
   if not card.isFaceUp:
      hostCards = eval(getGlobalVariable('Host Cards'))
      if missionInProgress and not card.highlight and not hostCards.has_key(card._id): # If there is a mission in progress, and the card is not currently participating and it's not a gear, then check if the player wants it to participate
         if confirm("There's currently a mission in progress. Do you want to declare this card as participating agent?"): participate(card)
         else: activate(card)
      else: activate(card)
   elif card.Type == 'Mission':
      if not card.highlight: runMission(card)
      else: winMission(card)
   elif card.Type == 'Agent' or card.Type == 'Leader':
      if missionInProgress:
         if not card.highlight: participate(card)
         elif not card.markers[mdict['DefaultMission']]: useDefaultMission(card)
         elif not card.markers[mdict['MissionAction']]: useMission(card)
         else: useText(card)
      else: useText(card)
   else: 
      if missionInProgress:
         if not card.markers[mdict['MissionAction']]: useMission(card)
         else: useText(card)
      else: useText(card)
   debugNotify("<<< defaultAction()") #Debug
    
def activate(card, x = 0, y = 0):
   debugNotify(">>> activate()") #Debug
   mute()
   if card.isFaceUp:
      notify("{} Deactivates {}".format(me, card))
      card.isFaceUp = False
   else:
      card.isFaceUp = True
      rnd(1,10)
      hostCards = eval(getGlobalVariable('Host Cards'))
      if card.Type == 'Mission': 
         notify("{} Reveals {}".format(me, card))
         card.orientation = Rot0
      elif (card.Type == 'Action' # If the card is an action and it's been played face-down, it's always discarded on activation
            or (card.Type == 'Agent' and hostCards.has_key(card._id)) # If the card is an agent and it's been played as an attachment, it's a bluff and must be discarded
            or (card.Type == 'Gear' and not hostCards.has_key(card._id))): # if the card is a gear and it has been played as an agent, it's a bluff and must be discarded
         notify("{} Reveals the {} card {} as a bluff! The card is discarded.".format(card.owner, card.Type, card))
         rnd(1,1000) # Adding a small delay before discarding the card.
         clearAttachLinks(card)
         card.moveTo(card.owner.Discard)
      elif card.Type == 'Leader':
         if card.markers[mdict['Briefed']] < num(card.properties['Expense Rating']) and not confirm("You do not seem to have enough briefing tokens on this leader to activate them.\n\nProceed anyway?"):
            card.isFaceUp = False
            card.peek()
            return
         notify("{} Activates their level {} leader: {}".format(me,card.Level,card))
         card.orientation = Rot0
         card.moveToTable(playerside * -300, yaxisMove() + (cwidth() * playerside * 2))
         if num(card.Level) < 4: card.markers[mdict['Fresh']] += 1
         card.markers[mdict['Briefed']] = 0
         for c in table:
            if c.controller == me and c.isFaceUp and c.Type == 'Leader' and num(c.Level) < num(card.Level) and not c.markers[mdict['Demoted']]:
               c.markers[mdict['Demoted']] = 1
               notify("{}'s previous leader ({}) is demoted".format(me,c))
               break
      else: 
         if card.Type == 'Gear': notify("{} Activates {} on {}".format(me, card, Card(hostCards[card._id]))) 
         else: notify("{} Activates {}".format(me, card))
   debugNotify("<<< activate()") #Debug

def discard(card, x = 0, y = 0):
   debugNotify(">>> discard()") #Debug
   mute()
   if fetchProperty(card, 'Type') != 'Mission': 
      if card.Type == 'Agent' or (card.Type == 'Leader' and card.markers[mdict['Demoted']]): notify("{} retires {}.".format(me, card))
      elif card.Type == 'Leader':
         debugNotify("About to discard Active leader", 2) #Debug
         if card.Level == '4': notify("{} has retired their highest level leader and loses the game".format(me))
         else:
            for iter in range(4):
               debugNotify("Checking Leader level {}".format(iter + 1), 3) #Debug
               leaderCHK = Card(leadersDict[iter + 1])
               if not leaderCHK.isFaceUp and leaderCHK.group == table:
                  notify("{} retires {} and {} activates to take their place as leader.".format(me,card,leaderCHK))
                  leaderCHK.isFaceUp = True
                  rnd(1,10)
                  leaderCHK.orientation = Rot0
                  leaderCHK.moveToTable(playerside * -300, yaxisMove() + (cwidth() * playerside * 2))
                  if num(leaderCHK.Level) < 4: leaderCHK.markers[mdict['Fresh']] += 1
                  leaderCHK.markers[mdict['Briefed']] = 0
                  break
      else: notify("{} trashes {}.".format(me, card))
      clearAttachLinks(card)
      card.moveTo(card.owner.Discard)
   else: 
      if card.highlight: finishRun()
      if scrubMission(card) == 'ABORT': return
      if prepMission(shared.Missions.top()) == 'ABORT': return
      clearAttachLinks(card)
      card.moveTo(shared.piles['Mission Discard'])
      notify("{} discards {}.".format(me, card))
   debugNotify("<<< discard()") #Debug
      
def discardTarget(group, x = 0, y = 0):
   if confirm("Are you sure you want to discard all cards you've targeted on the table?"):
      for card in table:
         if card.targetedBy and card.targetedBy == me: discard(card)

def useText(card, x = 0, y = 0):
    mute()
    card.markers[mdict['TextAction']] += 1
    if card.markers[mdict['TextAction']] > 1: extraTXT = ' {}'.format(numOrder(card.markers[mdict['TextAction']])) # The extra text only displays if the player uses a second or third printed ability on the same card.
    else: extraTXT = ''
    notify('{} uses the a{} printed ability on {}.'.format(me, extraTXT, card))

def useMission(card, x = 0, y = 0):
    mute()
    card.markers[mdict['MissionAction']] += 1
    if card.markers[mdict['MissionAction']] > 1: extraTXT = ' {}'.format(numOrder(card.markers[mdict['MissionAction']])) # The extra text only displays if the player uses a second or third printed ability on the same card.
    else: extraTXT = ''
    notify('{} uses the a{} mission ability on {}.'.format(me, extraTXT, card))

def useDefaultMission(card, x = 0, y = 0):
    mute()
    card.markers[mdict['DefaultMission']] += 1
    if card.markers[mdict['DefaultMission']] > 1: extraTXT = ' for the {} time'.format(numOrder(card.markers[mdict['DefaultMission']])) # The extra text only displays if the player uses a second or third printed ability on the same card.
    else: extraTXT = ''
    notify('{} uses the default mission action{} with {}.'.format(me, extraTXT, card))
    
def runMission(card, x = 0, y = 0):
   debugNotify(">>> runMission()")
   mute()
   for c in table:
      debugNotify("Checking table card: {}".format(c),4)
      if c.Type == 'Mission' and c.highlight:
         delayed_whisper(":::ERROR::: There's already a run in progress on {}. Please make sure that run is complete by winning, discarding or cleasring that mission, and then redo this action.".format(c))
         return 'ABORT'
   if fetchProperty(card, 'Type') == 'Mission': 
      debugNotify("About to start the run:",2)
      if not card.isFaceUp: 
         card.isFaceUp = True
         rnd(1,10)
         card.orientation = Rot0
      debugNotify("About to assign highlight color",2)
      debugNotify("My color is {}".format(PlayerColor),4)
      card.highlight = PlayerColor
      notify("{} starts a run on {}".format(me,card))
   else: 
      delayed_whisper(":::ERROR::: You can only run mission cards")      
      return 'ABORT'
   debugNotify("<<< runMission()")
   return 'OK'

def runTargetMission(group, x = 0, y = 0):
   for card in table:
      if card.targetedBy and card.targetedBy == me: 
         runResult = runMission(card)
         if runResult != 'ABORT': break
    
def winMission(card, x = 0, y = 0):
   mute()
   if card.Type == 'Mission' and confirm("Have you just won {}?".format(card.name)): 
      if card.highlight: finishRun()
      if scrubMission(card) == 'ABORT': return 'ABORT'
      if prepMission(shared.Missions.top()) == 'ABORT': return 'ABORT'
      card.moveTo(me.piles['Victory Pile'])
      me.counters['Victory Points'].value += num(card.properties['Victory Points'])
      notify("{} wins {} and gains {} VP.".format(me, card, card.properties['Victory Points']))
   else: 
      whisper(":::ERROR::: You can only win missions")
      return 'ABORT'
   return 'OK'

def winTargetMission(group, x = 0, y = 0):
   mute()
   for card in table:
      if card.targetedBy and card.targetedBy == me: 
         winResult = winMission(card)
         if winResult != 'ABORT': break
    
def abortMission(group, x = 0, y = 0):
   mute()
   if confirm("Do you want your team to abort the current mission?"): finishRun(True)
   notify("{} has pulled some agents out of the current mission")

    
def cancelMission(group, x = 0, y = 0):
   mute()
   missionCard = None
   for card in table:
      if card.Type == 'Mission' and card.highlight and confirm("Cancel the current mission for all players?"):
         card.highlight = None
         finishRun()
         missionCard = card
         break
   if missionCard: notify("{} has cancelled {}".format(me,missionCard))
    
def inspectCard(card, x = 0, y = 0): # This function shows the player the card text, to allow for easy reading until High Quality scans are procured.
   debugNotify(">>> inspectCard()") #Debug
   #if debugVerbosity > 0: finalTXT = 'AutoScript: {}\n\n AutoAction: {}'.format(CardsAS.get(card.model,''),CardsAA.get(card.model,''))
   if card.Type == 'Reference':
      information("This is the {} Leader Ability Reference card.\
                 \nIt does not have any abilities itself but it informs you which built-in ability your leaders have.".format(card.Faction))
   else:          
      finalTXT = "{}\n\nTraits:{}\n\nCard Text: {}".format(card.name, card.Traits, card.Rules)
      information("{}".format(finalTXT))

def inspectTargetCard(group, x = 0, y = 0): # This function shows the player the card text, to allow for easy reading until High Quality scans are procured.
   debugNotify(">>> inspectTargetCard()") #Debug
   for card in table:
      if card.targetedBy and card.targetedBy == me: inspectCard(card)
    
#---------------------------------------------------------------------------
# Agent Status and Actions
#---------------------------------------------------------------------------

def snoop(card, x = 0, y = 0):
   mute()
   if card.markers[mdict['Snoop']] > 0 and not confirm("{} has already snooped at a card this turn. Proceed anyway?".format(card.name)): return
   targetCard = None
   for c in table:
      if c.targetedBy and c.targetedBy == me and not c.isFaceUp:
         targetCard = c
         break
   if not targetCard: 
      whisper(":::ERROR::: You need to target a face down card to snoop at.")
   else:
      targetCard.peek()
      card.markers[mdict['Snoop']] += 1
      notify("{} snoops target inactive card".format(card))
      
def brief(card, x = 0, y = 0):
   mute()
   if card.markers[mdict['Fresh']] > 0 and not confirm("{} has enterred play this turn and is not normally allowed to perform a brief. Proceed anyway?".format(card.name)): return
   if card.markers[mdict['Demoted']] > 0 and not confirm("{} is a demoted leader and is not normally allowed to perform a brief. Proceed anyway?".format(card.name)): return
   if card.markers[mdict['Brief']] > 0 and not confirm("{} has already briefed a leader this turn. Proceed anyway?".format(card.name)): return
   if (not card.isFaceUp or card.Type != 'Leader') and not confirm("Only active leaders may perform a brief action. Proceed anyway?".format(card.name)): return
   targetCard = None
   for c in table:
      if c.targetedBy and c.targetedBy == me and not c.isFaceUp and fetchProperty(c, 'Type') == 'Leader':
         targetCard = c
         break
   if not targetCard: 
      whisper(":::ERROR::: You need to target a face down leader to brief.")
   else:
      card.markers[mdict['Brief']] += 1
      briefNR = num(card.properties['Expense Rating'])
      targetCard.markers[mdict['Briefed']] += briefNR
      notify("{} briefs one of their inactive leaders for {} points".format(card,briefNR))
      
def clear(card, x = 0, y = 0, silent = False):
   debugNotify(">>> clear()")
   mute()
   if not silent: notify("{} clears {}.".format(me, card))
   card.target(False)
   card.markers[mdict['Brief']] = 0
   card.markers[mdict['Snoop']] = 0
   card.markers[mdict['MissionAction']] = 0
   card.markers[mdict['DefaultMission']] = 0
   card.markers[mdict['TextAction']] = 0
   debugNotify("<<< clear()")

def participate(card, x = 0, y = 0):
   debugNotify(">>> participate()")
   mute()
   if card.highlight == AttackerColor or card.highlight == DefenderColor:
      card.highlight = None
      card.markers[mdict['MissionAction']] = 0
      card.markers[mdict['DefaultMission']] = 0
      card.markers[mdict['Baffled']] = 0
      notify("{} leaves the mission".format(card))
   else:
      attacker = None
      for c in table:
         if c.Type == 'Mission' and c.highlight:
            if c.highlight == PlayerColor: attacker = 'me'
            else: attacker = 'opponent'
            break
      if attacker == 'me': 
         card.highlight = AttackerColor
         notify("{} declares {} as an attacker.".format(me,card))
      elif attacker == 'opponent': 
         card.highlight = DefenderColor
         notify("{} declares {} as a defender.".format(me,card))
      else: delayed_whisper("There is no mission run currently in progress! Aborting.")
   debugNotify("<<< participate()")
   
   
def wound(card, x = 0, y = 0):
   mute()
   card.orientation ^= Rot90
   if card.orientation & Rot90 == Rot90:
      notify('{} is wounded.'.format(card))
   else:
      notify('{} is unwounded.'.format(card))

def expose(card, x = 0, y = 0):
    mute()
    if card.markers[mdict['Exposed']] == 0:
        notify("{} becomes Exposed.".format(card))
        card.markers[mdict['Exposed']] = 1
    else:
        notify("{} is not Exposed anymore.".format(card))
        card.markers[mdict['Exposed']] = 0

def baffle(card, x = 0, y = 0):
    mute()
    if card.markers[mdict['Baffled']] == 0:
       notify("{} becomes Baffled, loses all skill points, and is considered Exposed until the end of the mission.".format(card))
       card.markers[mdict['Baffled']] = 1
    else:
       notify("{} is not baffled anymore.".format(card))
       card.markers[mdict['Baffled']] = 0

#---------------------------------------------------------------------------
# Hand Actions
#---------------------------------------------------------------------------

def smartPlay(card, x = 0, y = 0):
    mute()
    if card.Type == 'Gear': playGear(card)
    elif card.Type == 'Action': playAction(card)
    else: playAgent(card)

def playAgent(card, x = 0, y = 0):
    mute()
    card.moveToTable(playerside * -270, yaxisMove() + (cwidth() * playerside),True)
    card.peek()
    notify("{} recruits an agent from their hand.".format(me))

def playGear(card, x = 0, y = 0):
    mute()
    hostCard = findHost()
    if not hostCard: return
    else: attachCard(card,hostCard,'Facedown')
    #card.moveToTable(playerside * -220, yaxisMove() + (cwidth() * playerside),True)
    if hostCard.isFaceUp: notify("{} requisitions a gear for {}.".format(me,hostCard))
    else: notify("{} requisitions a gear from their hand.".format(me))

def playAction(card, x = 0, y = 0):
    mute()
    card.moveToTable(playerside * 300, yaxisMove() + (cwidth() * playerside))
    if re.search(r'Solo Op',card.Traits):
      notify("{} begins the {} Solo Op.".format(me, card))
      draw()
    else: notify("{} attempts to play {}.".format(me, card))

def playBravado(card, x = 0, y = 0):
    mute()
    card.moveTo(me.Discard)
    notify("{} discards {} for {} bravado.".format(me, card, card.Bravado))

def discardFromHand(card):
   mute()
   card.moveTo(me.Discard)
   notify("{} discards {}.".format(me, card))

def shuffleIntoDeck(group = me.Discard):
   mute()
   Deck = me.Deck
   for c in group: c.moveTo(Deck)
   random = rnd(100, 1000)
   Deck.shuffle()
   notify("{} shuffles his {} into his Deck.".format(me, group.name))
   
def handRandomDiscard(group, count = None, player = None, silent = False):
   debugNotify(">>> handRandomDiscard(){}".format(extraASDebug())) #Debug
   mute()
   if not player: player = me
   SSize = len(group)
   if SSize == 0: return 0
   if count == None: count = askInteger("Discard how many cards at random?", 1)
   if count == None: return 0
   if count > SSize :
      count = SSize
      whisper("You do not have enough cards in your hand to complete this action. Will discard as many as possible.")
   for iter in range(count):
      debugNotify("handRandomDiscard() iter: {}".format(iter + 1), 3) # Debug
      card = group.random()
      if card == None: return iter + 1 # If we have no more cards, then return how many we managed to discard.
      card.moveTo(player.Discard)
      if not silent: notify("{} discards {} at random.".format(player,card))
   debugNotify("<<< handRandomDiscard() with return {}".format(iter + 1), 2) #Debug
   return iter + 1 #We need to increase the iter by 1 because it starts iterating from 0
   

#---------------------------------------------------------------------------
# Pile Actions
#---------------------------------------------------------------------------

def draw(group = me.piles['Deck'], x = 0, y = 0):
    if len(group) == 0: return
    mute()
    group[0].moveTo(me.hand)
    notify("{} draws a card.".format(me))

def drawMany(group = me.piles['Deck'], count = None, destination = None, silent = False):
   debugNotify(">>> drawMany()") #Debug
   debugNotify("source: {}".format(group.name),2)
   if destination: debugNotify("destination: {}".format(destination.name),2)
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

#---------------------------------------------------------------------------
# Phases
#---------------------------------------------------------------------------

def goToIntel(group,x=0,y=0):
   mute()
   notify("===================")
   notify("  New Intel Phase  ")
   notify("===================")
   craftCalcs = {}
   debugNotify("About to calculate crafts",2)
   for player in players: # First we calculate the craft for each player 
      craftCalcs[player] = 0
      debugNotify("About to iterate table cards",4)
      for card in table:
         clear(card, silent = True) # Since we're going through all cards, we might as well clear them now.
         if card.controller == player and card.isFaceUp:
            if card.orientation == Rot90 and (card.Type == 'Agent' or card.Type == 'Leader'): # If agent is wounded, their craft is reduced by 2
               craft = num(card.Craft) - 2
               if craft < 0: craft = 0
            else:
               craft = num(card.Craft)
            craftCalcs[player] += craft
   craftyPlayers = [] # A list holding the player or players with the highest craft total.
   debugNotify("About to compare crafts",2)
   for player in players:
      if len(craftyPlayers) == 0: craftyPlayers.append(player)
      else:
         for crafty in craftyPlayers:
            debugNotify("Comparing {}'s total of {} with {} total of {}".format(player, craftCalcs[player], crafty, craftCalcs[crafty]), 4)
            if crafty == player: continue # Don't compare with ourself.
            if craftCalcs[crafty] < craftCalcs[player]: 
               del craftyPlayers[:] # If the checked player has more craft than those in the list, we clear the list and put just them in
               craftyPlayers.append(player)
               debugNotify("{}'s is larger".format(player), 4)
               break
            elif craftCalcs[crafty] == craftCalcs[player]: 
               craftyPlayers.append(player)  # If they are equal, we put them both in the list
               debugNotify("{}'s is equal".format(player), 4)
               break
   if len(craftyPlayers) == 1: 
      debugNotify("Only one winner",4)
      winner = craftyPlayers[0]
      notify(":> {} has the most craft this turn and takes the initiative".format(winner))
   else:
      debugNotify("Craft is tied",4)
      random = rnd(0,len(craftyPlayers) - 1)
      winner = craftyPlayers[random]
      notify(":> {} are tied in craft this turn. {} is selected at random to get the initiative".format([player.name for player in craftyPlayers],winner))
   debugNotify("About to place starting marker",2)
   for card in table:
      if card.Type == 'Reference':
         if card.owner == winner: card.markers[mdict['Starting']] = 1
         else: card.markers[mdict['Starting']] = 0

def goToDebrief(group,x=0,y=0):
   mute()
   drawMany(count = 5,silent = True)
   for card in table:
      if card.markers[mdict['Fresh']]: card.markers[mdict['Fresh']] = 0 # We clean the "fresh" markers from all leaders to allow them to perform briefing actions next turn.
   notify(":> {} starts their debriefing phase and draw 5 cards".format(me))
   

#---------------------------------------------------------------------------
# Announcements
#---------------------------------------------------------------------------

def declarePass(group,x=0,y=0):
   notify("-- {} Passes".format(me))
   
#---------------------------------------------------------------------------
# Rest
#---------------------------------------------------------------------------

def roll6(group, x = 0, y = 0):
    mute()
    n = rnd(1, 6)
    notify("{} rolls {} on a 6-sided die.".format(me, n))

def download_o8c(group,x=0,y=0):
   openUrl("http://dbzer0.com/pub/SpycraftCCG/sets/SpycraftCCG-Sets-Bundle.o8c")

    
