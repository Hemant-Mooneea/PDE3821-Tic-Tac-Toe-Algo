import cv2
import numpy as np

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
        #compare the cell to each template 
        for label, template in templates.items():
            #check how well the template matches
            res = cv2.matchTemplate(cell, template, cv2.TM_CCOEFF_NORMED)
            # if similarity is above 0.5, assume it's a match
            if np.max(res) > 0.5: 
                # return the label, X or O
                return label
        # if no template matches, return "Empty"
        return "Empty"


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
                # add it to array row
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
    def grid_changed(previous, current):
        return previous != current


    # capture frame from camera module and feed it to the different functions to extract grid data
    def main(self):
        # Load the camera feed or an image
        cap = cv2.VideoCapture(0)
        templates = self.load_templates()

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame")
                break

            try:
                #! just using an image as example since i can't use frame at the moment
                img = cv2.imread("test_images/test1.jpg") 
                # Step 1: Detect and isolate the grid
                grid_image = self.detectGrid(img) #? will replace img with frame later

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
                    return self.previous_grid_array
                else:
                    return self.previous_grid_array

            except ValueError as e:
                print(e)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        return self.previous_grid_array


#? testing
# camera = Camera()

# grid = camera.main()




















# # read image used
# img = cv2.imread("test_images/test1.jpg") 
# templates = load_templates()
# previous_grid_array = None

# grid_image = detectGrid(img)

# processed = preprocess_image(grid_image)

# cells = split_grid(processed)

# grid_dict, grid_array = map_grid(cells, templates)

# if previous_grid_array is None or grid_changed(previous_grid_array, grid_array):
#     print("Grid Updated:")
#     print(grid_array)
#     previous_grid_array = grid_array

# cv2.imshow("Grid", grid_image)
# cv2.imshow("Processed", processed)


# cv2.waitKey(0)

# cv2.destroyAllWindows()