# -*- coding: utf-8 -*-
#by Alex Stroev

from __future__ import division

import numpy as np

import itertools
import sys

class Field(object):
    
    @classmethod
    def init(cls, width, height):
        cls.width = width
        cls.height = height
        cls.field = np.zeros((width, height)) 
    
    @classmethod
    def clear(cls):
        cls.field = np.zeros((cls.width, cls.height))
    

class PoliBase(object):
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.max_x = Field.width - self.width + 1
        self.max_y = Field.height - self.height + 1


class PoliSquare(PoliBase):
    
    def __init__(self, width, height):
        super(PoliSquare, self).__init__(width, height)
        
    def check_and_place(self, x, y):
        if x + self.width > Field.width or y + self.height > Field.height:
            return -1
        for i in range(x, x+self.width):
            for j in range(y, y+self.height):
                if Field.field[i][j] == 0:
                    Field.field[i][j] = 1
                else:
                    return -1
        return 0
        
class PoliL(PoliBase):

    def __init__(self, width, height):
        super(PoliL, self).__init__(width, height)
        
        #possible optimization: dependence on actual rotation
        self.max_x = max(self.max_x, Field.width - self.height + 1)
        self.max_y = max(self.max_y, Field.height - self.width + 1)
        
    def check_and_place(self, x, y, rotation):
        #x to the right, y to the top
        if rotation == 0:
            #\_ shape
            p1 = PoliSquare(1, self.height) 
            p2 = PoliSquare(self.width - 1, 1) 
            if p1.check_and_place(x, y) < 0:
                return -1
            if p2.check_and_place(x + 1, y) < 0:
                return -1
        elif rotation == 1:
            #_| shape
            p1 = PoliSquare(self.height, 1) 
            p2 = PoliSquare(1, self.width - 1)  
            if p1.check_and_place(x, y) < 0:
                return -1
            if p2.check_and_place(x + self.height - 1, y + 1) < 0:
                return -1
        elif rotation == 2:
            #^| shape
            p1 = PoliSquare(1, self.height) 
            p2 = PoliSquare(self.width - 1, 1)  
            if p1.check_and_place(x + self.width - 1, y) < 0:
                return -1
            if p2.check_and_place(x, y + self.height - 1) < 0:
                return -1
        else:
            #|^ shape
            p1 = PoliSquare(self.height, 1) 
            p2 = PoliSquare(1, self.width - 1)
            if p1.check_and_place(x, y + self.width - 1) < 0:
                return -1
            if p2.check_and_place(x, y) < 0:
                return -1
        return 0
            
        
        
        
def solve_poliomino(polis):
    states = []
    #each element of 'states' is a list of all possible positions (and rotations)
    #of a corresponding poliomino
    for poli in polis:        
        if type(poli) is PoliSquare:
            states.append(list(itertools.product(range(poli.max_x), range(poli.max_y))))
        else:
            #third coordinate is rotation
            states.append(list(itertools.product(range(poli.max_x), range(poli.max_y), range(4))))
        
    #combination of all possible states is a placement
    placements = itertools.product(*states)

    #check all placements if they are possible
    for placement in placements:
        Field.clear()
        for poli, state in zip(polis, placement):
            if poli.check_and_place(*state) < 0:
                break
        else:
            print('Possible!')
            return True
    print('Impossible')
    return False

def parse_input_and_run(s):    
    
    fw = int(s[s.find('(')+1 : s.find(',')])
    
    fh = int(s[s.find(',')+1 : s.find(')')])
    
    Field.init(fw, fh)
    
    qs = s[s.find('2.')+2 : s.find('3.')]
    
    polis = []
    
    while qs.find('((') > -1:
        pw = int(qs[qs.find('((')+2 : qs.find(',')])
        ph = int(qs[qs.find(',')+1 : qs.find('),')])
        t = qs.find('),')
        pn = int(qs[t+2 : qs.find(')', t+2)])
        for _ in range(pn):
            polis.append(PoliSquare(pw, ph))
        qs = qs[qs.find(')', t+2) + 2 : ]
        
    qs = s[s.find('3.')+2 : ]

    while qs.find('((') > -1:
        pw = int(qs[qs.find('((')+2 : qs.find(',')])
        ph = int(qs[qs.find(',')+1 : qs.find('),')])
        t = qs.find('),')
        pn = int(qs[t+2 : qs.find(')', t+2)])
        for _ in range(pn):
            polis.append(PoliL(pw, ph))
        qs = qs[qs.find(')', t+2) + 2 : ]

    solve_poliomino(polis)

def test():
    
    s = """ 
1. (3, 5)    
2. [((2, 2), 1)]
3. [((3, 2), 1), ((2, 2), 2)]
"""    
    #from task
    parse_input_and_run(s)

    #should not be possible
    Field.init(4, 4)
    polis = []
    polis.append(PoliL(3, 4))
    polis.append(PoliL(2, 3))
    polis.append(PoliL(2, 2))
    polis.append(PoliL(2, 2))
    solve_poliomino(polis)
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please specify input file, for example: ')
        print('>>> python poliomino.py input.txt')
    else:
        with open(sys.argv[1], 'r') as file:
            s = file.read()
            parse_input_and_run(s)