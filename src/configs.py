import os
class Constants_: 
    MINE = 'X'
    SPACE = ' '
    ZERO_TILE = '0'
    FLAG = 'F' 
    UNFLAG = 'UF'

def clear_console(): 
    clear = lambda: os.system('cls')
    return clear() 
