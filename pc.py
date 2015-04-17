#!/usr/bin/python

# coding : utf-8

import sys
import time
import readline
import rpn as rp

ver = '0.1'

commands = ( 'quit' , 'debug' , 'version' , 'help' , 'show' )

debug=True

def completer(text, state):
    options = [x for x in commands if x.startswith(text) and x!=text]
    try:
        return options[state]
    except IndexError:
        return None

readline.set_completer(completer)
readline.parse_and_bind("tab: complete")


def cmd_parse(command):
    
    global debug

    if command == 'quit' or command == '!q':
        sys.exit(0)

    elif command == 'debug' or command == '!d':
        debug=not debug
        print "debug now set to",debug

    elif command == 'show':
        print var

    elif command == 'help' or command == '!h':
        print "show    : show variables"
        print "debug   : toggle debug on/off"
        print "quit    : exit calc"
        print "help    : show this help"
        print "version : show version number"

    elif command == 'version' or command == '!v':
        print "calc version",ver

print "Welcome to calc",ver,"!q to quit , !h for command help."

var={}

t=0
while 1:
    
    try:
        user_input = raw_input('> ')
    except KeyboardInterrupt:
        user_input=''
        print "(ctrl^c) => exit."
        sys.exit(0)

    if user_input:

        go=False
        cmd=''

        for i,c in enumerate(list(user_input)):

            if c != ';':
                cmd+=c
            else:
                go=True

            if i==len(user_input)-1:
                go=True

            if go:

                if cmd in commands:
                    cmd_parse(cmd)

                elif '=' in cmd:

                    (v,expr)=cmd.split("=")
                    expr=rp.Infix(expr,var,debug)

                    if expr.evaluate():
                        var[v]=expr.result
                        if debug:
                            print v, "<=", var[v]

                elif cmd != '':

                    t = time.time()

                    expr=rp.Infix(cmd,var,debug)

                    if expr.evaluate():
                        e = time.time()

                        if debug:
                            print "(time)   "+ '{0:.11f}'.format(e - t)+ "s"
                            print "(result)",expr.result
                        else:
                            print expr.result

                go=False
                cmd=''

print