#!/usr/bin/python

banned_characters = ['%', '<', '"', '\'', '--+', '--', '=', '<script>', '</script', ';', '0x']

def scan(word_to_scan):
    for things in banned_characters:
        #print (things) #debug purposes
        if things in str(word_to_scan):
            return "MALICIOUS"
    return "CLEAN"
            
