from graphix import Window, Point, Rectangle, Circle, Polygon

# Constants for screen and tile sizes
SCREEN = 100  # Size of the grid cell in pixels
TILE = 100  # Size of each patch in pixels
SMALL_TILE = 10  # Size of sub-elements in patches
SMALL_RADIUS = 5  # Radius for small circles

# Valid user inputs for patchwork size and colors
VALID_SIZES = [5, 7, 9]  # Allowed patch sizes
VALID_COLOURS = ["red", "green", "blue", "magenta", "orange", "purple"]  # Allowed colors


# Draws a rectangle on the window
def draw_rectangle(win, top_left, bottom_right, colour):
    rec = Rectangle(top_left, bottom_right)
    rec.fill_colour = colour
    rec.outline_colour = colour
    rec.draw(win)


# Draws a circle on the window
def draw_circle(win, center, radius, colour, outline):
    circle = Circle(center, radius)
    circle.fill_colour = colour
    circle.outline_colour = outline
    circle.draw(win)


# Draws a polygon (diamond) on the window
def draw_polygon(win, left, right, top, below, colour):
    pol_points = [left, right, top, below]
    pol = Polygon(pol_points)
    pol.fill_colour = colour
    pol.outline_colour = colour
    pol.draw(win)


# Draws the first patch design
def draw_patch_1(win, tl, colour):
    X = tl.x
    Y = tl.y
    for y in range(Y, TILE + Y, SMALL_TILE):
        for x in range(X, TILE + X, SMALL_TILE):
            tl = Point(x, y)
            br = Point(x + SMALL_TILE, y + SMALL_TILE)
            # Draw rectangles diagonally for the design
            if x + y == TILE + Y + X - SMALL_TILE:
                draw_rectangle(win, tl, br, colour)


# Draws the second patch design
def draw_patch_2(win, tl, colour):
    SMALL_TILE = 20  # Larger sub-tile size for this design
    X = tl.x
    Y = tl.y
    for y in range(Y, TILE + Y, SMALL_TILE):
        for x in range(X, TILE + X, SMALL_TILE):
            tl = Point(x, y)
            br = Point(x + SMALL_TILE, y + SMALL_TILE)
            centre = Point(SMALL_TILE // 2 + x, SMALL_TILE // 2 + y)

            # Draw alternate rectangles and circles for the design
            if y == Y or y == SMALL_TILE * 2 + Y or y == SMALL_TILE * 4 + Y:
                draw_rectangle(win, tl, br, colour)  # Colored rectangles
                draw_circle(win, centre, SMALL_RADIUS, "white", colour)  # White circles
            else:
                draw_rectangle(win, tl, br, "white")  # White rectangles
                draw_circle(win, centre, SMALL_RADIUS, colour, colour)  # Colored circles

            # Add the polygon (diamond) at specific grid positions
            if y == SMALL_TILE + Y or y == SMALL_TILE * 3 + Y:
                if x == X or x == SMALL_TILE * 2 + X or x == SMALL_TILE * 4 + X:
                    draw_polygon(
                        win,
                        Point(x + SMALL_TILE // 2, y),  # Top point of the diamond
                        Point(x + SMALL_TILE, y + SMALL_TILE // 2),  # Right point
                        Point(x + SMALL_TILE // 2, y + SMALL_TILE),  # Bottom point
                        Point(x, y + SMALL_TILE // 2),  # Left point
                        colour  # Polygon fill color
                    )
                    draw_circle(win, centre, SMALL_RADIUS, "white", colour) # Add white circles inside the polygons


# Draws a plain patch (blank square)
def draw_patch_blank(win, tl, colour):
    square = Rectangle(tl, Point(tl.x + 100, tl.y + 100))
    square.fill_colour = colour
    square.draw(win)


# Draws the entire patchwork based on user inputs
def draw_patchwork(win, size, colours):
    for y in range(0, size * TILE, 100):
        for x in range(0, size * TILE, 100):
            top_left = Point(x, y)
            bottom_right = Point(x + TILE, y + TILE)
            # Determine patch color based on position
            if x == y or x + y == SCREEN * size - TILE:
                colour = colours[0]  # First color for diagonals
            elif x < y and x + y < SCREEN * size - TILE or x > y and x + y > SCREEN * size - TILE:
                colour = colours[2]  # Third color for certain quadrants
            else:
                colour = colours[1]  # Second color for other quadrants

            # Use the patch designs for inner grid areas
            if TILE <= x < SCREEN * size - TILE and TILE <= y < SCREEN * size - TILE:
                if x == y or x + y == SCREEN * size - TILE:
                    draw_patch_1(win, top_left, colour)
                else:
                    draw_patch_2(win, top_left, colour)
            else:
                # Plain patch for borders
                draw_rectangle(win, top_left, bottom_right, colour)


# Prompts the user for patch size and validates the input
def get_patch_size():
    while True:
        size = int(input("Enter patch size (5, 7, or 9): "))
        if size in VALID_SIZES:
            print("Size is:", size)
            return size
        else:
            print("Invalid size. Please choose 5, 7, or 9.")


# Prompts the user for three unique colors and validates the input
def get_patch_colors():
    user_colours = []
    for i in range(3):
        while True:
            colour = input(f"Enter colour {i+1} (red, green, blue, magenta, orange, purple): ").lower()
            if colour in VALID_COLOURS and colour not in user_colours:
                user_colours.append(colour)
                print("Colour is:", colour)
                break
            elif colour in user_colours:
                print("Duplicate colour. Please enter another one.")
            else:
                print("Invalid colour. Please choose a valid colour.")
    return user_colours


# Main function to run the program
def program():
    size = get_patch_size()  # Get patchwork size from user
    user_colours = get_patch_colors()  # Get patchwork colors from user
    win = Window("Grid Patterns", SCREEN * size, SCREEN * size)  # Create a drawing window
    draw_patchwork(win, size, user_colours)  # Draw the patchwork
    win.get_mouse()  # Wait for user to click before closing
    win.close()  # Close the window


program()  # Execute the program
