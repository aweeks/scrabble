import sys
import cmd
from scrabble import *
from index import *

class Interface(cmd.Cmd):
    def do_print(self, line):
        print board

    def do_play(self, line):
        args = line.split()
        row = int(args[0]) - 1
        col = int(args[1]) - 1
        if args[2] == "r":
            direction = board.RIGHT
        if args[2] == "d":
            direction = board.DOWN

        s = args[3]

        board.play(row, col, direction, s)
        print board 
    
    def do_search(self, line):
        letters = line
        for score, p in board.best_plays(letters, n=10):
            print "SCORE:", score
            board.print_play(*p)



with open(sys.argv[1], 'r')  as f:
    words = f.read().splitlines()

dictionary= Node()

for w in words:
    dictionary.insert(w)       

board = Board(dictionary)

if __name__ == '__main__':
    Interface().cmdloop()



#board = Board(dictionary)
#board.play(1,1,board.RIGHT, "ab")
#board.play(1,3,board.DOWN, "sell")
#board.play(4,2,board.RIGHT, "pease")
#board.play(1,6,board.DOWN, "cat")

#for p in board.continuations(0,2, board.DOWN, dictionary, "abbsyftnuf", "", False):
#    print p

#for p in board.all_plays("aengqzu"):
#    print p
