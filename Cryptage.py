import os

def createkey():
    key = os.urandom(16)
    return key

def crypting(file):
    
    