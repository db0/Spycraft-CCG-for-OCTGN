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
