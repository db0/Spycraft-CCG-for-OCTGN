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
   if debugVerbosity >= 1: notify(">>> resetAll(){}".format(extraASDebug())) #Debug
   mute()
   hostCards = eval(getGlobalVariable('Host Cards'))
   hostCards.clear()
   setGlobalVariable('Host Cards',str(hostCards))
   if len(players) > 1: debugVerbosity = -1 # Reset means normal game.
   elif debugVerbosity != -1 and confirm("Reset Debug Verbosity?"): debugVerbosity = -1 
   setGlobalVariable('Turn','0')
   if debugVerbosity >= 1: notify("<<< resetAll()") #Debug