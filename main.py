# Display title screen
import os


def prompt():
    print("----------------Welcome to Simple Game \U0001F642 Nice to have you----------------")
    print()


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def handle_open(noun, current_room, rooms, containers, vowels):
    if noun == "":
        print("You need to be more specific.")
    # if the room has a container in it and that container matches the input
    elif 'container' in rooms[current_room].keys() and rooms[current_room]['container'] == noun.lower():
        container_open = containers[noun]['open']
        container_locked = containers[noun]['locked']
        # if the container is both unlocked and unopened, it will do the following
        if container_locked == 'no' and container_open == 'no':
            # container is now set to open
            containers[noun]['open'] = 'yes'
            rooms[current_room]['item'] = containers[noun]['item']
            # goes through rooms{} and checks to see if there are any items
            if 'item' in rooms[current_room].keys():
                nearby_item = rooms[current_room]['item']
                # if the last character of the item is an 's' (as in a plural item)
                if nearby_item[-1] == 's':
                    print(f'You open the {noun} and find {nearby_item}')
                # else if the first letter of the item is a vowel
                elif nearby_item[0] in vowels:
                    print(f'You open the {noun} and see an {nearby_item}')
                # else if the item is singular and starts with a consonant
                else:
                    print(f'You open the {noun} and see a {nearby_item}')
        elif container_locked == 'yes':
            print(f'The {noun} is locked. Maybe I should find a key...')
        elif container_open == 'yes':
            print(f'The {noun} is already open, dumb dumb')
    else:
        print(f'You don\'t see a {noun} to open.')


def handle_go(noun, currentRoom, rooms):
    # declares current_room as global to modify it
    global current_room
    if noun == '':
        print("You need to be more specific.")
    elif noun in rooms[currentRoom].keys():
        current_room = rooms[current_room][noun]
        print(f'You moved to the {current_room}')
    else:
        print('I can\'t go that way.')


def handle_talk(noun, current_room, rooms, dialogue):
    if noun == "":
        print("You need to be more specific.")
    # goes through rooms, checks to see if there's any npc's and checks if the input is a valid npc
    elif 'npc' in rooms[current_room].keys() and rooms[current_room]['npc'] == noun.lower():
        # gets the npc's dialogue
        npc_name = rooms[current_room]['npc']
        npc = dialogue.get(npc_name)

        if npc:
            print(npc['greeting'])

            print('Choose a question to ask:')

            # prints the dialogue menu in a numbered list
            for index, question in enumerate(npc['questions'].keys(), start=1):
                print(f'[{index}] {question}')
            print('[9] Exit')

            while True:
                try:
                    choice_index = int(input('> '))
                    if choice_index == 9:
                        break
                    if 1 <= choice_index <= len(npc['questions']):
                        question_key = list(npc['questions'].keys())[choice_index - 1]
                        print(npc['questions'][question_key])
                    else:
                        print('Invalid choice. Enter a number from the menu above.')
                except ValueError:
                    print("Invalid input. Please enter a number from the menu above.")
    else:
        print(f"There's no one here to talk to named {noun.capitalize()}.")


def handle_take(noun, current_room, rooms, inventory):
    if noun == "":
        print("You need to be more specific.")
    elif 'item' in rooms[current_room].keys() and rooms[current_room]['item'] == noun.lower():
        inventory.append(rooms[current_room]['item'])
        print(f'You take the {noun}.')
        del rooms[current_room]['item']
    else:
        print(f'You look around and you don\'t see one of those.')


# def handle_look(current_room, rooms):
#     print()


def handle_inventory(inventory):
    # checks if inventory is empty
    if not inventory:
        print('You aren\'t carrying anything.')
    else:
        print(f'Inventory: {inventory}')


# object_descriptions = {}

containers = {
    'fridge': {
        'open': 'no',
        'locked': 'no',
        'item': 'ice cold beer'}
}

rooms = {
    'living room': {
        'description': 'You\'re in your living room. Your DAD is on the couch watching Fox News.'
                       ' The KITCHEN is to your LEFT and your ROOM is to the RIGHT.',
        'left': 'kitchen',
        'right': 'bedroom',
        'npc': 'dad',
        'item': 'ice cold beer'

    },

    'kitchen': {
        'description': 'In the kitchen, you can smell dad cooking some chicken fried rice. '
                       'Around you is the FRIDGE.',
        'right': 'living room',
        'container': 'fridge',
        'object': 'fridge'
    },

    'bedroom': {
        'left': 'living room',
        'description': 'Your room is pretty tidy. You see your BED. It looks pretty damn comfy.',
        'object': 'bed'
    }
}

dialogue = {
    'dad': {
        'greeting': 'Hey son, can you fetch me that beer in the FRIDGE? '
                    'It\'s next to the leftovers. I\'m absolutely parched.',
        'questions': {
            'How are you': 'I\'m good, just relaxing here.',
            'What are you doing?': 'Just watching TV and enjoying my evening.',
            'Got any advice?': 'Always be kind and thoughtful to others.'
        }
    }
}

# List to track inventory
inventory = []

# Tracks current room
current_room = 'living room'

# List of vowels
vowels = ['a', 'e', 'i', 'o', 'u']
previous_room = current_room
print(rooms[current_room]['description'])

while True:
    if current_room != previous_room:
        print(rooms[current_room]['description'])
        previous_room = current_room

    user_in = input('> ')

    # split input on the first whitespace to separate the verb and the remaining input
    split_input = user_in.strip().split(' ', 1)

    # check if there is a verb and noun
    if len(split_input) == 2:
        verb, noun = split_input
        verb = verb.lower()
        noun = noun.lower()
    else:
        # if there's no whitespace in the input, the user might have only entered a verb
        verb = user_in.strip().lower()
        noun = ""

    if verb.lower() == 'exit':
        print("Exiting the game. Goodbye!")
        break

    if verb.lower() == 'open':
        handle_open(noun, current_room, rooms, containers, vowels)

    if verb.lower() == 'talk':
        handle_talk(noun, current_room, rooms, dialogue)

    if verb.lower() == 'take':
        handle_take(noun, current_room, rooms, inventory)

    if verb.lower() == 'go':
        handle_go(noun, current_room, rooms)

    if verb.lower() == 'inventory':
        handle_inventory(inventory)
