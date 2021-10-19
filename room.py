''' Arielle Slatus
    CS5001
    Homework 7
    December 5, 2019

    Room
'''

MAX_INVENTORY_WEIGHT = 10

'''class: Game
    Description: this class encapsulates the entire functionality of the game.
    To begin gameplay, walking_around() must be called. This then runs
    continuously until the player decides to quit the game. Rooms, Items,
    Puzzles, and Monsters are all read from .txt files and stored as objects in
    lists. Throughout the game, the player can walk from room to room. The
    player can also look at items in the rooms, pick the items up, carry them
    around with them, and drop them wherever they choose. When the player
    encounters a puzzle or monster, they can use items to neutralize them.
    When they quit the game, their total points will be calculated based on
    how many items they have in their inventory.
'''

class Game:

    def __init__(self):
        '''This initialization of Game stores lists of item objects, room
            objects, and puzzle objects. It also sets self.start to be the
            first room object in the list.
        '''
        self.items = self.get_items() # gets list of item objects
        self.rooms = self.get_rooms(self.items) # gets list of room objects
        # gets list of puzzle objects
        self.puzzles = self.read_puzzles(self.items, self.rooms) 
        self.start = self.rooms[0] # room1, the courtyard

    def get_items(self):
        '''This function opens, reads, and closes the aquest_items.txt file and
            parses it so that each item line becomes an item object.
        '''
        try:
            infile = open('aquest_items.txt', 'r')
            items = infile.readlines()
            infile.close()
        except OSError:
            print('Error reading file')
        items.pop(0) # get rid of metadata line
        items_list = []
        for item in items:
            item_info = item.strip('\n').split('|')
            # instantiate item object
            item_ob = Item(number = item_info[0], name = item_info[1],
                           description = item_info[2],
                           weight = int(item_info[3]),
                           value = int(item_info[4]), use = int(item_info[5]))
            items_list.append(item_ob)
        return items_list # list of item objects

    def get_rooms(self, items_list):
        '''This function opens, reads, and closes the aquest_rooms.txt file and
            parses it so that each room line becomes a room object. It also
            places items objects into their appropriate rooms.
        '''
        try:
            infile = open('aquest_rooms.txt', 'r')
            rooms = infile.readlines()
            infile.close()
        except OSError:
            print('Error reading file')
        rooms.pop(0) # gets rid of metadata line
        rooms_list = []
        for room in rooms:
            room_info = room.strip('\n').split('|')
            adjacent_strings = room_info[3].split(' ') # these nums are strs
            adjacent_ints = []
            for string in adjacent_strings:
                num = int(string) # make ints
                adjacent_ints.append(num) # same list, but ints
            # instantiate room objects
            room_ob = Room(number = int(room_info[0]), name = room_info[1],
                           description = room_info[2],
                           adjacent = adjacent_ints)
            if room_info[6] != 'None': # there are items in the room
                items = room_info[6].split(',')
                for item in items_list:
                    if item.name in items:
                        room_ob.add_item(item) # place items in room
            
            #room_ob.picture = room_info[7]
            rooms_list.append(room_ob)
        return rooms_list # list of room objects

    def read_puzzles(self, items_list, rooms_list):
        '''This function opens, reads, and closes the puzzles_n_monsters.txt
            file and parses it so that each puzzle line becomes a puzzle object.
            Some puzzle lines contain monsters, a subclass of puzzle. The
            monsters are initialized as objects separately from the puzzles.
            Items are added to the monsters and puzzles as solutions and the
            mosnters and puzzles are placed in rooms.   
        '''
        try:
            infile = open('puzzles_n_monsters.txt', 'r')
            puzzles = infile.readlines()
            infile.close()
        except OSError:
            print('Error reading file')
        puzzles.pop(0) # gets rid of metadata line
        puzzles_list = []
        for puzzle in puzzles:
            puzzle_info = puzzle.strip('\n').split('|')
            target_room = puzzle_info[5].split(' ') # turn it into list
            solution_item = puzzle_info[4]
            if puzzle_info[7] != '*': # then not just a puzzle, but a monster
                # instantiate monster object
                monster_ob = Monster(name = puzzle_info[0], active = True,
                                     description = puzzle_info[1],
                                     effect = puzzle_info[6],
                                     attack = puzzle_info[8])
                for room in rooms_list:
                    if str(room.number) == target_room[1]: # a number
                        monster_ob.target = room
                        room.add_puzzle(monster_ob)
                item = self.get_solution(solution_item, items_list, monster_ob)
                monster_ob.solution = item # attach item to monster
                item.puzzle = monster_ob # attach monster to item
                puzzles_list.append(monster_ob)
            else:
                # instantiate puzzle object
                puzzle_ob = Puzzle(name = puzzle_info[0],
                                   description = puzzle_info[1],
                                   effect = puzzle_info[6])
                if 'Room' in target_room: # only setting rooms as targets
                    for room in rooms_list:
                        if str(room.number) == target_room[1]: # a number
                            puzzle_ob.target = room # attach room to puzzle
                            room.add_puzzle(puzzle_ob) # attach puzzle to room
                    item = self.get_solution(solution_item, items_list,
                                                      puzzle_ob)
                    puzzle_ob.solution = item # attach item to puzzle
                    item.puzzle = puzzle_ob # attach puzzle to item
                puzzles_list.append(puzzle_ob)
        return puzzles_list # list of monster objects and puzzle objects    
        
    def get_solution(self, solution_item, items_list, puz_mon_ob):
        '''This function iterates through a light of item objects and looks
            to see if the name of one of those items matches the name of
            the string solution_item. If one does match, the item object
            is returned.
        '''
        for item in items_list:
            if item.name == solution_item: # name of object vs. string
                return item

    def walking_around(self):
        '''This function runs the framework of the game. The majority of the
            function is nexted in a while loop that runs until the user quits.
            The game starts in the variable self.start, with an empty inventory,
            and an inventory weight of 0. The points counter also starts at 0.
        '''
        room = self.start # the courtyard
        inventory = [] # initially empty list
        inventory_weight = 0 # initialize as 0
        points = 0 # initialize as 0
        play = True
        while play:
        
            print('\nYou are now in the: ' + room.name)
            
            desc = room.contextual_description() # changes depending on 
            print(desc) # whether a puzzle is blocking the full description
            for item in room.items:
                print('A ' + item.name + ' is here in the room.')
            
            choice = input('===\nEnter N, S, E, or W to move in those' +
                           'directions.\nI for Inventory, L to Look at' +
                           'something, U to Use an item.\nT to Take an ' +
                           'item, D to Drop an item, or '
                           + 'Q to Quit and exit the game.\n' + 'Your choice: ')

            choice = choice.upper()
            
            if choice == 'N' or choice == 'S' or choice == 'E' or choice == 'W':
                room = self.walk(room, choice) # update room
                continue
            elif choice == 'I':
                self.print_inventory(inventory) # report inventory
                continue
            elif choice == 'L':
                description = self.look(room) # report item description
                print(description + '\n======================================' +
                      '=====')
            elif choice == 'U':
                updated_adjacencies = self.use_item(inventory, room)
                if updated_adjacencies != '': # adjacent_rooms has been updated
                    room.adjacent_rooms = updated_adjacencies 
            elif choice == 'T':
                new_item = self.take_item(room) # get an item object
                if new_item != '': # an item object was returned
                    inventory_weight, can_hold = self.check_weight(new_item,
                                                                   inventory,
                                                              inventory_weight)
                    if can_hold == True: # player can carry the item
                        inventory.append(new_item) # add item to inventory
                        points += new_item.value # add to overall points
                        print('SUCCESS! You now have the ' + new_item.name +
                              ' in your inventory.')
                        room.remove_item(new_item) # remove from room object
                    else:
                        print('Carrying too much weight. Cannot add ' +
                              new_item.name)
                    continue
            elif choice == 'D':
                drop = input('What item would you like to drop? ')
                drop = drop.title() # get updated inventory weight
                dropped_item, inventory_weight = self.drop_item(drop, room,
                                                                inventory,
                                                           inventory_weight)
                if dropped_item != '':
                    print('You dropped the ' + dropped_item.name + ' in the '
                          + room.name)
                    points -= dropped_item.value # subtract value from points
            elif choice == 'Q': # quit
                if points <= 10:
                    rating = 'rookie explorer'
                elif 10 < points <= 100:
                    rating = 'seasoned pathfinder'
                elif points > 100:
                    rating = 'expert adventurer'
                print('Your score is: ', points, '\nYour rating is: ',
                      rating, '\nThank you for playing. Goodbye.')
                play = False # end loop
                return 
            else:
                continue
        
    def walk(self, room, direction):
        '''Thus function is called when the player wants to walk into a new
            room. The function takes the player's input of either N, S, E, or W
            as a parameter, as well as the current room that the player is in.
            The function then determines whether the path forward is open,
            blocked, or nonexistent and calls additional functions accordingly.
            The updated room object is returned.
        '''
        if direction == 'N': # north
            if room.adjacent_rooms[0] > 0: # doorway
                room_number = room.adjacent_rooms[0]
                new_room = self.enter_new_room(room_number) # get new room
            elif room.adjacent_rooms[0] < 0: # puzzle in the way
                new_room = self.blocked_path(room)
            else:
                new_room = self.wrong_direction(room) # no doorway
        elif direction == 'S': # south
            if room.adjacent_rooms[1] > 0: # doorway
                room_number = room.adjacent_rooms[1]
                new_room = self.enter_new_room(room_number)# get new room
            elif room.adjacent_rooms[1] < 0: # puzzle in the way
                new_room = self.blocked_path(room)
            else:
                new_room = self.wrong_direction(room) # no doorway
        elif direction == 'E': # east
            if room.adjacent_rooms[2] > 0: # doorway
                room_number = room.adjacent_rooms[2]
                new_room = self.enter_new_room(room_number) # get new room
            elif room.adjacent_rooms[2] < 0: # puzzle in the way
                new_room = self.blocked_path(room)
            else:
                new_room = self.wrong_direction(room) # no doorway
        elif direction == 'W':# west
            if room.adjacent_rooms[3] > 0: # doorway
                room_number = room.adjacent_rooms[3]
                new_room = self.enter_new_room(room_number) # get new room
            elif room.adjacent_rooms[3] < 0: # puzzle in the way
                new_room = self.blocked_path(room) 
            else:
                new_room = self.wrong_direction(room) # no doorway
        return new_room # updated room object

    def enter_new_room(self, room_number):
        '''This function moves a player from their current room to it's adjacent
            room. The new room object is returned.
        '''
        for room in self.rooms:
            if room.number == room_number: # match name to element from list
                new_room = room
                return new_room # return room object

    def blocked_path(self, room):
        '''This function is called when a player's path is blocked by a puzzle
            or monster. It determines the obstacle in the player's way and
            returns the current room object, unchanged.
        '''
        for puzzle in room.puzzles:
            obstacle = puzzle
        print('You cannot go in that direction because the ' + obstacle.name
              + ' is blocking your path.')
        return room # object

    def wrong_direction(self, room):
        '''This function simply prints to the player that they have attempted
            to walk in the wrong direction. It returns the room object,
            unchanged.
        '''  
        print('\n\n-----------> You cannot go in that direction! ' +
              '<-----------\n\n')
        return room

    def use_item(self, inventory, room):
        '''This function asks the player what item in their inventory they want
            to use. If their input is not the name of an item in their
            inventory, the function returns an empty string. Otherwise, the
            function checks to see if that item has use remaining. If it does,
            then the function checks to see if using the item solves a puzzle
            in the current room. If so, the rooms effects are reversed and the
            rooms updated adjacency list is returned.
        '''
        use = input('What item do you want to use? ')
        use = use.title()
        for item in inventory:
            if item.name == use: # check names of item objects
                remaining = item.has_use_remaining() # True or False
                if remaining == True:
                    print('Using the ' + item.name)
                    solve = item.use(room) 
                    if solve == True: # puzzle has been solved
                        for puzzle in room.puzzles:
                            defeated = puzzle.name
                        print('SUCCESS! You used the ' + item.name + ' on the '
                              + defeated)
                        room.reverse_effects() # uncovers room description &
                        return room.adjacent_rooms # updates adjacent rooms
                    else:
                        print('You used the ' + item.name +
                              ' but it had no effect.')  
                        return '' # item was not the solution to rooms puzzle
                else:
                    print('The ' + item.name + 'has no use left.')
                    return '' # item has been used up
        print('You do not have that item in your inventory.')
        return '' # do not have access to that item
                
    def take_item(self, room):
        '''This function first asks the player what item they would like to
            take. If their response is the name of an item in the room, that
            item object is returned. Othwerwise, the function returns an empty
            string.
        '''
        take = input('Take what item? ')
        take = take.title()
        for item in room.items:
            if item.name == take: # match name to string  
                return item # the item object
        print('Sorry, that item is not in the room.')
        return ''

    def check_weight(self, item, inventory, inventory_weight):
        '''This item takes an item object, the inventory list, and the current
            inventory weight as parameters. The function checks to see if the
            current inventory weight in addition the weight of the new item
            object would exceed the maximum inventory weight. If so, the
            inventory weight is returned, unchanged, along with the boolean
            False. If not, then weight of the item is added to the total
            inventory weight, which is returned, updated, along with the boolean
            True.
        '''
        new_weight = item.weight
        if inventory_weight + new_weight <= MAX_INVENTORY_WEIGHT: 
            inventory_weight += new_weight # total + new
            return inventory_weight, True
        else:
            return inventory_weight, False    
            
    def print_inventory(self, inventory):
        '''This function checks to see if the length of the inventory list is
            equal to zero. If so, it lets the player know that they are not
            currently carrying any items. Otherwise, it prints out the name of
            each item in the inventory list.
        '''
        if len(inventory) == 0: # empty
            print('You are not currently carrying any items.')
        else:
            print('You are carrying:')
            for item in inventory:
                print(item.name)

    def look(self, room):
        '''This funciton first asks the player what they would like to look at.
            If their response is not the name of an item in the room, they are
            told so. Otherise, the function returns the description of the item.
        '''
        look = input('Look at what? ')
        look = look.title()
        for item in room.items:
            if item.name == look: # item is in the room
                print('You examine the ' + item.name + ':')
                return item.description
        print('That item is not in this room.')
        
    def drop_item(self, drop, room, inventory, inventory_weight):
        '''This function first checks to see if the player's input is the
            name of an item currently in the player's inventory. If so, the
            item object is removed from the inventory list and added to the
            current room object. The weight of the item is subtracted from the
            inventory weight, which is returned along with the dropped item
            object. If the player's input was not the name of an iten in their
            inventory, then the funciton returns an empty string along with the
            unchanged inventory weight.
        '''
        for item in inventory:
            if item.name == drop:
                inventory.remove(item) # remove from list
                room.add_item(item) # add to room object
                inventory_weight -= item.weight # update inventory weight
                return item, inventory_weight      
        print('You do not currently have that item in your inventory.')
        return '', inventory_weight
       

'''
    class: Room
    Description:
    This class encapsulates all of the behavior for the "areas" in our
    virtual world. A room is a general idea; rooms might be anywhere
    the player can explore by stepping into them (e.g. closets, boxes)
    Each room has a description and can contain items. Some rooms
    may have a puzzle to solve or a "monster" (our monsters are cute,
    furry animals or toys) that protect the room. If a monster or puzzle
    is present, the user must "deactivate" said puzzle/monster before
    the full room description is presented to them
'''    
class Room:
    def __init__(self, number = 0, name = 'n/a',
                 description = 'trapped!', adjacent = [], picture = ''):
        self.name = name
        self.number = number
        self.description = description
        self.adjacent_rooms = adjacent
        self.picture = picture
        self.items = []
        self.puzzles = []
        self.monsters = []
    def add_item(self, item): # add an item to the room
        self.items.append(item)
    def remove_item(self, item): # remove an item from the room
        self.items.remove(item)
    def add_puzzle(self, puzzle): # add a puzzle to the room
        self.puzzles.append(puzzle)
    def add_monster(self, monster): # add a monster to the room
        self.monsters.append(monster)
    def has_items(self):            # answer if the room has items or not
        return not (len(self.items) == 0)
    def has_puzzle(self):           # does the room have puzzles?
        return not (len(self.puzzles) == 0)
    def reverse_effects(self):      # reverse effects of puzzle/monster
        for i in range(len(self.adjacent_rooms)):
            if self.adjacent_rooms[i] < 0: # blocked by a puzzle or monster
                self.adjacent_rooms[i] = 0 - self.adjacent_rooms[i] # make it open
    def contextual_description(self):
        if self.has_puzzle(): # puzzle blocks regular description. 
            for each in self.puzzles:
                if (each.target == self and
                    each.active and
                    each.affects_target):
                    return each.do_effect()
        # if no puzzles/monsters are active, return regular description
        return self.description 
    def __str__(self):
        return (str(self.number) + ':' + self.name + ':' + self.description)

'''
    class: Item
    Description:
    This class encapsulates all of the behavior for the "things" in our
    rooms. Items can be collected by the player by Taking them during
    their quest. Items also have a description that players can see when
    they Look at the item. Players can also Drop or Use items
    For this prototype, puzzles and monsters CAN be attached to items
    (just like rooms) but the framework doesn't fully support the
    resolution of solutions for those puzzles on objects yet.
    reverse_effects() is future work, so you can leave it as a "pass"
    in your code
'''
class Item:
    def __init__(self, number = 0, name = 'n/a',
                 description = '', weight = 0, value = 0, use = 0):
        self.name = name
        self.number = number
        self.description = description
        self.weight = weight
        self.value = value
        self.use_remaining = use
        self.puzzle = ''

    # does the item have any use left, or is it used up?
    def has_use_remaining(self):
        if self.use_remaining > 0:
            return True
        return False

    # answer if the Item has a puzzle or not
    def has_puzzle(self):
        if self.puzzle == '':
            return False
        else:
            return True
           
    # try to use the item (on a puzzle or monster)
    def use(self, room):
        self.use_remaining -= 1
        if self.has_puzzle() == True:
            for puzzle in room.puzzles:
                if puzzle == self.puzzle:
                    solved = puzzle.try_to_solve(self)
                    return solved
        return False
        
    def __str__(self):
        return str(self.number + ':' + self.name + ':' + self.description)
        
'''
    class: Puzzle
    Description:
    This class encapsulates all of the behavior for the challenges in our
    rooms. Puzzle is a general term...right now it's not some hard problem
    to solve, but currently the use of some ITEM to "neutralize" the problem
    or monster the player encounters. E.g. a glass of water might neutralize
    a FIRE puzzle
    If puzzles are active, they occlude the regular description of a room
    Items neutralize puzzles and deactivate them
'''
class Puzzle:
    def __init__(self, name = 'n/a', description = '', target = '',
                 active = True, affects_target = True,
                 solution = '', effect = ''):
        self.name = name
        self.description = description
        self.active = active
        self.affects_target = affects_target
        self.solution = solution
        self.target = target
        self.effect = effect
    def activate(self):
        self.active = True
    def deactivate(self):
        self.active = False
    def is_active(self):
        return self.active
    def do_effect(self):
        return self.effect
    def try_to_solve(self, solution):
        if solution == self.solution:
            self.deactivate()
            return True
        return False

'''
    class: Monster
    Description:
    This class is a subtype of Puzzle that can "attack" the user.
    All of our monsters are soft and furry creatures so they can't
    really hurt the user (no need for inducing PTSD in a computer game)
    Like their superclass, they occlude the regular room description
    until they are neutralized
'''
class Monster(Puzzle):
    def __init__(self, name = 'n/a',description = '', target = '',
                 active = True, affects_target = True,
                 solution = '', effect = '',
                 can_attack = True, attack = 'Cotton Balls'):
        super().__init__(name, description, target,
                         active, affects_target, solution, effect)
        self.can_attack = can_attack
        self.attack = attack
    def do_effect(self):
        return self.effect + '\n' + self.do_attack()
    def do_attack(self):
        return self.name + ' ' + self.attack
    def defeated(self):
        return 'The ' + self.name + ' has been defeated. It is not moving.'
