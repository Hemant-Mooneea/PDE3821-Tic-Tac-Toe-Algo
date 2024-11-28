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
