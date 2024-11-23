
#SECTION: Detecting grid cells and extracting details

def captureGridAndConvertToArray():

    #? using opencv to capture frame of grid
    #! add opencv code here


    #? use yolo model or whatever to scan grid cells, separate them using bounding boxes and label them as coordinates 
    #? such as (0,0), (0,1), etc and determine whether its empty, filled with X or O

    #! add code here for detection


    """ Each of those coordinates will then be assigned a value depending on what they contain
    # a dictionary could be used to store these key-value pairs as such: (0,0):0 (empty), (0,1):1 (filled with X)
    ? 0: empty grid cell
    ? 1: represents X
    ? 2: represents O
    """

    #example of said dictionary
    coordinateValueDict = {
        (0, 0): 0,  
        (0, 1): 1,  
        (0, 2): 2, 
        (1, 0): 0,
        (1, 1): 2,
        (1, 2): 1,
        (2, 0): 0,
        (2, 1): 0,
        (2, 2): 1,
        #etc
    }

    #*default starting grid, will get updated as game proceeds
    grid = [[0,0,0],
            [0,0,0],
            [0,0,0]]

    #* updating the grid as per the dictionary
    for (row,col), value in coordinateValueDict.items():
        grid[row][col] = value

    return grid
