'''
Lorissa Hughes

A springtime turtle graphics project showing a sunny camping scene in the
hills with grass, a river, flowers, clouds, a sun, and multiple tents.
The scene was first built as one larger drawing sequence, then refactored
into helper functions for the background, flowers, clouds, and tents so the
code would be easier to read, reuse, and modify. 

After refactoring, the scene was made more populated by increasing the number 
of clouds and tents, letting the flower colors be customized, and varying the tents in color,
size, and placement across the foreground. Specific improvements include grouping repeated 
drawing steps into reusable functions, spreading clouds more naturally across the sky, and 
keeping added tents below the top of the grass so the composition stays organized.


'''


# Import Turtle for drawing and math for tent height calculations.
import turtle
import math

def setup_turtle():
    """Initialize turtle with standard settings"""
    t = turtle.Turtle()
    t.speed(5)  # Fastest speed
    screen = turtle.Screen()
    screen.title("Turtle Graphics Assignment")
    return t, screen


def draw_rectangle(t, width, height, fill_color=None):
    """Draw a rectangle with optional fill"""
    if fill_color:
        t.fillcolor(fill_color)
        t.begin_fill()
    for _ in range(2):
        t.forward(width)
        t.right(90)
        t.forward(height)
        t.right(90)
    if fill_color:
        t.end_fill()

def draw_square(t, size, fill_color=None):
    """Draw a square with optional fill"""
    if fill_color:
        t.fillcolor(fill_color)
        t.begin_fill()
    for _ in range(4):
        t.forward(size)
        t.right(90)
    if fill_color:
        t.end_fill()


def draw_triangle(t, size, fill_color=None):
    """Draw an equilateral triangle with optional fill"""
    if fill_color:
        t.fillcolor(fill_color)
        t.begin_fill()
    for _ in range(3):
        t.forward(size)
        t.left(120)
    if fill_color:
        t.end_fill()


def draw_circle(t, radius, fill_color=None):
    """Draw a circle with optional fill"""
    if fill_color:
        t.fillcolor(fill_color)
        t.begin_fill()
    t.circle(radius)
    if fill_color:
        t.end_fill()


def draw_polygon(t, sides, size, fill_color=None):
    """Draw a regular polygon with given number of sides"""
    if fill_color:
        t.fillcolor(fill_color)
        t.begin_fill()
    angle = 360 / sides
    for _ in range(sides):
        t.forward(size)
        t.right(angle)
    if fill_color:
        t.end_fill()

def draw_curve(t, length, curve_factor, segments=10, fill_color=None):
    """
    Draw a curved line using small line segments
    
    Parameters:
    - t: turtle object
    - length: total length of the curve
    - curve_factor: positive for upward curve, negative for downward curve
    - segments: number of segments (higher = smoother curve)
    - fill_color: optional color to fill if creating a closed shape
    """
    if fill_color:
        t.fillcolor(fill_color)
        t.begin_fill()
        
    segment_length = length / segments
    # Save the original heading
    original_heading = t.heading()
    
    for i in range(segments):
        # Calculate the angle for this segment
        angle = curve_factor * math.sin(math.pi * i / segments)
        t.right(angle)
        t.forward(segment_length)
        t.left(angle)  # Reset the angle for the next segment
    
    # Reset to original heading
    t.setheading(original_heading)
    
    if fill_color:
        t.end_fill()
        
def jump_to(t, x, y):
    """Move turtle without drawing"""
    t.penup()
    t.goto(x, y)
    t.pendown()


def draw_background():
    """Draw the fixed background layers behind the main objects."""
    t = turtle.getturtle()
    screen = t.getscreen()
    screen.bgcolor("skyblue")

    # Place two filled circles low on the screen to act as rolling hills.
    jump_to(t, 170, -200)
    draw_circle(t, 180, fill_color="green")
    jump_to(t, -170, -100)
    draw_circle(t, 100, fill_color="green")
    jump_to(t, -400, 0)

    # Add a wide rectangle in front so later objects sit on the grass.
    draw_rectangle(t, 800, 400, fill_color="green")


def flowers(color1="pink", color2="purple", color3="cyan"):
    """Draw three rows of flowers and allow the row colors to be changed."""
    t = turtle.getturtle()

    # Alternate heights so the flowers feel more scattered across the field.
    for i in range(7):
        jump_to(t, (-300 + i * 100), (-100 + (-1)**i * 80))
        draw_polygon(t, 7, 7, fill_color=color1)

    for i in range(5):
        jump_to(t, (-200 + i * 120), (-50 + (-1)**i * 100))
        draw_polygon(t, 7, 4, fill_color=color2)

    for i in range(5):
        jump_to(t, (-250 + i * 120), (-150 + (-1)**i * 80))
        draw_polygon(t, 7, 4, fill_color=color3)


def clouds(number_of_clouds):
    """Draw the requested number of clouds across the upper sky."""
    t = turtle.getturtle()

    for i in range(number_of_clouds):
        # Spread clouds horizontally and stagger their heights slightly.
        base_x = -250 + i * 180
        base_y = 200 + (-1)**i * 20

        jump_to(t, base_x, base_y)
        draw_circle(t, 20, fill_color="white")
        jump_to(t, (t.xcor() + 30), (t.ycor() + 10))
        draw_circle(t, 20, fill_color="white")
        jump_to(t, (t.xcor() - 14), (t.ycor() - 20))
        draw_circle(t, 20, fill_color="white")
        jump_to(t, (t.xcor() + 30), (t.ycor() + 10))
        draw_circle(t, 20, fill_color="white")
        jump_to(t, (t.xcor() + 180), (t.ycor() + 20))


def tent(number_of_tents=1):
    """Draw one or more tents with varied layouts and cycling colors."""
    t = turtle.getturtle()
    tent_colors = ["brown", "red", "orange", "olivedrab"]
    tent_layouts = [
        (-230, -120, 150),
        (-30, -150, 120),
        (145, -185, 95),
        (-360, -170, 110),
        (270, -160, 105),
    ]

    for i in range(number_of_tents):
        x, y, size = tent_layouts[i % len(tent_layouts)]
        # Keep each tent low enough that its peak stays within the foreground.
        peak_height = size * math.sqrt(3) / 2
        y = min(y, -peak_height)

        jump_to(t, x, y)
        draw_triangle(t, size, fill_color=tent_colors[i % len(tent_colors)])


# Build the full picture by combining the helper functions with the remaining
# single-use objects, keeping all drawing logic inside functions.
def draw_scene(t):
    """Draw a colorful scene with various shapes"""
    draw_background()

    # Draw the river after the grass so it appears in the foreground.
    jump_to(t, -75, 0)
    draw_curve(t, 600, curve_factor=40, segments=20, fill_color="blue")
    
    # Place the sun high in the sky above the hills.
    jump_to(t, 200, 250)
    draw_circle(t, 50, fill_color="yellow")

    # Add repeated scene details after refactoring.
    flowers("LightGoldenRod1", "RosyBrown1", "plum2")
    clouds(4)
    tent(4)


# Set up the turtle window and start drawing the full scene.
def main():
    t, screen = setup_turtle()
    draw_scene(t)
    screen.mainloop()

# Run the program only when this file is executed directly.
if __name__ == "__main__":
    main()
