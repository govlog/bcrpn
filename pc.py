#!/usr/bin/python

# coding : utf-8

import sys
import time
import readline
import rpn as rp

ver = '1.0'

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
        print "debug is now set to",debug

    elif command == 'show':
        print var

    elif command == 'help' or command == '!h':
        print "debug   : toggle debug on/off"
        print "show    : show variables"
        print "quit    : exit calc"
        print "version : show version number"

    elif command == 'version' or command == '!v':
        print "calc version",ver

print "Welcome to calc",ver,"use help for command list or quit to exit."

var={}

#t=0

while 1:
    
    try:
        user_input = raw_input('> ')
    except KeyboardInterrupt:
        user_input=''
        print "(ctrl^c) => exit."
        sys.exit(0)

    if user_input:

        cmd=''

        input_arr=list(user_input.rstrip(' ').lstrip(' '))
        input_len=len(input_arr)

        pos=0

        loop=False
        loop_iter=0
        iter_num=0

        while (pos!=input_len):

            c=input_arr[pos]

            if c != ';':

                cmd+=c

            if c == ';' or (pos==input_len-1):

                if ('for' in cmd) and loop==False:
                    (_tmp,iter_num)=cmd.split(' ')
                    iter_num=int(iter_num)
                    loop=True
                    loop_pos=pos
                    loop_iter=0

                elif cmd in commands:
                    cmd_parse(cmd)

                elif '=' in cmd:

                    (v,expr)=cmd.split("=")
                    expr=rp.Infix(expr,var,debug)

                    if expr.get_result():
                        var[v]=expr.result
                        if debug:
                            print v, "<=", var[v]

                elif cmd != '':

                    t = time.time()

                    expr=rp.Infix(cmd,var,debug)

                    if expr.get_result():
                        e = time.time()

                        if debug:
                            print "(time)   "+ '{0:.11f}'.format(e - t)+ "s"
                            print "(result)",expr.result
                        else:
                            print expr.result
                cmd = ''

            if loop == True:

                if pos == input_len - 1:
                    pos=loop_pos
                    loop_iter += 1
                    cmd=''

                if loop_iter >= iter_num:
                    break

            pos+=1

print