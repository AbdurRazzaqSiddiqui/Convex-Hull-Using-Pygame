import pygame
import sys
from pygame.locals import *
from convex_brute_force_func import convex_hull_bruteforce
from convex_graham_scan_func import convex_hull_grahamscan
from convex_jarvis_march_func import convex_hull_jarvismarch
from convex_quick_elimination_func import convex_hull_quickelimination     
from convex_research_func import convex_hull_research
from line_intersect_func import line_intersection_checker_algebra
from line_intersect_func import line_intersection_checker_CCW
# from pyvidplayer import Video
# vid = Video("hello.mp4")
# vid.draw(menu_screen,(0,0))
# while True:
#     vid.draw(menu_screen,(0,0))
#     pygame.display.update()
# Initialize Pygame

pygame.init()

# Constants
width, height = 960, 720
bg_img = pygame.image.load('image.jpg')
bg_img = pygame.transform.scale(bg_img,(width,height))
button_color = (0, 71, 189)
text_color = (255,255,255)
heading_color = (56, 0, 153)
button_border_color = heading_color
button_width = 160
button_height = 30
button_margin = 15
point_color = (30, 0, 255)
point_bg_color = (255,255,255)
coord_color = (56, 0, 153)
line_color = (0,30,255)
line_width = 1
point_radius = 8
font_size = 24
# Create a menu window
menu_screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Convex Hull Visualization - Menu")

# Font setup
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 20)

# Initialize the screen as None
screen = None

# Function to create a button
def draw_button(rect, text, callback):
    pygame.draw.rect(menu_screen, button_color, rect)
    pygame.draw.rect(menu_screen, button_border_color, rect, 5)  # Draw the border
    text_surface = small_font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    menu_screen.blit(text_surface, text_rect)
    if rect.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0]:
            callback()

# Function to open the main application window
def open_main_window(algorithm_no):
    global screen,algo_title  # Declare screen and algo title as a global variable
    if screen is not None:
        screen.blit(bg_img,(0,0))  # Clear the screen
        pygame.display.flip()  # Update the display

    screen = pygame.display.set_mode((width, height))
    if algorithm_no==1:
        # Create the main application window for Brute Force
        algo_title = "Brute Force"
    elif algorithm_no == 2:
        # Create the main application window for Graham Scan
        algo_title = "Graham Scan"
    elif algorithm_no == 3:
        # Create the main application window for Jarvis March
        algo_title = "Jarvis March"
    elif algorithm_no == 4:
        # Create the main application window for Quick Elimination
        algo_title = "Quick Elimination"
    elif algorithm_no == 5:
        algo_title = "Chan Algorithm"    

    # List to store user-selected points
    points = []

    # Variable to store the Convex Hull
    convex_hull = []

    # Flag to indicate whether the "Find Complexity" button was clicked
    complexity_button_clicked = False

    # Rectangles to define the button areas
    reset_button_rect = pygame.Rect(width - button_width - button_margin, button_margin, button_width, button_height)
    convex_hull_button_rect = pygame.Rect(width - button_width - button_margin, button_margin * 2 + button_height, button_width, button_height)
    back_button_rect = pygame.Rect(width - button_width - button_margin, height - button_height - button_margin, button_width, button_height)
    complexity_button_rect = pygame.Rect(width - button_width - button_margin, height - button_height - button_margin * 2 - button_height, button_width, button_height)

    # Function to draw a point
    def draw_point(x, y, color=point_color):
        pygame.draw.circle(screen, color, (x, y), point_radius)
        pygame.draw.circle(screen, point_bg_color, (x, y), point_radius-3)
        coords_text = small_font.render(f'({x},{y})', True, coord_color)
        screen.blit(coords_text, (x + 10, y - 20))

    # Function to find the convex hull
    def find_convex_hull():
        nonlocal convex_hull
        if algorithm_no == 1:
            convex_hull = convex_hull_bruteforce([point for point in points if not is_point_in_button(point)])
        elif algorithm_no == 2:
            convex_hull = convex_hull_grahamscan([point for point in points if not is_point_in_button(point)])
        elif algorithm_no == 3: 
            convex_hull = convex_hull_jarvismarch([point for point in points if not is_point_in_button(point)])   
        elif algorithm_no == 4:
            convex_hull = convex_hull_quickelimination([point for point in points if not is_point_in_button(point)])  
        elif algorithm_no == 5:
            convex_hull = convex_hull_research([point for point in points if not is_point_in_button(point)])     

    # Function to reset points and clear the convex hull
    def reset_points():
        nonlocal convex_hull, complexity_button_clicked
        points.clear()
        convex_hull.clear()
        screen.blit(bg_img,(0,0))
        complexity_button_clicked = False  # Reset the button click flag

    # Function to find the time and space complexity
    def find_complexity():
        nonlocal complexity_button_clicked
        complexity_button_clicked = True
        global time_complexity, space_complexity
        if algorithm_no == 1:
            time_complexity = "O(n^3)"  # Calculate or update the time complexity for Brute Force here
        elif algorithm_no == 2:
            time_complexity = "O(nlogn)"  # Calculate or update the time complexity for Graham Scan here
        elif algorithm_no == 3:
            time_complexity = "O(nh)"    
        elif algorithm_no == 4: 
            time_complexity = "O(nlogn)"
        space_complexity = "O(n)"  # Calculate or update the space complexity here

    # Function to check if a point is inside a button, excluding the "Find Complexity" button
    def is_point_in_button(point):
        return reset_button_rect.collidepoint(point) or convex_hull_button_rect.collidepoint(point) or back_button_rect.collidepoint(point)

    # Main loop for the main application window
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                back_to_menu()  # Go back to the main menu
            if event.type == MOUSEBUTTONDOWN:
                if len(points) < 20:
                    if not complexity_button_clicked:
                        point = event.pos
                        if not (complexity_button_rect.collidepoint(point) or is_point_in_button(point)):
                            points.append(point)
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    reset_points()

        # Set the background color
        screen.blit(bg_img,(0,0))

        # Draw title
        title_text = font.render("Convex Hull Application - " + algo_title, True, heading_color)
        title_rect = title_text.get_rect(center=(width // 3, 15 + title_text.get_height() // 2))
        screen.blit(title_text, title_rect)

        # Draw buttons
        draw_button(reset_button_rect, "Reset", reset_points)
        draw_button(convex_hull_button_rect, "Find Convex Hull", find_convex_hull)
        draw_button(complexity_button_rect, "Find Complexity", find_complexity)

        # Draw the "Back" button
        draw_button(back_button_rect, "Back", sub_menu1)

        # Draw time and space complexity above the button if the button was clicked
        if complexity_button_clicked:
            complexity_text = small_font.render(f"Time Complexity: {time_complexity} | Space Complexity: {space_complexity}", True, heading_color)
            screen.blit(complexity_text, (complexity_button_rect.centerx - complexity_text.get_width() / 2 - 80, complexity_button_rect.y - complexity_text.get_height()-10))

        # Draw convex hull
        if convex_hull:
            pygame.draw.lines(screen, line_color, True, convex_hull, 2)

        # Draw points and coordinates
        for point in points:
            draw_point(point[0], point[1])

        # Update the display
        pygame.display.flip()

def line_intersect(intersect_no):
    # Initialize Pygame
    pygame.init()

    # Constants

    # Create a screen
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Line Intersection Checker")

    # Store the points for the two lines
    line1 = []  # Store coordinates of line 1
    line2 = []  # Store coordinates of line 2
    line1_ready = False  # Track if line 1 is ready for intersection check
    line2_ready = False  # Track if line 2 is ready for intersection check

    # Flags for showing intersection status
    show_intersection_status = False
    intersection_status_displayed = False  # New flag to track if the intersection status is displayed

    # Function to draw a point on the screen
    def draw_point(x, y, color=point_color,label=None):
        pygame.draw.circle(screen, color, (x, y), point_radius)
        pygame.draw.circle(screen, point_bg_color, (x, y), point_radius-3)
        if label:
            font = pygame.font.Font(None, font_size)
            text = font.render(label, True, color)
            text_rect = text.get_rect(center=(x, y - 2 * point_radius))
            screen.blit(text, text_rect)

    # Function to draw a line on the screen
    def draw_line(start, end):
        pygame.draw.line(screen, line_color, start, end, line_width)    

    # Function to display the intersection status
    def display_intersection_status():
        nonlocal intersection_status_displayed
        if line1_ready and line2_ready and show_intersection_status:
            if intersect_no == 1:
                intersection = line_intersection_checker_algebra(line1, line2)
            elif intersect_no == 2:
                intersection = line_intersection_checker_CCW(line1, line2)   
#            elif intersect_no == 3:
#                intersection = line_intersection_checker_CCW(line1, line2)

            intersection_status = "Lines Intersect" if intersection else "Lines Do Not Intersect"
            font = pygame.font.Font(None, font_size)
            text = font.render(intersection_status, True, line_color)
            text_rect = text.get_rect(center=((width // 2) - 160, height // 10 + 20))
            screen.blit(text, text_rect)
            intersection_status_displayed = True

    def reset_line_points():
        screen.blit(bg_img,(0,0))
        line1.clear()
        line2.clear()
        line1_ready = False
        line2_ready = False
        drawing_line1 = True
        show_intersection_status = False
        intersection_status_displayed = False

    # Main loop
    drawing_line1 = True
    reset_button_rect = pygame.Rect(width - 180, height - 100, 160, 40)  # Create the reset button rect
    back_button_rect = pygame.Rect(width - 180, height - 50, 160, 40)  # Create the back button rect
    find_intersection_button_rect = pygame.Rect(width - 180, 10, 160, 40)  # Create the "Find Intersection" button rect

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if reset_button_rect.collidepoint(x, y):
                    # Handle the "Reset" button by clearing both lines and resetting flags
                    line1.clear()
                    line2.clear()
                    drawing_line1 = True
                    line1_ready = False
                    line2_ready = False
                    show_intersection_status = False
                    intersection_status_displayed = True  # Clear intersection status when resetting
                elif back_button_rect.collidepoint(x, y):
                    # Handle the "Back to Menu" button
                    # You can add code here to go back to the menu screen
                    pass
                elif find_intersection_button_rect.collidepoint(x, y):
                    # Handle the "Find Intersection" button
                    show_intersection_status = True
                    intersection_status_displayed = False  # Reset intersection status display flag
                elif drawing_line1:
                    line1.append((x, y))
                    if len(line1) == 2:
                        line1_ready = True
                else:
                    line2.append((x, y))
                    if len(line2) == 2:
                        line2_ready = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                show_intersection_status = True  # Show intersection status

        # Draw everything on the screen
        screen.blit(bg_img,(0,0))

        # Draw title
        font = pygame.font.Font(None, 36)
        title_text = font.render("Line Intersection Checker", True, heading_color)
        title_rect = title_text.get_rect(center=(width // 3, 15 + title_text.get_height() // 2))
        screen.blit(title_text, title_rect)

        # Always show the "Reset" button
        draw_button(reset_button_rect, "Reset", reset_line_points)

        # Draw the "Back" button
        draw_button(back_button_rect, "Back", sub_menu2)

        draw_button(find_intersection_button_rect, "Find Intersection", display_intersection_status)

        # Draw the points
        for point in line1:
            draw_point(point[0], point[1], label=f"({point[0]}, {point[1]})")
        for point in line2:
            draw_point(point[0], point[1], label=f"({point[0]}, {point[1]})")

        # Draw the lines if they are ready
        if line1_ready:
            draw_line(line1[0], line1[1])
        if line2_ready:
            draw_line(line2[0], line2[1])

        # Display the intersection status when requested
        if show_intersection_status:
            display_intersection_status()

        pygame.display.update()

        # Switch to drawing the second line if the first line is ready
        if line1_ready and not line2_ready:
            drawing_line1 = False

# Function to open the line intersection window
def open_line_intersection_window(intersect_no):
    global screen  # Declare screen as a global variable
    screen = None  # Set the screen to None

    # Clear the main application screen
    menu_screen.blit(bg_img,(0,0))
    pygame.display.flip()  # Update the display

    # Call the line intersection function
    if intersect_no == 1:
        line_intersect(intersect_no=1)
    elif intersect_no == 2:
        line_intersect(intersect_no=2)    
    elif intersect_no == 3:
        line_intersect(intersect_no=3)

# Sub menu function for Convex Hulls
def sub_menu1():
    global screen  # Declare screen as a global variable
    screen = None  # Set the screen to None

    # Clear the main application screen
    menu_screen.blit(bg_img,(0,0))
    pygame.display.flip()  # Update the display

    # Main menu loop
    menu_running = True
    while menu_running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()  # Quit the program
                sys.exit()  # Exit the program

        # Set the background color
        menu_screen.blit(bg_img,(0,0))

        # Draw "Brute Force" button
        brute_force_button_rect = pygame.Rect(width // 2 - button_width // 2, height // 2 - button_height // 2, button_width, button_height)
        graham_scan_button_rect = pygame.Rect(width // 2 - button_width // 2, height // 2 - button_height // 2 + 40, button_width, button_height)
        jarvis_march_button_rect = pygame.Rect(width // 2 - button_width // 2, height // 2 - button_height // 2 + 80, button_width, button_height)
        quick_elimination_button_rect = pygame.Rect(width // 2 - button_width // 2, height // 2 - button_height // 2 + 120, button_width, button_height)
        research_button_rect = pygame.Rect(width // 2 - button_width // 2, height // 2 - button_height // 2 + 160, button_width, button_height)
        back_button_rect = pygame.Rect(width // 2 - button_width // 2, height // 2 - button_height // 2 + 200, button_width, button_height)

        draw_button(brute_force_button_rect, "Brute Force", lambda: open_main_window(algorithm_no=1))
        draw_button(graham_scan_button_rect, "Graham Scan", lambda: open_main_window(algorithm_no=2))
        draw_button(jarvis_march_button_rect, "Jarvis March", lambda: open_main_window(algorithm_no=3))
        draw_button(quick_elimination_button_rect, "Quick Elimination", lambda: open_main_window(algorithm_no=4))
        draw_button(research_button_rect, "Research Algorithm", lambda: open_main_window(algorithm_no=5))         
        draw_button(back_button_rect, "Return to Main Menu", main_menu)      

        # Update the display
        pygame.display.flip()

# Sub menu for Line intersection
def sub_menu2():
    global screen  # Declare screen as a global variable
    screen = None  # Set the screen to None

    # Clear the main application screen
    menu_screen.blit(bg_img,(0,0))
    pygame.display.flip()  # Update the display

    # Main menu loop
    menu_running = True
    while menu_running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()  # Quit the program
                sys.exit()  # Exit the program

        # Set the background color
        menu_screen.blit(bg_img,(0,0))

        # Draw "Brute Force" button
        line1_button_rect = pygame.Rect(width // 2 - button_width // 2, height // 2 - button_height // 2, button_width, button_height)
        line2_button_rect = pygame.Rect(width // 2 - button_width // 2, height // 2 - button_height // 2 + 40, button_width, button_height)
        line3_button_rect = pygame.Rect(width // 2 - button_width // 2, height // 2 - button_height // 2 + 80, button_width, button_height)
        back_button_rect = pygame.Rect(width // 2 - button_width // 2, height // 2 - button_height // 2 + 120, button_width, button_height)

        draw_button(line1_button_rect, "Line Intersection 1", lambda: line_intersect(intersect_no=1))
        draw_button(line2_button_rect, "Line Intersection 2", lambda: line_intersect(intersect_no=2))
        draw_button(line3_button_rect, "Line Intersection 3", lambda: line_intersect(intersect_no=3))
        draw_button(back_button_rect, "Return to Main Menu", main_menu)

        # Handle button clicks
        if line1_button_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                open_line_intersection_window(intersect_no=1)  # Open the line intersection window

        # Handle button clicks
        if line2_button_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                open_line_intersection_window(intersect_no=2)  # Open the line intersection window    

        # Handle button clicks
        if line3_button_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                open_line_intersection_window(intersect_no=3)  # Open the line intersection window                

        # Update the display
        pygame.display.flip()

# About Function
def about():
    global screen  # Declare screen as a global variable
    screen = None  # Set the screen to None

    # Clear the main application screen
    menu_screen.blit(bg_img,(0,0))
    pygame.display.flip()  # Update the display

    # Main menu loop
    menu_running = True
    while menu_running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()  # Quit the program
                sys.exit()  # Exit the program

        # Set the background color
        menu_screen.blit(bg_img,(0,0))

        back_button_rect = pygame.Rect(width - button_width - button_margin, height - button_height - 15, button_width, button_height)
        draw_button(back_button_rect, "Return to Main Menu", main_menu) 

        # Load images
        image1 = pygame.image.load("image.jpg")  
        image2 = pygame.image.load("image.jpg")  
        image3 = pygame.image.load("image.jpg")  

        # Scale the images to fit on the screen
        image1 = pygame.transform.scale(image1, (200, 200))
        image2 = pygame.transform.scale(image2, (200, 200))
        image3 = pygame.transform.scale(image3, (200, 200))

        # Fonts
        font = pygame.font.Font(None, 36)

        # Create text captions
        caption1 = font.render("Picture 1", True, heading_color)
        caption2 = font.render("Picture 2", True, heading_color)
        caption3 = font.render("Picture 3", True, heading_color)

        # Display images
        menu_screen.blit(image1, (width // 4 - 100, height // 2 - 100))
        menu_screen.blit(image2, (width // 2 - 100, height // 2 - 100))
        menu_screen.blit(image3, (3 * width // 4 - 100, height // 2 - 100))

        # Display captions
        menu_screen.blit(caption1, (width // 4 - 40, height // 2 + 110))
        menu_screen.blit(caption2, (width // 2 - 40, height // 2 + 110))
        menu_screen.blit(caption3, (3 * width // 4 - 40, height // 2 + 110))

        pygame.display.flip()

# Main menu function
def main_menu():
    global screen  # Declare screen as a global variable
    screen = None  # Set the screen to None

    # Clear the main application screen
    menu_screen.blit(bg_img,(0,0))
    pygame.display.flip()  # Update the display

    # Main menu loop
    menu_running = True
    while menu_running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()  # Quit the program
                sys.exit()  # Exit the program

        # Set the background color
        menu_screen.blit(bg_img,(0,0))

        # Draw Title
        title_text = font.render("Algorithm Project", True, heading_color)
        title_rect = title_text.get_rect(center=(width // 2, 15 + title_text.get_height() // 2))
        menu_screen.blit(title_text, title_rect)

        convex_hull_button_rect = pygame.Rect(width//2 - 80, height//2 - 100, 160, 40)  # Create the convex button rect
        draw_button(convex_hull_button_rect, "Convex Hull Generator", sub_menu1)

        line_int_button_rect = pygame.Rect(width//2 - 80, height//2 - 50, 160, 40)  # Create the convex button rect
        draw_button(line_int_button_rect, "Line Intersect Checker", sub_menu2)

        about_button_rect = pygame.Rect(width - button_width - button_margin, button_margin * 2 - 15, button_width, button_height)
        draw_button(about_button_rect, "About Us", about)
        pygame.display.flip()

# Call the function to display the main menu initially
main_menu()
sys.exit()
