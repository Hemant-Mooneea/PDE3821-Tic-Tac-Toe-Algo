import cv2
import numpy as np

# isolates the grid from the input image
def detectGrid(image):
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
        ordered_pts = order_points(pts)

        # transform the grid to a fixed size one, so it's easier to split into smaller cells
        grid_size = 360
        dst = np.array([[0, 0], [grid_size - 1, 0], [grid_size - 1, grid_size - 1], [0, grid_size - 1]], dtype="float32")

        # Perspective transform
        matrix = cv2.getPerspectiveTransform(ordered_pts, dst)
        grid = cv2.warpPerspective(image, matrix, (grid_size, grid_size))
        return grid

    else:
        raise ValueError("Grid not detected. Ensure the grid is clearly visible.")


# Organizes the 4 corners of the detected grid so they can be used for perspective transformation
def order_points(pts):
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
def preprocess_image(image):
    # turn image into black and white
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

    # make grid lines black and cell content black and everything else white
    _, thresh = cv2.threshold(grayImage, 160, 255, cv2.THRESH_BINARY_INV)  
    return thresh


# Function to divide the grid into 3x3 cells
def split_grid(image):
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

            # # Display each cell
            # cv2.imshow(f"Cell ({i}, {j})", cell)
            # cv2.waitKey(0)  # Wait for a key press before moving to the next cell
            # cv2.destroyWindow(f"Cell ({i}, {j})")  # Close the window after viewing

            #add cell to the current row
            row.append(cell)
        #add the completed row to the list of cells
        cells.append(row)
    print("cell height: " , cell_height , " cell width: " , cell_width)
    return cells


# identify the contents of a cell
def identify_cell_content(cell, templates):
    contours, _ = cv2.findContours(cell, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # if no contours detected, cell is empty
    if len(contours) == 0:
        return "Empty" 
    
    #find the largest contour
    max_contour = max(contours, key=cv2.contourArea)
    #if the largest shape is too small, consider it empty
    if cv2.contourArea(max_contour) < 100:
        return "Empty"
    
    #compare the cell to each template 
    for label, template in templates.items():
        #check how well the template matches
        res = cv2.matchTemplate(cell, template, cv2.TM_CCOEFF_NORMED)
        # if similarity is above 0.5, assume it's a match
        if np.max(res) > 0.35: 
            # return the label, X or O
            return label
    # if no template matches, return "Unknown"
    return "Unknown"


# maps grid contents to dictionary and array
def map_grid(cells, templates):
    # stores content of each cell as {(row, col): "content"}
    grid_dict = {}
    # stores content in a 2D array
    grid_array = []
    
    #loop through each row of cells
    for i, row in enumerate(cells):
        # temporary array for this row in the array
        array_row = []
        #loop through each cell in the row
        for j, cell in enumerate(row):
            #identify what's inside the cell
            content = identify_cell_content(cell, templates)
            #add it to the dictionary with (row, col) as key
            grid_dict[(i, j)] = content
            # add it to array row
            array_row.append(content)
        #add the completed row to the 2D array
        grid_array.append(array_row)
    
    return grid_dict, grid_array

# Initialize templates for X and O
def load_templates():
    template_X = cv2.imread('templates/X.jpg', cv2.IMREAD_GRAYSCALE)
    template_O = cv2.imread('templates/O.jpg', cv2.IMREAD_GRAYSCALE)

     # Resize templates to match cell size
    template_X = cv2.resize(template_X, (120, 120))
    template_O = cv2.resize(template_O, (120, 120))

    

    # Apply thresholding
    _, template_X = cv2.threshold(template_X, 170, 255, cv2.THRESH_BINARY_INV)
    _, template_O = cv2.threshold(template_O, 170, 255, cv2.THRESH_BINARY_INV)

    cv2.imshow("Template1", template_O)
    cv2.imshow("Template2", template_X)
    cv2.waitKey(0)  # Wait for a key press before moving to the next cell
    cv2.destroyAllWindows()  # Close the window after viewing

    return {"X": template_X, "O": template_O}

# Compare grids to detect changes
def grid_changed(previous, current):
    return previous != current


# read image used
img = cv2.imread("test_images/test1.jpg") 
templates = load_templates()
previous_grid_array = None

grid_image = detectGrid(img)

processed = preprocess_image(grid_image)

 # Step 3: Split the grid into cells
cells = split_grid(processed)

# Step 4: Identify grid contents
grid_dict, grid_array = map_grid(cells, templates)

# Step 5: Compare grids
if previous_grid_array is None or grid_changed(previous_grid_array, grid_array):
    print("Grid Updated:")
    print(grid_array)
    previous_grid_array = grid_array

# Display the isolated grid for debugging
cv2.imshow("Grid", grid_image)
cv2.imshow("Processed", processed)


cv2.waitKey(0)

cv2.destroyAllWindows()


# Main Program
# def main():
#     # Load the camera feed or an image
#     cap = cv2.VideoCapture(0)
#     templates = load_templates()
#     previous_grid_array = None

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("Failed to capture frame")
#             break

#         try:
#             # Step 1: Detect and isolate the grid
#             grid_image = detect_grid(frame)

#             # Step 2: Preprocess the isolated grid
#             processed = preprocess_image(grid_image)
            
#             # Step 3: Split the grid into cells
#             cells = split_grid(processed)

#             # Step 4: Identify grid contents
#             grid_dict, grid_array = map_grid(cells, templates)

#             # Step 5: Compare grids
#             if previous_grid_array is None or grid_changed(previous_grid_array, grid_array):
#                 print("Grid Updated:")
#                 print(grid_dict)
#                 previous_grid_array = grid_array

#             # Display the isolated grid for debugging
#             cv2.imshow("Grid", grid_image)
#             cv2.imshow("Processed", processed)

#         except ValueError as e:
#             print(e)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()