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
   global Faction
   if debugVerbosity >= 1: notify(">>> resetAll(){}".format(extraASDebug())) #Debug
   mute()
   Faction = None
   hostCards = eval(getGlobalVariable('Host Cards'))
   hostCards.clear()
   setGlobalVariable('Host Cards',str(hostCards))
   if len(players) > 1: debugVerbosity = -1 # Reset means normal game.
   elif debugVerbosity != -1 and confirm("Reset Debug Verbosity?"): debugVerbosity = -1 
   setGlobalVariable('Turn','0')
   debugNotify("<<< resetAll()") #Debug
   
def prepMission(card, GameSetup = False): 
# Function stores into a shared variable the current missions, so that everyone can look them up and re-arrange them.
# This function also reorganizes the missions on the table
   debugNotify(">>> prepMission()") #Debug
   currentMissions = eval(me.getGlobalVariable('currentMissions'))
   destroyedObjectives = eval(getGlobalVariable('destroyedObjectives'))
   for card_id in destroyedObjectives: 
      try:
         currentMissions.remove(card_id) # Removing destroyed objectives before checking.
         destroyedObjectives.remove(card_id) # When we successfully remove an objective stored in this list, we clear it as well, so that we don't check it again in the future.
      except ValueError: pass # If an exception is thrown, it means that destroyed objective does not exist in this objective list
   currentMissions.append(card._id)
   debugNotify("About to iterate the list: {}".format(currentMissions),2)
   if GameSetup:
      for iter in range(len(currentMissions)):
         Objective = Card(currentMissions[iter])
         Objective.moveToTable((playerside * -315) - 25, (playerside * -10) + (70 * iter * playerside) + yaxisMove(Objective), True)
         Objective.highlight = ObjectiveSetupColor # During game setup, we put the objectives face down so that the players can draw their hands before we reveal them.
         Objective.orientation = Rot90
   else:
      for iter in range(len(currentMissions)):
         Objective = Card(currentMissions[iter])
         Objective.moveToTable((playerside * -315) - 25, (playerside * -10) + (70 * iter * playerside) + yaxisMove(Objective))
         xPos, yPos = Objective.position
         countCaptures = 0
         debugNotify("About to retrieve captured cards",2) #Debug      
         capturedCards = eval(getGlobalVariable('Captured Cards'))
         for capturedC in capturedCards: # once we move our objectives around, we want to move their captured cards with them as well.
            if capturedCards[capturedC] == Objective._id:
               debugNotify("Moved Objective has Captured cards. Moving them...",2)
               countCaptures += 1
               Card(capturedC).moveToTable(xPos - (cwidth(Objective) * playerside / 2 * countCaptures), yPos, True)
               Card(capturedC).sendToBack()
         #Objective.orientation = Rot90
      rnd(1,100) # We put a delay here to allow the table to read the card autoscripts before we try to execute them.
      debugNotify("About to set destroyedObjectives",2) #Debug      
      setGlobalVariable('destroyedObjectives', str(destroyedObjectives))
      debugNotify("About to execure play Scripts",2) #Debug      
      executePlayScripts(card, 'PLAY')
   debugNotify("About to set currentMissions",2) #Debug      
   me.setGlobalVariable('currentMissions', str(currentMissions))
   debugNotify("<<< prepMission()") #Debug