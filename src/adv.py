from room import Room
from player import Player
from item import Item
from weapon import Weapon

# Declare items

rocks = Item("rocks", "Small rocks. Good for a slingshot, if you had one.")
map = Item("map", "Looks like a treasure map.")
slingshot = Item("slingshot", "Well used, but appears to still function.")

# Declare rooms

rooms = {
    'outside':  Room("Outside Cave Entrance",
                    "North of you, the cave mouth beckons",
                    [rocks]),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east.""", 
                    []),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm.""",
                    [slingshot]),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air.""",
                    []),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south.""",
                    [map]),
}


# Link rooms together

rooms['outside'].n_to = 'foyer'
rooms['foyer'].s_to = 'outside'
rooms['foyer'].n_to = 'overlook'
rooms['foyer'].e_to = 'narrow'
rooms['overlook'].s_to = 'foyer'
rooms['narrow'].w_to = 'foyer'
rooms['narrow'].n_to = 'treasure'
rooms['treasure'].s_to = 'narrow'

#
# Main
#

# Make a new player object that is currently in the 'outside' room.

player = Player("Steve", "outside", [])

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.

playing = True

while playing:
    current_room = rooms[player.current_room]

    print("--------------------")
    print(current_room)

    commands = input(" >>> ").lower().strip().split()

    if len(commands) == 1:
        cmd = commands[0]
        
        if cmd in ["n", "s", "e", "w"]:
            if hasattr(current_room, f"{cmd}_to"):
                player.current_room = getattr(current_room, f"{cmd}_to")
                print(f"Moving {cmd.upper()}")
            else:
                print(f"Can't move {cmd.upper()}")
        
        elif cmd == "q":
            playing = False
            print("Goodbye!")

    elif len(commands) == 2:

        if commands[0] == "get":
            # remove item if exists
            item = current_room.removeItem(commands[1])
            if item:
                # add to player storage
                player.storage.append(item)
            else:
                print(f"A `{commands[1]}` does not exist here.")

        elif commands[0] == "drop":
            # remove item if exists
            item = player.removeItem(commands[1])
            if item:
                # add to room storage
                current_room.storage.append(item)
            else:
                print(f"You don't have a `{commands[1]}` to drop.")

        if len(player.storage) > 0:
            print(f"You have: {player.storageString()}")
        else:
            print("You are not carrying anything.")
    
    else:
        print(f"I do not understand `{cmd}`")