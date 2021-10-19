''' Arielle Slatus
    CS5001
    Homework 7
    December 5, 2019

    Adventure Game Unit Test
'''
import unittest
from adventure_game import Game
from room import Room

class GameTest(unittest.TestCase):


    def test_walk(self):
        game = Game()
        room0 = game.rooms[0]
        room1 = game.rooms[1]
        room2 = game.rooms[2]
        room4 = game.rooms[4]
        room5 = game.rooms[5]
        room6 = game.rooms[6]
        room7 = game.rooms[7]

        walk1 = game.walk(room0, 'N')
        walk2 = game.walk(room6, 'N') # path blocked by rabbit
        walk3 = game.walk(room6, 'S')
        # walks north from room0 to room1
        self.assertEqual(walk1, room1)
        # path north is blocked, stays in room6
        self.assertEqual(walk2, room6) # returns same room
        # walks south from room6 to room7
        self.assertEqual(walk3, room7)

    def test_check_weight(self):
        game = Game()
        item1 = game.items[0]
        item2 = game.items[1]
        item3 = game.items[2]
        item4 = game.items[3]
        item5 = game.items[4]
        inventory1 = []
        inventory2 = []
        inventory3 = []
        inventory1.append(item1)
        inventory1_weight = item1.weight
        inventory2.append(item1)
        inventory2.append(item2)
        inventory2.append(item3)
        inventory2_weight = item1.weight + item2.weight + item3.weight
        inventory3.append(item1)
        inventory3.append(item3)
        inventory3.append(item4)
        inventory3_weight = item1.weight + item3.weight + item4.weight       
        
        weight1, boolean1 = game.check_weight(item2, inventory1,
                                              inventory1_weight)
        weight2, boolean2 = game.check_weight(item4, inventory2,
                                              inventory2_weight)
        weight3, boolean3 = game.check_weight(item5, inventory3,
                                              inventory3_weight)
        # adds item to inventory, returns updated inventory weight and True
        self.assertEqual(weight1, inventory1_weight + item2.weight)
        self.assertEqual(boolean1, True)
        # adds item to inventory, returns updated inventory weight and True
        self.assertEqual(weight2, inventory2_weight + item4.weight)
        self.assertEqual(boolean2, True)
        # carrying too much weight to add item4, returns original weight & False
        self.assertEqual(weight3, inventory3_weight)
        self.assertEqual(boolean3, False)


    def test_drop_item(self):
        game = Game()
        room2 = game.rooms[2]
        room3 = game.rooms[3]
        room7 = game.rooms[7]
        item1 = game.items[0]
        item2 = game.items[1]
        item3 = game.items[2]
        item4 = game.items[3]
        inventory1 = []
        inventory2 = []
        inventory3 = []
        inventory1.append(item1)
        inventory1_weight = item1.weight
        inventory2.append(item1)
        inventory2.append(item2)
        inventory2.append(item3)
        inventory2_weight = item1.weight + item2.weight + item3.weight
        inventory3.append(item1)
        inventory3.append(item3)
        inventory3.append(item4)
        inventory3_weight = item1.weight + item3.weight + item4.weight
        
        drop1, weight1 = game.drop_item(item2.name, room3, inventory1,
                                        inventory1_weight) # not in inventory
        drop2, weight2 = game.drop_item(item2.name, room2, inventory2,
                                        inventory2_weight)
        drop3, weight3 = game.drop_item(item4.name, room7, inventory3,
                                        inventory3_weight)
        # returns empty string and same inventory weight
        self.assertEqual(drop1, '') 
        self.assertEqual(weight1, inventory1_weight) 
        # returns item object and updated inventory weight
        self.assertEqual(drop2, item2)
        self.assertEqual(weight2, inventory2_weight - item2.weight)
        # returns item object and updated inventory weight
        self.assertEqual(drop3, item4)
        self.assertEqual(weight3, inventory3_weight - item4.weight)
        
        

def main():
    
    unittest.main(verbosity = 3)
    
main()
