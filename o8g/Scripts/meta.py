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
   setGlobalVariable('currentMissions', '[]')
   if len(players) > 1: debugVerbosity = -1 # Reset means normal game.
   elif debugVerbosity != -1 and confirm("Reset Debug Verbosity?"): debugVerbosity = -1 
   debugNotify("<<< resetAll()") #Debug
   
def prepMission(card, GameSetup = False): 
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
      if iter - 1 > 0: missionFaceDown = True # Last three missions are face down
      else: missionFaceDown = False # First two missions are face up
      Mission.moveToTable(cwidth() * (3 - iter), 0, missionFaceDown)
      if missionFaceDown: Mission.orientation = Rot90
      else: Mission.orientation = Rot0
      # rnd(1,100) # We put a delay here to allow the table to read the card autoscripts before we try to execute them.
   debugNotify("About to set currentMissions",2) #Debug      
   setGlobalVariable('currentMissions', str(currentMissions))
   debugNotify("<<< prepMission()") #Debug
   
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
