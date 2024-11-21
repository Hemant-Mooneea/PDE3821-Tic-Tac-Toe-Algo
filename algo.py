import random

def getShape():
    # If random is 0, then return 'X', else return 'O'
    if(random.randint(0,1) == 0):
        return 'X'
    return 'O'
    
def main():
    BOT_SHAPE = getShape()
    print(BOT_SHAPE)
    
main()
    