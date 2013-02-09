#!/usr/bin/env python
"""
This file is part of a solution to the Mars Rover Exercise
(http://thefundoowriter.com/2009/10/01/the-mars-rover-problem/).

Matthew Baker <mu.beta.06@gmail.com> 2013

This module defines the base class for the RoverDispatcher.

Responsible for interpretting user data into controller data.

"""

import math
import sys

import rovercontroller

class RoverDispatcher(object):

    """This is a base for describing a RoverDispatcher."""
    INSTRUCTIONS = ['L', 'R', 'M']
    HEADINGS = {'E':0, 'N':math.pi/2, 'W':math.pi, 'S':3*math.pi/2}

    def __init__(self, input):
        """Initialise a RoverDispatcher. Parse input according to problem 
        description."""
        self.parse_input(input)

    def parse_input(self, input):
        """Parse input according to problem description."""
        self.input = input.split('\n')[:-1] #null char
        vertex = tuple([int(v) for v in self.input[0].split(' ')] + [0])
        self.controller = rovercontroller.RoverController(((0, 0, 0), vertex))
        self.rovers = []
        self.instructions = []
        #parse and add Rovers
        for line in self.input[1::2]:
            rover = line.split(' ')
            if len(rover) == 3:
                position = tuple([int(v) for v in rover[0:2]] + [0])
                heading = (self.map_user_heading(rover[-1]), math.pi/2)
                self.controller.add_rover(line, position, heading)
                self.rovers.append(line) #rover idd by starting pos and heading
            else:
                raise Exception('Incorrectly specified Rover.')
        #parse instructions        
        self.instructions = [[c for c in line] for line in self.input[2::2]]

    def dispatch(self):
        """Dispatch Rover input to RoverController."""
        for rover, instructions in zip(self.rovers, self.instructions):
            for instruction in instructions:
                if instruction == 'L':
                    self.turn_left(rover)
                elif instruction == 'R':
                    self.turn_right(rover)
                elif instruction == 'M':
                    self.move(rover)
                else:
                    raise Exception('unknown instruction %s' % str(instruction))

    def turn_left(self, rover_id):
        """Turn nominated Rover left."""
        self.controller.turn(rover_id,  math.pi/2, 0)

    def turn_right(self, rover_id):
        """Turn nominated Rover Right."""
        self.controller.turn(rover_id, -math.pi/2, 0)

    def move(self, rover_id):
        """Move the nominated Rover forward 1 position."""
        self.controller.move(rover_id, 1)

    def map_user_heading(self, heading):
        """Map user heading to controller heading."""
        if not heading in self.HEADINGS.keys():
            raise Exception('unknown user heading %s' % str(heading))
        else:
            return self.HEADINGS[heading]

    def map_controller_heading(self, heading):
        """Map controller heading to user heading."""
        if not heading in self.HEADINGS.values():
            raise Exception('unknown controller heading %s' % str(heading))
        else:
            for h in self.HEADINGS.keys():
                if self.HEADINGS[h] == heading:
                    return h

    def render_view(self):
        """Renders view to user."""
        for rover in self.rovers:
            r = self.controller.get_rover(rover)
            heading = self.map_controller_heading(r.heading[0])
            print r.position[0], r.position[1], heading


def main():
    """Main Program.
    Usage: Batch - cat inputfile.txt | python roverdispatcher.py
    Interactive - python roverdispatcher.py"""
    if sys.stdin.isatty():
        input = ''
        vertices = raw_input('Please enter grid vertex: ')
        rover = raw_input('Please enter something else: ')
        input += vertices + '\n'
        input += rover + '\n'
    else:        
        input = sys.stdin.read()

    dispatcher = RoverDispatcher(input)
    dispatcher.dispatch()
    dispatcher.render_view()

if __name__ == '__main__':
    main()