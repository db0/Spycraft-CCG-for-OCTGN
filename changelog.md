Changelog - Spycraft CCG OCTGN Game Definition
===============================================

### 1.0.5.x

* Fixed the participate command which was mistakenly put under the table menu. The same command can now also take agents out of missions (in case they are removed via card effects)
* Prevented Inactive cards from performing a briefing
* Added "Discard a random card" action, to the hand menu.
* You can now cancel current mission (in case it was started by mistake)
* You can now pull out agents from the team with a special table menu action. Simply target the agents you want to pull out and use it.
* "Fresh Leader" markers will be removed at the debriefing phase.
* Inactive gear won't ask you if you want it to participate in missions if you double click it.
* Fixed King Maul's Craft.
* Fixed Setup placement to be a bit more bunched up in the middle.
* Fixed activating leader placement to pop-into the middle of the table which is a bit more obvious.
* Fixed Discarding Target Cards

### 1.0.4.x

* **Significant:** Added card attachment code. 
  * Now when you play a card as a gear, you need to have one of your active or inactive agent cards targeted or it will abort. 
  * Cards played as gear will be attached to their host card automatically at the right placement
  * When retiring an agent card, all attached gear is also automatically trashed.
  * When activating a agent played as gear, or a gear played as agent, those cards will be automatically discarded.

### 1.0.3.x

* **Significant:** Added Mission Participation controls
  * Double clicking on a mission or targeting and pressing Ctrl+A initiates a run on that mission for your side
  * Double clicking a highlighted mission tries to score it
  * Double clicking on a non-participating agent, marks them as a participanty
  * Double clicking on a participating agent tries to use: Default Mission Action, Mission Action, Text Action, in that order
  * Face down cards can be declared as participants as well.
  * Winning or Discarding a mission currently being run, clears all participants and their mission markers.
* Added Debriefing Phase. It just draws 5 cards for you and announces it.


### 1.0.2.x

* Fixed b0rked mutliplayer mission queue
* **Significant:** Leaders now start in your hand and are placed on the table at the start of the game, behind your reference card. You can use the brief action on inactive leaders.
* **Significant:** Added Intel Phase (F1). Only one player needs to use it per turn, and it will clear all once-per-turn markers and calculate who has the initiative
* Discarding a Leader now automatically activates the next one
* Activating a Leader now automatically demotes the existing one.
* Fixed placement of 2nd player cards and mission queue a bit
* Added a function under the game menu to get the mission queue unstuck if it gets stuck
* Game will auto peek face down cards you play
* Added Brief ability 
* Added Snoop ability
* Added Mission Action and Default Mission Action
* You can now discard cards from your hand as Bravado
* Activating Actions cards played as bluffs now discard them.


### 1.0.1.x

* Game setup function now functional. After one player has loaded the mission deck and you've loaded your deck, 
* Mission queue now autoupdated when you win or discard one. Just make sure you do it via the appropriate menu options.
* Added default actions for playing cards from your hand. Should be fairly smart on what it does
* Added smart action for double-clicking cards on the table.

### 1.0.0.x

Conversion for OCTGN 3.1.x

### 0.4.1

Incorporated changes from the official 0.4 version by Lord Nat to 0.3.1 and modified the following

  * The Expose action became Expose/Clear. Using it a second time will remove the Exposed counter.
  * The Baffle action became Baffle/Clear. Using it a second time will reduce the counters by one.

### 0.3.1

Added a different background to fit the theme

### 0.3

Original version released by Lord Nat in the [OCTGN Game Directory](http://octgn.gamersjudgement.com/viewtopic.php?f=44&t=262)