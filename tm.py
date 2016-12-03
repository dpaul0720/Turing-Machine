#!/usr/bin/env python2.7

import sys
import os

cmdrules = sys.argv[1]
cmdinput = sys.argv[2]

rules = open(cmdrules)          # open the rules file

title = rules.readline()
title = title.strip()

print title


ia = rules.readline()
ialpha=[x.strip() for x in ia.split(',')]               # parsing the input alphabet and putting them into an array

ea = rules.readline()
ealpha=[w.strip() for w in ea.split(',')]       # parsing the extra symbols beyond input alphabet
ealpha.append('_')      # adding the _ character to the tape alphabet

tapealpha = ealpha+ialpha   # creating the whole tape alphabet

s = rules.readline()
states=[y.strip() for y in s.split(',')]        # parsing the states and putting into an array




first = rules.readline()
first = first.strip()                                           # getting the first initial state into a variable


accept = rules.readline()
accept = accept.strip()         # parsing the last(accepted) state

reject = rules.readline()
reject = reject.strip()


transition = []

rulecount = 1
for line in rules:          # printing the rules and appending them to a list
        print "Rule #" + str(rulecount) + " : " + line,
        line = line.replace('|', ",")
        transition.append([str(u.strip()) for u in line.split(',')])
        rulecount += 1


print '\n'
inputfile = open(cmdinput)


for inputlines in inputfile.readlines():    # loop through the strings in the input file
    stack = []      # reset the stack
    ifrulefound = 0
    i = 0
    numbertrans = 0
    step = 0
    ruleno = 0
    currentst = first
    inputlines = inputlines.strip()
    inputlines = inputlines + '_'
    print "Tape: ", inputlines
    tape = list(inputlines)

    while True: # loop through the characters in the each input string
        if tape[i] not in tapealpha:      #check for incorrect input
            print "an input character was not in the specified input alphabet provided"
            print '\n'
            break
        if currentst not in states:
            print "The current state is not in provided list of states"
            print '\n'
            break
        elif numbertrans > 200:         # check if the machine performed too many transitions
            if tape[-1] == '_':
                tape.pop()
            tape=''.join(tape)
            print 'Error', ":", tape
            print '\n'
            break
        else:
            ruleno = 0
            foundrule = 0
            stacklength = len(stack)
            for transc in transition:       # loop through the rules
                ruleno = ruleno + 1

                if currentst == transc[0] and tape[i] == transc[1]:   #checking to find state and input value
                    prestate = currentst
                    currentst = transc[2]
                    step += 1
                    foundrule += 1
                    numbertrans += 1
                    p = i
                    if transc[4] == 'R':        # if statement for correct printing at the end
                        print 'Step #', step, '@ Current Tape Head Index ', i, '#', 'Rule Number', ruleno, ':', str(prestate), tape[i], '|',  str(currentst), transc[3], i+1
                        tape[i] = transc[3]
                        i += 1
                    else:
                        print 'Step #', step, '@ Current Tape Head Index ', i, '#', 'Rule Number', ruleno, ':', str(prestate), tape[i], '|',  str(currentst), transc[3], i-1
                        tape[i] = transc[3]
                        i -= 1
                    break


            if currentst == reject:     # Reject, Accept, and Error Testing
                if tape[-1] == '_':
                    tape.pop()
                tape =''.join(tape)
                print 'Rejected' , ":", tape
                print '\n'
                break
            elif currentst == accept:
                if tape[-1] == '_':
                    tape.pop()
                tape=''.join(tape)
                print 'Accepted', ":", tape
                print '\n'
                break
            elif foundrule == 0:
                if tape[-1] == '_':
                    tape.pop()
                tape=''.join(tape)
                print 'Error', ":", tape
                print '\n'
                break

inputfile.close()       # Closing files I opened
rules.close()

