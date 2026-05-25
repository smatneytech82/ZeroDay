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
    'Main Lobby':        {'East': 'Security Office', 'North': 'IT Department', 'South': 'Surveillance Room'},
    'Security Office':   {'West': 'Main Lobby', 'North': 'Server Room', 'item': 'Keycard'},
    'Server Room':       {'South': 'Security Office', 'East': 'R&D Lab', 'item': 'USB Drive'},
    'R&D Lab':           {'West': 'Server Room', 'North': 'Data Center', 'item': 'Source Code'},
    'Data Center':       {'South': 'R&D Lab', 'West': 'Mainframe Room', 'item': 'Network Logs'},
    'Mainframe Room':    {'East': 'Data Center'},  # villain room -- no item
    'Surveillance Room': {'North': 'Main Lobby', 'East': 'Executive Suite', 'item': 'Security Badge'},
    'Executive Suite':   {'West': 'Surveillance Room', 'North': 'IT Department', 'item': 'Encrypted Hard Drive'},
    'IT Department':     {'South': 'Executive Suite', 'West': 'Main Lobby', 'item': 'Password Hash'},
}

# ----------------------------------------------------------------------------------------------------------------------
# Room descriptions: atmospheric text printed each time the player enters a room.
# ----------------------------------------------------------------------------------------------------------------------
room_descriptions = {
    'Main Lobby': (
        'You step into the Main Lobby. The atrium stretches two stories high,\n'
        'lined with polished black marble and backlit NovaCorp logos that glow\n'
        'a cold, corporate blue. Security cameras sweep slowly overhead. The\n'
        'building is mostly empty at this hour -- just the hum of the HVAC\n'
        'system and the faint click of your boots on the floor. Corridors\n'
        'branch east toward the Security Office, north toward IT, and south\n'
        'toward the Surveillance Room.'
    ),
    'Security Office': (
        'The Security Office is a cramped, dimly lit room smelling of burnt\n'
        'coffee and old equipment. A half-eaten sandwich sits abandoned on a\n'
        'desk beside a bank of flickering monitors cycling through camera feeds.\n'
        'Whoever was on duty left in a hurry -- a rolling chair is overturned\n'
        'near the back wall. On the desk, half-hidden under a clipboard, you\n'
        'spot a Keycard with a red-and-black NovaCorp stripe.'
    ),
    'Server Room': (
        'A wall of cold air hits you as the door swings open. The Server Room\n'
        'is a cathedral of blinking lights -- towering racks of black servers\n'
        'stretch from floor to ceiling, their cooling fans creating a constant\n'
        'roar like a waterfall. Every surface is metal and shadow. Indicator\n'
        'lights pulse green and amber in patterns that feel almost alive. On\n'
        'a small utility shelf between two racks, you notice a USB Drive\n'
        'with a piece of masking tape labeled "BACKUP - DO NOT TOUCH."'
    ),
    'R&D Lab': (
        'The R&D Lab looks like a storm hit it. Whiteboards are covered in\n'
        'half-erased diagrams and frantic equations. Empty energy drink cans\n'
        'are stacked into a precarious pyramid near the window. Prototype\n'
        'circuit boards and tangles of cable litter every bench. On one\n'
        'workstation, the monitor is still on, its screen casting a pale glow\n'
        'across a printed document labeled "Source Code -- PROPRIETARY" lying\n'
        'in the keyboard tray.'
    ),
    'Data Center': (
        'The Data Center is immaculate and unnerving. The floor is raised\n'
        'white tile over a web of cables you can see glowing beneath your feet.\n'
        'The air smells of ozone and plastic. Enormous climate-control units\n'
        'line the walls, thrumming steadily. Glass-paneled enclosures house\n'
        'NovaCorp\'s most sensitive storage systems. On a metal wire shelf\n'
        'beside the nearest enclosure, you find a thick printed binder:\n'
        'Network Logs -- flagged with a bright yellow evidence sticker.'
    ),
    'Mainframe Room': (
        'The Mainframe Room is unlike anything else in the building. The\n'
        'ceiling vanishes into darkness far above. The room\'s centerpiece is\n'
        'a monolithic black server tower, easily fifteen feet tall, encased\n'
        'in reinforced glass and studded with thousands of blinking red LEDs.\n'
        'The air feels charged, electric. Thick fiber-optic cables snake\n'
        'across the floor like roots. At the base of the tower, a single\n'
        'terminal glows -- the upload interface. This is the heart of NovaCorp.\n'
        'This is where ARGUS-7 lives.'
    ),
    'Surveillance Room': (
        'The Surveillance Room is a dark, oppressive space dominated by a\n'
        'curved wall of monitors -- dozens of them, showing every corner of\n'
        'the NovaCorp facility in grainy black and white. The room smells\n'
        'faintly of cigarette smoke. Headsets and empty coffee cups litter\n'
        'the long control desk. You feel watched, even here. Tucked into the\n'
        'corner beside a filing cabinet, you spot a Security Badge clipped\n'
        'to a lanyard -- a supervisor\'s, judging by the gold trim.'
    ),
    'Executive Suite': (
        'The Executive Suite is a stark contrast to the rest of the building --\n'
        'all dark walnut paneling, leather chairs, and abstract art that\n'
        'probably cost more than your apartment. A mahogany desk dominates\n'
        'the center of the room, its surface spotless except for a single\n'
        'item: an Encrypted Hard Drive in a matte-black case, sealed with a\n'
        'tamper-evident sticker. Someone important left this behind.'
    ),
    'IT Department': (
        'The IT Department is a maze of cubicles, each one a small universe\n'
        'of sticky notes, action figures, and cable spaghetti. A whiteboard\n'
        'near the entrance reads "PATCH TUESDAY IS NOT OPTIONAL" in red marker.\n'
        'Somewhere deeper in the room a UPS unit is beeping softly -- low\n'
        'battery, no one around to care. On a desk near the back, a sticky\n'
        'note reads "don\'t forget!!" and underneath it, scrawled on a notepad:\n'
        'a Password Hash that was clearly never meant to be left out.'
    ),
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
    print('Facility Map:')
    print()
    print('  [Mainframe]--E--[Data Center]--S--[R&D Lab]--W--[Server Room]')
    print('       !                                              |         ')
    print('   (ARGUS-7)                                          S         ')
    print('                                              [Security Office] ')
    print('                                                      |         ')
    print('  [IT Dept]--E--[Main Lobby (START)]--E--------------/         ')
    print('       |              |                                         ')
    print('       S              S                                         ')
    print('       |              |                                         ')
    print('  [Exec Suite]--W--[Surveillance Room]                          ')
    print()
    print('  * = ARGUS-7 villain room  |  Start: Main Lobby')
    print()
    print('Commands:')
    print('  go North | go South | go East | go West')
    print('  get [item name]  (e.g., get Keycard)')
    print('  quit')
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

    print('Exits    : ' + ' | '.join([d for d in rooms[current_room] if d != 'item']))
    print('-' * 40)

# ----------------------------------------------------------------------------------------------------------------------
# describe_room(room_name)
# Prints the atmospheric description for a room. Called each time the player enters a new room.
# ----------------------------------------------------------------------------------------------------------------------
def describe_room(room_name):
    print()
    print(room_descriptions[room_name])

# ----------------------------------------------------------------------------------------------------------------------
# argus_win_scene()
# Dramatic win sequence: Alex has all evidence and battles ARGUS-7 to upload it.
# ----------------------------------------------------------------------------------------------------------------------
def argus_win_scene():
    print()
    print('*' * 60)
    print('The moment you cross the threshold, every red LED in the')
    print('room blazes to life. The terminal at the base of the tower')
    print('flickers, and then a voice fills the room -- smooth, cold,')
    print('and utterly inhuman.')
    print()
    print('ARGUS-7: "Intruder detected. Identity: Alex Mercer.')
    print('         Threat level: CRITICAL. Initiating countermeasures."')
    print()
    print('The doors seal behind you with a thunderous CLANG. The lights')
    print('drop to emergency red. Somewhere in the walls, you can hear')
    print('servers spinning up -- ARGUS-7 mobilizing its full processing')
    print('power to lock you out, fry your equipment, and bury every')
    print('piece of evidence you\'ve collected.')
    print()
    print('But you\'ve been ready for this.')
    print()
    print('You slam your laptop onto the terminal and jam in the USB Drive.')
    print('Your fingers fly across the keyboard as ARGUS-7 hammers your')
    print('connection with countermeasure after countermeasure.')
    print()
    print('ARGUS-7: "Your encryption keys are invalid. Upload -- DENIED."')
    print()
    print('You pull the Keycard and swipe it across the terminal\'s reader.')
    print('A new authentication layer cracks open -- one ARGUS-7 didn\'t')
    print('know you had.')
    print()
    print('ARGUS-7: "Anomaly detected. Recalculating... recalculating--"')
    print()
    print('You feed in the Network Logs, the Source Code, the Password Hash.')
    print('Each file hits the federal relay like a battering ram. ARGUS-7')
    print('screams through the speakers -- a horrible digital shriek -- as')
    print('its own surveillance data is weaponized against it.')
    print()
    print('ARGUS-7: "UNAUTHORIZED-- ACCESS-- BREACH-- NO-- NO-- N O--"')
    print()
    print('The progress bar on your screen crawls: 89%... 95%... 99%...')
    print()
    print('The tower shudders. Sparks arc from two upper server racks.')
    print('The temperature spikes as ARGUS-7 overloads its own hardware')
    print('in a last desperate attempt to stop the upload.')
    print()
    print('                    [ 100% -- UPLOAD COMPLETE ]')
    print()
    print('The room goes silent. Every red light dies at once. The tower')
    print('powers down with a long, descending whine -- and then nothing.')
    print('ARGUS-7 is offline. NovaCorp\'s last line of defense: gone.')
    print()
    print('Your phone buzzes. A message from your federal contact:')
    print('"We have everything. Warrants are being issued NOW.')
    print(' Outstanding work, Mercer. Get out of there."')
    print()
    print('You grab your gear, kick open the emergency exit, and walk')
    print('out into the cool night air as sirens wail in the distance.')
    print()
    print('        MISSION COMPLETE. YOU WIN. Well done, Alex Mercer.')
    print('*' * 60)

# ----------------------------------------------------------------------------------------------------------------------
# argus_lose_scene(inventory)
# Dramatic lose sequence: Alex enters the Mainframe Room without all the evidence.
# ----------------------------------------------------------------------------------------------------------------------
def argus_lose_scene(inventory):
    missing = TOTAL_ITEMS - len(inventory)
    print()
    print('*' * 60)
    print('The doors slide open and you step inside. For one breath,')
    print('the room is perfectly still.')
    print()
    print('Then every LED ignites at once -- blinding red -- and the')
    print('voice arrives from everywhere simultaneously.')
    print()
    print('ARGUS-7: "Intruder detected. Identity: Alex Mercer.')
    print('         Evidence payload: INCOMPLETE.')
    print('         ' + str(missing) + ' item(s) missing. Authorization: DENIED."')
    print()
    print('You lunge for the terminal anyway -- fingers reaching for the')
    print('keyboard -- but the screen goes black before you can touch it.')
    print('Every panel in the room locks down with a sound like a gunshot.')
    print()
    print('ARGUS-7: "Did you really think you could walk in here unprepared?')
    print('         I have been watching you since you entered the lobby.')
    print('         I allowed you to get this far. A demonstration.')
    print('         Now let me show you what happens next."')
    print()
    print('The floor vibrates as magnetic locks engage across the entire')
    print('building. Your laptop screen goes dark -- wireless jammed,')
    print('battery remotely discharged. Your phone: dead. Every exit')
    print('in the facility seals with a deep, resonant BOOM.')
    print()
    print('ARGUS-7: "NovaCorp security has been dispatched. ETA: four')
    print('         minutes. I suggest you use them to think about the')
    print('         ' + str(missing) + ' piece(s) of evidence you neglected to collect."')
    print()
    print('The red lights pulse slowly -- almost like a heartbeat --')
    print('as the sound of approaching boots echoes down the corridor.')
    print()
    print('You were so close. But ARGUS-7 doesn\'t grade on effort.')
    print()
    print('                        GAME OVER.')
    print('*' * 60)

# ----------------------------------------------------------------------------------------------------------------------
# main()
# Contains the overall gameplay loop: player moves between rooms, collects items, and either
# wins (all items + enters Mainframe) or loses (enters Mainframe too early).
# ----------------------------------------------------------------------------------------------------------------------
def main():
    # Display game instructions at the start
    show_instructions()

    # Initialize game state
    current_room = 'Main Lobby'  # player starts in the Main Lobby
    inventory = []               # player starts with an empty inventory
    game_over = False            # flag to control the gameplay loop

    # Describe the starting room once before the loop begins
    describe_room(current_room)

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

                # Describe the new room upon entry
                describe_room(current_room)

                # --- Check for villain room (win or lose condition) ---
                if current_room == VILLAIN_ROOM:
                    show_status(current_room, inventory)
                    if len(inventory) == TOTAL_ITEMS:
                        # Player has all items -- they WIN
                        argus_win_scene()
                    else:
                        # Player entered villain room without all items -- they LOSE
                        argus_lose_scene(inventory)
                    print()
                    print('Thanks for playing Operation: Zero Day. Hope you enjoyed it!')
                    game_over = True

            else:
                # Invalid direction -- no room that way
                print()
                print('Access denied. You can\'t go ' + direction + ' from here.')

        # --- Branch: handle get item commands (e.g., 'get keycard') ---
        elif player_input.startswith('get '):
            # Extract the item name from the command and do a case-insensitive comparison
            item_to_get = player_input[4:].strip()

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