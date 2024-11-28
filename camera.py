import cv2

#? using opencv to capture frame of grid
def captureGrid():

    capture = cv2.VideoCapture(0)
    
    # checking if camera is opened
    if not capture.isOpened():
        print("Error: Could not open video device.")
        exit()
    
    print("Press 'c' to capture a frame, or 'q' to quit.")

    while True:
        # read a frame from the video feed
        ret, frame = capture.read()

        if not ret:
            print("Error: Failed to capture frame.")
            break

        # display the frame
        cv2.imshow("Live Feed", frame)

        # wait for key press
        key = cv2.waitKey(1) & 0xFF

        # press 'c' to capture the frame
        if (key == ord('c')):
            # saving captured frame as captured_frame.jpg
            cv2.imwrite("captured_frame.jpg", frame)
            # press 'q' to quit
        elif (key == ord('q')):
            break

    # release the capture and close windows
    capture.release()
    cv2.destroyAllWindows()


#? use yolo model or whatever to scan grid cells, separate them using bounding boxes and label them as coordinates 
#? such as (0,0), (0,1), etc and determine whether its empty, filled with X or O
#? use the captured_frame.jpg for extracting these details
def extractDetailsFromGrid(image_path):
    
    #! add code here for detection/extraction


    """ Each of those coordinates will then be assigned a value depending on what they contain
    # a dictionary could be used to store these key-value pairs as such: (0,0):0 (empty), (0,1):1 (filled with X)
    ? 0: empty grid cell
    ? 1: represents X
    ? 2: represents O
    """

    #example of said dictionary
    #? we could also use the symbols directly instead of using numbers 0,1,2 as you said
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

    return coordinateValueDict

def ConvertGridToArray():  

    coordinateValueDict = extractDetailsFromGrid('captured_frame.jpg')
    
    #*default starting grid, will get updated as game proceeds
    grid = [[0,0,0],
            [0,0,0],
            [0,0,0]]

    #* updating the grid as per the dictionary
    for (row,col), value in coordinateValueDict.items():
        grid[row][col] = value

    return grid