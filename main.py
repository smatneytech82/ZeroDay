# Shannon Matney
# IT 140 - Project Two
# TextBasedGame.py
# Operation: Zero Day -- Full Text-Based Adventure Game
# Player is Alex Mercer, an ethical hacker infiltrating NovaCorp to collect evidence
# before confronting the rogue AI Guardian in the Mainframe Room.

# ----------------------------------------------------------------------------------------------------------------------
# Room dictionary: links each room to its neighbors (by direction) and its item (if any).
# The Main Lobby is the starting room (no item).
# The Mainframe Room is the villain room (no item -- player wins or loses upon entry).
# ----------------------------------------------------------------------------------------------------------------------
rooms = {
    'Main Lobby':       {'East': 'Security Office', 'North': 'IT Department', 'South': 'Surveillance Room'},
    'Security Office':  {'West': 'Main Lobby', 'North': 'Server Room', 'item': 'Keycard'},
    'Server Room':      {'South': 'Security Office', 'East': 'R&D Lab', 'item': 'USB Drive'},
    'R&D Lab':          {'West': 'Server Room', 'North': 'Data Center', 'item': 'Source Code'},
    'Data Center':      {'South': 'R&D Lab', 'West': 'Mainframe Room', 'item': 'Network Logs'},
    'Mainframe Room':   {'East': 'Data Center'},  # villain room -- no item
    'Surveillance Room':{'North': 'Main Lobby', 'East': 'Executive Suite', 'item': 'Security Badge'},
    'Executive Suite':  {'West': 'Surveillance Room', 'North': 'IT Department', 'item': 'Encrypted Hard Drive'},
    'IT Department':    {'South': 'Executive Suite', 'West': 'Main Lobby', 'item': 'Password Hash'},
}

# Total number of items the player must collect to win
TOTAL_ITEMS = 7

# The room that contains the villain (ARGUS-7)
VILLAIN_ROOM = 'Mainframe Room'

# ----------------------------------------------------------------------------------------------------------------------
# show_instructions()
# Displays the game title, backstory, goal, and available commands.
# ----------------------------------------------------------------------------------------------------------------------
def show_instructions():
    print('=' * 60)
    print('         OPERATION: ZERO DAY')
    print('         A Cybersecurity Text Adventure')
    print('=' * 60)
    print()
    print('You are Alex Mercer, an elite ethical hacker.')
    print('A federal agency has hired you to infiltrate NovaCorp --')
    print('a tech corporation secretly running illegal surveillance')
    print('and data-trafficking operations.')
    print()
    print('Your mission: collect all 7 pieces of digital evidence')
    print('scattered across NovaCorp\'s facility, then upload them')
    print('from the Mainframe Room to expose the corporation.')
    print()
    print('WARNING: The Mainframe Room is guarded by ARGUS-7,')
    print('NovaCorp\'s rogue AI. Enter without all 7 items and')
    print('you will be permanently locked out.')
    print()
    print('Evidence to collect (7 items):')
    print('  1. Keycard')
    print('  2. USB Drive')
    print('  3. Source Code')
    print('  4. Network Logs')
    print('  5. Security Badge')
    print('  6. Encrypted Hard Drive')
    print('  7. Password Hash')
    print()
    print('Commands:')
    print(' go North | go South | go East | go West')
    print(' get [item name] (e.g., get Keycard)')
    print(' quit')
    print('=' * 60)

# ----------------------------------------------------------------------------------------------------------------------
# show_status(current_room, inventory)
# Displays the player's current room, their inventory, and any item present in the room.
# ----------------------------------------------------------------------------------------------------------------------
def show_status(current_room, inventory):
    print()
    print('-' * 40)
    print('Location : ' + current_room)
    print('Inventory: ' + str(inventory))

    # Check if there is an item in the current room that hasn't been collected yet
    if 'item' in rooms[current_room]:
        room_item = rooms[current_room]['item']
        if room_item not in inventory:
            print('You see  : ' + room_item)
        else:
            print('You see  : (already collected)')
    else:
        print('You see  : Nothing of interest')

    print('-' * 40)

# ----------------------------------------------------------------------------------------------------------------------
# main()
# Contains the overall gameplay loop: player moves between rooms, collects items, and either
# wins (all items + enters Mainframe) or loses (enters Mainframe too early).
# ----------------------------------------------------------------------------------------------------------------------
def main():  # FIX 1: added missing colon
    # Display game instructions at the start
    show_instructions()

    # Initialize game state
    current_room = 'Main Lobby'  # player starts in the Main Lobby
    inventory = []               # player starts with an empty inventory
    game_over = False            # flag to control the gameplay loop

    # ------------------------------------------------------------------------------------------------------------------
    # Main gameplay loop: continues until the player wins, loses, or quits
    # ------------------------------------------------------------------------------------------------------------------
    while not game_over:

        # Show the player's current status
        show_status(current_room, inventory)

        # Prompt the player for input and normalize to lowercase for comparison
        player_input = input('Enter your command: ').strip().lower()

        # --- Branch: handle the quit command ---
        if player_input == 'quit':
            print()
            print('Mission aborted. NovaCorp lives to surveil another day.')
            print('Thanks for playing Operation: Zero Day!')
            game_over = True

        # --- Branch: handle movement commands (e.g., 'go north') ---
        elif player_input.startswith('go '):
            # Split input to isolate the direction word
            parts = player_input.split(' ', 1)
            direction = parts[1].strip().title()  # convert to Title Case (e.g., 'north' -> 'North')

            # Check if that direction is a valid exit from the current room
            if direction in rooms[current_room]:
                current_room = rooms[current_room][direction]  # move to the new room
                print()
                print('Moving ' + direction + '... You are now in: ' + current_room)

                # --- Check for villain room (win or lose condition) ---
                if current_room == VILLAIN_ROOM:
                    show_status(current_room, inventory)
                    print()
                    if len(inventory) == TOTAL_ITEMS:
                        # Player has all items -- they WIN
                        print('*' * 60)
                        print('You have all 7 pieces of evidence!')
                        print('You connect to the Mainframe and upload the data...')
                        print()
                        print('ARGUS-7 attempts to fight back, but the evidence upload')
                        print('completes. Federal agents move in. NovaCorp is exposed.')
                        print()
                        print('MISSION COMPLETE. YOU WIN! Congratulations, Alex Mercer.')
                        print('*' * 60)
                        print()
                        print('Thanks for playing Operation: Zero Day. Hope you enjoyed it!')
                        game_over = True  # FIX 2: added missing game_over = True for win condition
                    else:
                        # Player entered villain room without all items -- they LOSE
                        print('*' * 60)
                        print('ALERT! ARGUS-7 detects your intrusion!')
                        print('You only have ' + str(len(inventory)) + ' of ' + str(TOTAL_ITEMS) + ' items.')
                        print()
                        print('ARGUS-7: "Insufficient authorization. Initializing lockout."')
                        print('ALL exits seal. You are trapped. GAME OVER.')
                        print('*' * 60)
                        print()
                        print('Thanks for playing Operation: Zero Day. Hope you enjoyed it!')
                        game_over = True

            else:
                # Invalid direction -- no room that way  # FIX 3: un-nested from inside the 'if direction' block
                print()
                print('Access denied. You can\'t go ' + direction + ' from here.')

        # --- Branch: handle get item commands (e.g., 'get keycard') ---
        elif player_input.startswith('get '):  # FIX 3 cont.: restored to top-level elif (was nested under 'go')
            # Extract the item name from the command and do a case-insensitive comparison
            item_to_get = player_input[4:].strip()  # FIX 4: changed player_inputer to player_input

            # Check if the current room has an item
            if 'item' in rooms[current_room]:
                room_item = rooms[current_room]['item']

                if item_to_get.lower() == room_item.lower():
                    # Correct item name entered
                    if room_item in inventory:
                        # Player already has this item
                        print()
                        print('You already have the ' + room_item + '.')
                    else:
                        # Add the item to the player's inventory
                        inventory.append(room_item)
                        print()
                        print('You picked up the ' + room_item + '. Added to inventory.')
                else:
                    # Item name doesn't match what's in the room
                    print()
                    print('There is no ' + item_to_get + ' here. Check what\'s in this room.')
            else:
                # No item in this room at all
                print()
                print('There is nothing to pick up here.')

        # --- Branch: any other input is invalid ---
        else:
            print()
            print('Invalid command. Use: go [direction], get [item name], or quit.')

# ----------------------------------------------------------------------------------------------------------------------
# Entry point: run the main function when the script is executed
# ----------------------------------------------------------------------------------------------------------------------
main()