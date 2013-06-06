    # Python Scripts for the Spycraft CCG definition for OCTGN
    # Copyright (C) 2013  Konstantine Thoukydides

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

import re, time

debugVerbosity = -1 # At -1, means no debugging messages display
    
Automations = {'Play'    : True, # If True, game will automatically trigger card effects when playing or double-clicking on cards. Requires specific preparation in the sets.
               'WinForms'               : True, # If True, game will use the custom Windows Forms for displaying multiple-choice menus and information pop-ups
               'Placement'              : True, # If True, game will try to auto-place cards on the table after you paid for them.
               'Start/End-of-Turn/Phase': True, # If True, game will automatically trigger effects happening at the start of the player's turn, from cards they control.                
              }
    
def ofwhom(Autoscript, controller = me):  # WiP
   if debugVerbosity >= 1: notify(">>> ofwhom(){}".format(extraASDebug(Autoscript))) #Debug
   targetPL = None
   if re.search(r'o[fn]Opponent', Autoscript):
      if len(players) > 1:
         if controller == me: # If we're the current controller of the card who's scripts are being checked, then we look for our opponent
            for player in players:
               if player.getGlobalVariable('Side') == '': continue # This is a spectator 
               elif player != me and player.getGlobalVariable('Side') != Side:
                  targetPL = player # Opponent needs to be not us, and of a different type. 
                                    # In the future I'll also be checking for teams by using a global player variable for it and having players select their team on startup.
         else: targetPL = me # if we're not the controller of the card we're using, then we're the opponent of the player (i.e. we're trashing their card)
      else: 
         if debugVerbosity >= 1: whisper("There's no valid Opponents! Selecting myself.")
         targetPL = me
   else: 
      if len(players) > 1:
         if controller != me: targetPL = controller         
         else: targetPL = me
      else: targetPL = me
   if debugVerbosity >= 3: notify("<<< ofwhom() returns {}".format(targetPL))
   return targetPL

def resetAll(): # Clears all the global variables in order to start a new game.
   global Faction, debugVerbosity
   debugNotify(">>> resetAll()") #Debug
   mute()
   Faction = None
   hostCards = eval(getGlobalVariable('Host Cards'))
   hostCards.clear()
   leadersDict.clear()
   setGlobalVariable('Host Cards',str(hostCards))
   if len(shared.Missions) == 24: setGlobalVariable('currentMissions', '[]') # If the mission deck is exactly 24 cards, then it means it's a fresh game, and we clean the mission queue,
                                                                         # If it's less, then it means the mission queue has already been setup by another player so we don't do it again.
   if debugVerbosity != -1 and confirm("Reset Debug Verbosity?"): debugVerbosity = -1 
   debugNotify("<<< resetAll()") #Debug
   
def prepMission(card, silent = False): 
# Function stores into a shared variable the current missions, so that everyone can look them up and re-arrange them.
# This function also reorganizes the missions on the table
   debugNotify(">>> prepMission()") #Debug
   currMissionsVar = getGlobalVariable('currentMissions')
   if currMissionsVar == 'CHECKED OUT':
      delayed_whisper(":::ATTENTION::: Another player's scripts are manipulating the mission queue. Please try again later") 
      return 'ABORT'
   setGlobalVariable('currentMissions','CHECKED OUT') # If the missions var is not being manipulated by another, we set it as checked out ourselves.
   currentMissions = eval(currMissionsVar)
   currentMissions.append(card._id)
   debugNotify("About to iterate the list: {}".format(currentMissions),2)
   for iter in range(len(currentMissions)):
      Mission = Card(currentMissions[iter])
      if iter - 1 > 0 and not Mission.isFaceUp: missionFaceDown = True # Last three missions are face down unless they were already face up
      else: missionFaceDown = False # First two missions are face up
      Mission.moveToTable(cheight() * (2 - iter), (cheight(0) / -2) + 8, missionFaceDown)
      if missionFaceDown: Mission.orientation = Rot90
      else: 
         Mission.orientation = Rot0
         if not Mission.isFaceUp: Mission.isFaceUp = True # Backup check
      # rnd(1,100) # We put a delay here to allow the table to read the card autoscripts before we try to execute them.
   debugNotify("About to set currentMissions",2) #Debug      
   setGlobalVariable('currentMissions', str(currentMissions))
   if not silent: notify(":> Mission Queue Updated!")
   debugNotify("<<< prepMission()") #Debug

def scrubMission(card):
# Function cleans a mission card from the shared variable which shows which missions are on the table
   debugNotify(">>> scrubMission()") #Debug
   currMissionsVar = getGlobalVariable('currentMissions')
   if currMissionsVar == 'CHECKED OUT':
      delayed_whisper(":::ATTENTION::: Another player's scripts are manipulating the mission queue. Please try again later") 
      return 'ABORT'
   setGlobalVariable('currentMissions','CHECKED OUT') # If the missions var is not being manipulated by another, we set it as checked out ourselves.
   debugNotify("About to remove mission",2)
   currentMissions = eval(currMissionsVar)
   currentMissions.remove(card._id)
   debugNotify("About to set currentMissions",2) #Debug      
   setGlobalVariable('currentMissions', str(currentMissions))
   debugNotify("<<< scrubMission()") #Debug

def finishRun():
   debugNotify(">>> finishRun()") #Debug
   mute()
   for card in table:
      card.target(False)
      card.highlight = None
      card.markers[mdict['MissionAction']] = 0
      card.markers[mdict['DefaultMission']] = 0
   debugNotify("<<< finishRun()") #Debug

#------------------------------------------------------------------------------
# Card Attachments scripts
#------------------------------------------------------------------------------

def findHost():
   debugNotify(">>> findHost(){}".format(extraASDebug())) #Debug
   # Tries to find a host to attach the gear
   hostCards = eval(getGlobalVariable('Host Cards'))
   potentialHosts = [card for card in table  # Potential hosts are:
                     if card.targetedBy # Cards that are targeted by the player
                     and card.targetedBy == me 
                     and card.controller == me # Which the player control
                     and ((card.Type == 'Agent' or (card.Type == 'Leader' and card.isFaceUp)) # That are either Agents or Active Leader
                        or (not card.isFaceUp                    # Or that are face down (i.e. pretending to be agents)
                           and card.orientation == Rot0          # and are not turned sideways (which is reserved for missions and incactive leaders) 
                           and not hostCards.has_key(card._id))) # and are not attached to other cards already
                     ]
   debugNotify("Finished gatherting potential hosts",2)
   if len(potentialHosts) == 0:
      delayed_whisper(":::ERROR::: Please Target a valid host for this gear!")
      result = None
   else: result = potentialHosts[0] # If a propert host is targeted, then we return it to the calling function. We always return just the first result.
   debugNotify("<<< findHost() with result {}".format(result), 3)
   return result

def attachCard(attachment,host,facing = 'Same'):
   debugNotify(">>> attachCard(){}".format(extraASDebug())) #Debug
   hostCards = eval(getGlobalVariable('Host Cards'))
   hostCards[attachment._id] = host._id
   setGlobalVariable('Host Cards',str(hostCards))
   orgAttachments(host,facing)
   debugNotify("<<< attachCard()", 3)
   
def clearAttachLinks(card):
# This function takes care to discard any attachments of a card that left play
# It also clear the card from the host dictionary, if it was itself attached to another card
# If the card was hosted by a Daemon, it also returns the free MU token to that daemon
   debugNotify(">>> clearAttachLinks()") #Debug
   hostCards = eval(getGlobalVariable('Host Cards'))
   cardAttachementsNR = len([att_id for att_id in hostCards if hostCards[att_id] == card._id])
   if cardAttachementsNR >= 1:
      hostCardSnapshot = dict(hostCards)
      for attachmentID in hostCardSnapshot:
         if hostCardSnapshot[attachmentID] == card._id:
            if Card(attachmentID) in table: discard(Card(attachmentID))
            del hostCards[attachmentID]
   debugNotify("Checking if the card is attached to unlink.", 2)      
   if hostCards.has_key(card._id):
      hostCard = Card(hostCards[card._id])
      del hostCards[card._id] # If the card was an attachment, delete the link
      orgAttachments(hostCard) 
   setGlobalVariable('Host Cards',str(hostCards))
   debugNotify("<<< clearAttachLinks()", 3) #Debug   


def orgAttachments(card,facing = 'Same'):
# This function takes all the cards attached to the current card and re-places them so that they are all visible
# xAlg, yAlg are the algorithsm which decide how the card is placed relative to its host and the other hosted cards. They are always multiplied by attNR
   debugNotify(">>> orgAttachments()") #Debug
   attNR = 1
   debugNotify(" Card Name : {}".format(card.name), 4)
   if specialHostPlacementAlgs.has_key(card.name):
      debugNotify("Found specialHostPlacementAlgs", 3)
      xAlg = specialHostPlacementAlgs[card.name][0]
      yAlg = specialHostPlacementAlgs[card.name][1]
      debugNotify("Found Special Placement Algs. xAlg = {}, yAlg = {}".format(xAlg,yAlg), 2)
   else: 
      debugNotify("No specialHostPlacementAlgs", 3)
      yAlg = 0 # The Default placement on the Y axis, is to place the attachments at the same line as their parent
      #if card.controller == me: sideOffset = playerside # If it's our card, we need to assign it towards our side
      #else: sideOffset = playerside * -1 # Otherwise we assign it towards the opponent's side
      xAlg = -(cwidth() / 3 * playerside) # Default placement on the x axis is to the left of its host
   hostCards = eval(getGlobalVariable('Host Cards'))
   cardAttachements = [Card(att_id) for att_id in hostCards if hostCards[att_id] == card._id]
   x,y = card.position
   for attachment in cardAttachements:
      if facing == 'Faceup': FaceDown = False
      elif facing == 'Facedown': FaceDown = True
      else: # else is the default of 'Same' and means the facing stays the same as before.
         if attachment.isFaceUp: FaceDown = False
         else: FaceDown = True
      attachment.moveToTable(x + (xAlg * attNR), y + (yAlg * attNR),FaceDown)
      if attachment.controller == me and FaceDown: attachment.peek()
      attachment.setIndex(len(cardAttachements) - attNR) # This whole thing has become unnecessary complicated because sendToBack() does not work reliably
      debugNotify("{} index = {}".format(attachment,attachment.getIndex), 4) # Debug
      attNR += 1
      debugNotify("Moving {}, Iter = {}".format(attachment,attNR), 4)
   card.sendToFront() # Because things don't work as they should :(
   if debugVerbosity >= 4: # Checking Final Indices
      for attachment in cardAttachements: notify("{} index = {}".format(attachment,attachment.getIndex)) # Debug
   debugNotify("<<< orgAttachments()", 3) #Debug      

#------------------------------------------------------------------------------
# Debugging
#------------------------------------------------------------------------------
   
def TrialError(group, x=0, y=0): # Debugging
   global debugVerbosity
   mute()
   ######## Testing Corner ########
   #findTarget('Targeted-atVehicle_and_Fighter_or_Character_and_nonWookie')
   #BotD.moveToTable(0,0) 
   ###### End Testing Corner ######
   #notify("### Setting Debug Verbosity")
   if debugVerbosity >=0: 
      if debugVerbosity == 0: 
         debugVerbosity = 1
         #ImAProAtThis() # At debug level 1, we also disable all warnings
      elif debugVerbosity == 1: debugVerbosity = 2
      elif debugVerbosity == 2: debugVerbosity = 3
      elif debugVerbosity == 3: debugVerbosity = 4
      else: debugVerbosity = 0
      notify("Debug verbosity is now: {}".format(debugVerbosity))
      return
   notify("### Checking Players")
   for player in players:
      if player.name == 'db0' or player.name == 'dbzer0': debugVerbosity = 0
   notify("### Checking Debug Validity")
   if not (len(players) == 1 or debugVerbosity >= 0): 
      whisper("This function is only for development purposes")
      return
   notify("### Setting Table Side")
   if not playerside:  # If we've already run this command once, don't recreate the cards.
      chooseSide()

def extraASDebug(Autoscript = None):
   if Autoscript and debugVerbosity >= 3: return ". Autoscript:{}".format(Autoscript)
   else: return ''

def fixMissions(group, x = 0, y = 0): 
   setGlobalVariable('currentMissions', '[]')
   for card in table:
      if fetchProperty(card, 'Type') == 'Mission':
         prepMission(card, True)
   notify("{} has re-scanned the Mission Queue".format(me))
         
def debugMissions(group, x = 0, y = 0): 
   missionsVar = getGlobalVariable('currentMissions')
   debugNotify("Sh.Var: {}".format(missionsVar),1)
   if missionsVar != "CHECKED OUT":
      missionsList = eval(missionsVar)
      debugNotify("len = {}".format(len(missionsList)),1)
      debugNotify("missions: {}".format([Card(mission) for mission in missionsList]), 1)         
   else: debugNotify("Mission Queue is checked out",1)
