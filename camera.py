import cv2
import numpy as np
import time

class Camera:
    def __init__(self):
        self.grid_array = []
        self.previous_grid_array = None
        self.grid_size = 360
        
    # isolates the grid from the input image
    def detectGrid(self,image):
        #convert image to grayscale
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        #reduce noise in image, remove unnecessary edges
        blur = cv2.GaussianBlur(grayImage, (5,5), 0)

        #detect edges in image, make grid lines stand out clearly
        edges = cv2.Canny(blur, 50, 150)

        # Find contours (outlines) of grid
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # pick the largest contour since the grid is the one with the largest contour
        largest_contour = max(contours, key=cv2.contourArea)

        # Approximate contour to a polygon
        epsilon = 0.02 * cv2.arcLength(largest_contour, True)
        approx = cv2.approxPolyDP(largest_contour, epsilon, True)

        #if contour has 4 sides it is assumed to be the grid
        if len(approx) == 4:
            # Order the 4 points of the polygon to ensure grid is properly aligned and to apply perspective transform
            pts = np.array([point[0] for point in approx], dtype="float32")
            ordered_pts = self.order_points(pts)

            # transform the grid to a fixed size one, so it's easier to split into smaller cells
            dst = np.array([[0, 0], [self.grid_size - 1, 0], [self.grid_size - 1, self.grid_size - 1], [0, self.grid_size - 1]], dtype="float32")

            # Perspective transform
            matrix = cv2.getPerspectiveTransform(ordered_pts, dst)
            grid = cv2.warpPerspective(image, matrix, (self.grid_size, self.grid_size))
            return grid

        else:
            raise ValueError("Grid not detected. Ensure the grid is clearly visible.")


    # Organizes the 4 corners of the detected grid so they can be used for perspective transformation
    def order_points(self,pts):
        # Separate the corners into top-left, top-right, bottom-right, and bottom-left
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1) # Sum of x + y
        diff = np.diff(pts, axis=1) # Difference of x - y

        rect[0] = pts[np.argmin(s)]  # # Top-left corner (smallest sum)
        rect[2] = pts[np.argmax(s)]  # Bottom-right corner (largest sum)
        rect[1] = pts[np.argmin(diff)]  # Top-right corner (smallest difference)
        rect[3] = pts[np.argmax(diff)]  # Bottom-left corner (largest difference)

        return rect


    # Function to preprocess the image
    def preprocess_image(self,image):
        # turn image into black and white
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

        # make grid lines black and cell content black and everything else white
        _, thresh = cv2.threshold(grayImage, 160, 255, cv2.THRESH_BINARY_INV)  
        return thresh


    # Function to divide the grid into 3x3 cells
    def split_grid(self,image):
        #get height and width of grid
        height, width = image.shape

        #calculate height and width of an individual cell
        cell_height, cell_width = height // 3, width // 3

        #array to store the 9 cells
        cells = []
        
        #loop through rows
        for i in range(3):
            # to store 1 row of 3 cells
            row = []
            #loop through columns
            for j in range(3):
                #extract a single cell using slicing
                cell = image[i * cell_height:(i + 1) * cell_height, 
                            j * cell_width:(j + 1) * cell_width]

                #add cell to the current row
                row.append(cell)
            #add the completed row to the list of cells
            cells.append(row)

        return cells


    # identify the contents of a cell
    def identify_cell_content(self,cell, templates):
        highest_score = 0  # Track the highest match score
        best_label = ""  # Default label if no template matches well enough

        # Compare the cell to each template
        for label, template in templates.items():
            # Check how well the template matches
            res = cv2.matchTemplate(cell, template, cv2.TM_CCOEFF_NORMED)
            max_res = np.max(res)  # Get the maximum score for this template

            # Update the best match if this score is higher than the previous best
            if max_res > highest_score:
                highest_score = max_res
                best_label = label

        # Return the label with the highest score if it is above the threshold; otherwise, "Empty"
        return best_label if highest_score > 0.20 else ""


    # maps grid contents to dictionary and array
    def map_grid(self, cells, templates):
        #loop through each row of cells
        for i, row in enumerate(cells):
            # temporary array for this row in the array
            array_row = []
            #loop through each cell in the row
            for j, cell in enumerate(row):
                #identify what's inside the cell
                content = self.identify_cell_content(cell, templates)
                # add it to array row7
                array_row.append(content)
            #add the completed row to the 2D array
            self.grid_array.append(array_row)
        
        return self.grid_array

    # Initialize templates for X and O
    def load_templates(self):
        template_X = cv2.imread('templates/templateX.png', cv2.IMREAD_GRAYSCALE)
        template_O = cv2.imread('templates/templateO.png', cv2.IMREAD_GRAYSCALE)

        # Resize templates to match cell size
        template_X = cv2.resize(template_X, (105, 75))
        template_O = cv2.resize(template_O, (105, 75))

        # Apply thresholding
        _, template_X = cv2.threshold(template_X, 170, 255, cv2.THRESH_BINARY_INV)
        _, template_O = cv2.threshold(template_O, 170, 255, cv2.THRESH_BINARY_INV)

        return {"X": template_X, "O": template_O}

    # Compare grids to detect changes
    def grid_changed(self, previous, current):
        return previous != current

    #capture a stable decent frame of the grid image
    def captureFrame(self):
        # Load the camera feed or an image
        cap = cv2.VideoCapture(1)
        
        stable_frame = None
        start_time = time.time()  # Record the start time

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame")
                break
            flipped_frame = cv2.flip(frame, -1)
            #show the live feed
            cv2.imshow("Frame", flipped_frame)

            # Check if 5 seconds have passed
            elapsed_time = time.time() - start_time

            if (elapsed_time >=5):
                # Capture a stable frame
                stable_frame = flipped_frame.copy()  
                print("Stable frame captured.")
                break

            # Allow for manual exit (optional)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Process interrupted by user.")
                break

        cap.release()
        cv2.destroyAllWindows()

        return stable_frame


    # capture frame from camera module and feed it to the different functions to extract grid data
    def main(self):
        templates = self.load_templates()
        stable_frame = self.captureFrame()

        try:
            if stable_frame is not None:
                # Step 1: Detect and isolate the grid
                grid_image = self.detectGrid(stable_frame)

                # Step 2: Preprocess the isolated grid
                processed = self.preprocess_image(grid_image)
                
                # Step 3: Split the grid into cells
                cells = self.split_grid(processed)

                # Step 4: Identify grid contents
                self.grid_array = self.map_grid(cells, templates)

                # Step 5: Compare grids
                if self.previous_grid_array is None or self.grid_changed(self.previous_grid_array, self.grid_array):
                    print("Grid Updated:", self.grid_array)
                    self.previous_grid_array = self.grid_array
                else:
                    self.previous_grid_array = "Not Updated"
                    
        except ValueError as e:
            print(e)

        return self.previous_grid_array