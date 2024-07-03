import turtle
import random
import time
from functools import partial

direction_map = {"Right": {"index": 0, "move": (20, 0)},
                 "Up": {"index": 1, "move": (0, 20)},
                 "Left": {"index": 2, "move": (-20, 0)},
                 "Down": {"index": 3, "move": (0, -20)},
                 "Pause": {"index": 4, "move": (0, 0)}
}
last_direction, screen, snake, monster, intro_1, intro_2, status, key_pressed = None, None, None, None, None, None, None, None
num_of_contact, count_winner, length, elapsed_time, state_contact, speed = 0, 0, 1, 0, False, 0
list_food_item, list_key, head_list, list_non_repeat, food_conceal_state, eat = [], [0.5, 0.5], [], [0.5, 0.5], [False] * 5, [False] * 5
state, switch_move, state_strike, dir_change, motion, game_over_shown, snake_size, all_food_eaten= None, True, False, True, None, False,5, False
tendency = [0, 0]
color_body, color_head, color_monster = ("blue", "black"), "red", "purple"
font = ("Arial", 16, "normal")
key_up, key_down, key_left, key_right, key_space = "Up", "Down", "Left", "Right", "space"
monsters = []
heading_by_key = {key_up: 90, key_down: 270, key_left: 180, key_right: 0}

def rewrite(index):

    """
        :param index: We need to flash the food into a new place nearby,so I use this to do it
        :return: a new food cordinate that realize the flash the carvas
        """

    global turtle_list, food_list, food_conceal_state
    movements = [(0, 40), (0, -40), (40, 0), (-40, 0)]
    food_turtle = turtle_list[index]
    if not eat[index]:
        if food_conceal_state[index]:
            food_turtle.clear()
        else:
            move = random.choice(movements)
            new_x = food_turtle.xcor() + move[0]
            new_y = food_turtle.ycor() + move[1]
            if -240 <= new_x <= 240 and -280 <= new_y <= 200:
                food_turtle.goto(new_x, new_y)
                food_list[index] = (round(new_x / 20), round((new_y + 40) / 20))
            food_turtle.clear()
            food_turtle.write(index + 1, font=font)

def configure_play_area():

    """
       I use the function to create a canvas that our game is dependent on it

       :return: we create a new area that can help bound the area that the snack is moving on
       """

    m = create_turtle(0, 0, "", "black")
    m.shapesize(25, 25, 5)
    m.goto(0, -40)
    s = create_turtle(0, 0, "", "black")
    s.shapesize(4, 25, 5)
    s.goto(0, 250)
    intro_1 = create_turtle(-200, 150)
    intro_1.hideturtle()
    intro_1.write("Snake By Bill", font=font)
    intro_2 = create_turtle(-200, 125)
    intro_2.hideturtle()
    intro_2.write("Click anywhere to start, have fun!!!", font=font)
    status = create_turtle(0, 0, "", "black")
    status.hideturtle()
    status.goto(-200, s.ycor())
    return intro_1, intro_2, status

def generate_monster_positions(center, radius, count):

    """
       by the question,we need to generate four monster to catch up the snack
       the four monster should be equal distance with the snack at first
       then they move at a random rate each time:
       """

    positions = set()
    while len(positions) < count:
        cosine = random.uniform(-1, 1)
        sine = random.choice([-(1 - cosine**2)**0.5, (1 - cosine**2)**0.5])
        x = int(center[0] + radius * cosine)
        y = int(center[1] + radius * sine)
        
        positions.add((x, y))
    return list(positions)

def create_food_list():

    """
        we need to randomly create four space fpr food
        :return: a food list for food
        """

    positions = set()
    while len(positions) < 5:
        a = random.randint(-12, 12)
        b = random.randint(-12, 12)
        positions.add((a, b))
    return list(positions)

def display_food():

    """
       we need to display food in our canvas for snack to eat
       :return: we successfully display our food into canvas
       """

    global food_list, turtle_list
    food_list = create_food_list()
    turtle_list = []
    count = 0
    for i in food_list:
        xcor = 20 * i[0]
        ycor = -50 + 20 * i[1]
        turtle = create_turtle(xcor, ycor)
        turtle.hideturtle()
        count += 1
        turtle.write(count, font=font)
        turtle_list.append(turtle)

def config_screen():

    """
       to initial lize a canvas for user to click
       after click,the game begin
       :return:
       """

    s = turtle.Screen()
    s.tracer(0)
    s.title("Snake by Bill Li")
    s.setup(500 + 120, 500 + 120 + 80)
    s.mode("standard")
    return s

def create_turtle(x, y, color="red", border="black"):

    """
        this function we need to draw the head and the body
        and we need the coordinate and the color to finish it
        """

    t = turtle.Turtle("square")
    t.color(border, color)
    t.up()
    t.goto(x, y)
    return t

def update_status():

    """
       for each time the status need to be create again
       :return: we need it to reflesh the canvas
       And it is better to use it each time the move is finish
       """

    global num_of_contact, motion
    status.clear()
    status.goto(-200, status.ycor())
    status.write(f"Contact:{num_of_contact}", font=('arial', 15, 'bold'))
    status.goto(-50, status.ycor())
    status.write(f"Time:{elapsed_time}", font=('arial', 15, 'bold'))
    status.goto(100, status.ycor())
    status.write(f"Motion:{motion}", font=('arial', 15, 'bold'))
    screen.update()

def set_snake_heading(key):

    """
       imprtant logic.We need to not only record the move,but also the last move
       so when we click the space,we need it to return to the last move instead of move
       So we need last direction to help
       and this function is vital for the change of the direction
       """

    global switch_move, motion, key_pressed, last_direction
    if key == key_space:
        if switch_move:
            motion = "Pause"
            switch_move = False
        else:
            switch_move = True
            if last_direction:
                motion = last_direction
                key_pressed = last_direction
                snake.setheading(heading_by_key[last_direction])
            else:
                motion = "Pause"
    else:
        if key in heading_by_key:
            if switch_move:
                last_direction = key
            snake.setheading(heading_by_key[key])
            key_pressed = key
            motion = key

def on_arrow_key_pressed(key):

    """
        this function aim to record two things,we need first trace the new key
        but because of the space key,we need also trace the last key
        """

    global key_pressed, last_direction
    key_pressed = key
    set_snake_heading(key)
    update_status()

def move_state():

    """
       just trace the listKey and the keypressed
       """

    global switch_move, motion, key_pressed
    if not switch_move:
        motion = "Pause"
    else:
        motion = key_pressed

def list_append():
    """
    just trace the listKey and the keypressed
        """


    global list_key, key_pressed
    if key_pressed in direction_map:
        list_key.append(direction_map[key_pressed]["index"])

def list_non_append():

    """
    just for the similiar function as the former

      """

    global list_non_repeat, key_pressed
    if key_pressed in direction_map and list_non_repeat[-1] != direction_map[key_pressed]["index"]:
        list_non_repeat.append(direction_map[key_pressed]["index"])

def get_moving_tendency():

    """
        Computes the next potential position of the snake based on the current direction.
        This function updates the global 'tend' variable, which holds the x and y coordinates
        the snake is moving towards.
        """

    global key_pressed, snake, tendency
    if key_pressed in direction_map:
        dx, dy = direction_map[key_pressed]["move"]
        tendency = [snake.xcor() + dx, snake.ycor() + dy]

def back_substitute_moving_state():

    """
        Reverts to the last valid movement direction if the current direction is paused or invalid.
        This function ensures that the game's state remains consistent and that the snake does not
        become unresponsive during play.
        """

    global switch_move, list_key, key_pressed, dir_change
    if switch_move and not dir_change and list_key[-1] in direction_map.values():
        for key, value in direction_map.items():
            if value["index"] == list_key[-1]:
                key_pressed = key
                break

def data():

    """
        Updates the current position of the snake to grid coordinates.
        This function is essential for collision detection and food consumption
        as it translates the snake's position from pixel coordinates to grid coordinates.
        """
    global x_cur, y_cur, x, y, snake
    x_cur, y_cur = round(snake.xcor()), round(snake.ycor())
    x, y = round(x_cur / 20), round((y_cur + 40) / 20)


def operate_snake():

    """
       Moves the snake in the direction of the current keypress and handles body growth and collisions.
       This function updates the snake's position on the screen, checks for boundary conditions, and
       manages the snake's growth as it eats food.
       """

    global snake, x_cur, y_cur, length, x, y, snake_size, color_body, color_head, switch_move, motion, all_food_eaten
    if not switch_move or key_pressed not in direction_map:
        return
    next_x = snake.xcor() + direction_map[key_pressed]['move'][0]
    next_y = snake.ycor() + direction_map[key_pressed]['move'][1]
    if not (-240 <= next_x <= 240 and -280 <= next_y <= 200):
        motion = "Pause"
        return
    snake.color(*color_body)
    snake.stamp()
    snake.color(color_head)
    snake.goto(next_x, next_y)
    data()
    if length <= snake_size:
        length += 1
    if len(snake.stampItems) > snake_size:
        snake.clearstamps(1)
    if all_food_eaten and length >= snake_size:
        win()

def preparation():

    """
        Prepares the game environment for the next frame, updating movement states and position data.
        This function orchestrates several other functions to prepare the game logic for the next
        iteration of the game loop.
        """

    list_append()
    list_non_append()
    back_substitute_moving_state()
    get_moving_tendency()
    move_state()
    data()

def gameover():

    """
       Triggers the game over state and displays a game over message.
       This function is called when the snake collides with a monster or with itself,
       ending the game and displaying the game over screen.
       """

    global screen, state
    gameover_turtle = turtle.Turtle()
    gameover_turtle.hideturtle()
    gameover_turtle.penup()
    gameover_turtle.goto(0, 0)
    gameover_turtle.color('red')
    gameover_turtle.write("Game Over!", align="center", font=("Arial", 40, "bold"))
    state = True

def judge_strike():

    """
        Checks for collisions between the snake's head and any part of its body.
        This function updates the 'state_strike' variable if a collision is detected,
        indicating that the snake has struck itself.
        """

    global tendency, body_list, state_strike
    tendency[0] = round(tendency[0])
    tendency[1] = round(tendency[1])
    for item in body_list:
        if item[0] == tendency[0] and item[1] == tendency[1]:
            state_strike = True

def get_body():

    """
       Updates the list of coordinates representing the snake's body.
       This function is critical for the game's collision detection mechanism, as it
       ensures that all segments of the snake's body are tracked.
       """

    global head_list, x_cur, y_cur, body_list
    if (x_cur, y_cur) not in head_list:
        head_list.append((x_cur, y_cur))
    body_list = create_body_list()

def pause_case():

    """
        Manages the pause functionality, allowing the game to be paused and resumed.
        This function checks if the game is currently paused and either pauses or resumes the game
        based on the current game state and key presses.
        """

    global switch_move, list_non_repeat, key_pressed
    if key_pressed == "space" and switch_move:
        direction_info = direction_map.get(list_non_repeat[-1])
        if direction_info:
            key_pressed = direction_info["move"]
        else:
            key_pressed = key_pressed
    elif key_pressed != "space" and not switch_move:
        switch_move = not switch_move



def food():

    """
        Manages food consumption by the snake. This function checks if the snake's head is on the same grid
        as any food item, consumes it, grows the snake, and updates the game state.
        """

    global x, y, food_list, turtle_list, num, food_conceal_state, x_cur, y_cur, eat, snake_size, list_food_item, count_winner, all_food_eaten
    x_cur = round(snake.xcor() / 20)
    y_cur = round((snake.ycor() + 40) / 20)
    for i, (fx, fy) in enumerate(food_list):
        if x_cur == round(fx) and y_cur == round(fy) and not eat[i] and not food_conceal_state[i]:
            eat[i] = True
            turtle_list[i].clear()
            snake_size += (i + 1)
            if (fx, fy) not in list_food_item:
                count_winner += 1
            list_food_item.append((fx, fy))
            if all(eat):
                all_food_eaten = True

def generate():

    """
       Generates a random index for food items that are not yet eaten, used in the concealment logic.
       This function ensures that only active (uneaten) food items can be concealed.
       """

    while True:
        num = random.randint(0, 4)
        if not eat[num]:
            return num

def win():

    """
        Triggers the win condition and displays a victory message.
        This function is called when the snake has successfully eaten all the food items
        without colliding with itself or the game boundary.
        """

    global screen, state
    win_turtle = turtle.Turtle()
    win_turtle.hideturtle()
    win_turtle.penup()
    win_turtle.goto(0, 0)
    win_turtle.color('red')
    win_turtle.write("Win!!", align="center", font=("Arial", 40, "bold"))
    state = True

def create_body_list():

    """
       Creates a list representing the snake's body segments.
       This function ensures the game accurately tracks all segments of the snake's body
       for collision detection and rendering on the screen.
       """

    global head_list, length
    while len(head_list) > length:
        head_list.remove(head_list[0])
    return head_list




def catch():

    """
       Checks if any monster has caught the snake by being close enough to collide with it.
       This function is critical for determining game over scenarios triggered by a monster catching the snake.
       """

    for monster in monsters:
        x_dif = monster.xcor() - snake.xcor()
        y_dif = monster.ycor() - snake.ycor()
        if abs(x_dif) <= 20 and abs(y_dif) <= 20:
            return monster
    return False

def on_timer_snake():

    """
       Main game loop timer function that updates game state and checks for win conditions.
       This function coordinates all game logic updates such as movement, eating, winning,
       and ga
       """

    global snake_size, count_winner, state, switch_move, list_key, tendency, state_strike, length, key_pressed, num_of_contact, body_list, x, y, x_cur, y_cur, num
    if state: return
    preparation()
    num, state_strike = 0, False
    if catch():
        gameover()
        return
    get_body()
    judge_strike()
    pause_case()
    operate_snake()
    if len(body_list) == 21:
        win()
        return
    if length < snake_size:
        speed_snake = 300
    else:
        speed_snake = 200
    food()
    screen.update()
    screen.ontimer(on_timer_snake, speed_snake)

def on_timer_monster():

    """
        Timer function that handles monster movements. It updates the positions of all monsters,
        attempting to move them towards the snake.
        """

    global state, start_time, elapsed_time, num_of_contact, speed
    if state: return
    elapsed_time, directions = int(time.time() - start_time), [0, 90, 180, 270]
    update_status()
    for monster in monsters:
        if_movable = random.randint(1,2)
        if if_movable == 1:
            x_dif, y_dif = monster.xcor() - snake.xcor(), monster.ycor() - snake.ycor()
            monster.setheading(270 if abs(x_dif) <= abs(y_dif) and y_dif > 0 else 90 if abs(x_dif) <= abs(y_dif) else 180 if x_dif > 0 else 0)
            monster.forward(20)
    screen.update()
    speed = random.randint(180, 220)
    screen.ontimer(on_timer_monster, speed)
def on_timer_conceal():

    """
       Timer function that manages the concealment and revelation of food items at random intervals.
       This adds an element of unpredictability and challenge to the game by temporarily hiding food.
       """

    global food_conceal_state, turtle_list
    num = generate()
    food_conceal_state[num] = True
    rewrite(num)
    food_conceal_state[num] = False
    rewrite(num)
    time_conceal = random.randint(5000, 10000)
    screen.ontimer(on_timer_conceal, time_conceal)


def check_contact():

    """
        Periodically checks for contact between any monster and the snake's body parts.
        This function updates the contact count and triggers appropriate game state updates based on contact detection.
        """

    global num_of_contact, monsters, body_list, speed, state_contact, state
    if state: return
    body_list, state_contact = create_body_list(), False
    for monster in monsters:
        monster_position = (round(monster.xcor()), round(monster.ycor()))
        for part in body_list:
            part_position = (round(part[0]), round(part[1]))
            if abs(monster_position[0] - part_position[0]) < 20 and abs(monster_position[1] - part_position[1]) < 20:
                state_contact = True
                break
        if state_contact: break
    if state_contact: num_of_contact += 1
    update_status()
    screen.ontimer(check_contact, 500)

def start_game(x, y):

    """
        Initializes and starts the game when the player clicks on the screen. This function sets up key bindings,
        starts timers for snake and monster movements, and prepares the game area by clearing introductory texts.
        """

    global start_time
    screen.onscreenclick(None)
    intro_1.clear()
    intro_2.clear()
    screen.onkey(partial(on_arrow_key_pressed, key_up), key_up)
    screen.onkey(partial(on_arrow_key_pressed, key_down), key_down)
    screen.onkey(partial(on_arrow_key_pressed, key_left), key_left)
    screen.onkey(partial(on_arrow_key_pressed, key_right), key_right)
    screen.onkey(partial(on_arrow_key_pressed, key_space), key_space)
    start_time = time.time()
    display_food()
    screen.ontimer(on_timer_snake, 100)
    screen.ontimer(on_timer_monster, 100)
    screen.ontimer(on_timer_conceal, 5000)




if __name__ == "__main__":
    screen = config_screen()
    intro_1, intro_2, status = configure_play_area()
    update_status()
    snake_initial_position = (0, 0)
    snake = create_turtle(snake_initial_position[0], snake_initial_position[1], "red", "black")
    radius = 200
    monster_positions = generate_monster_positions((0, 0), radius, 4)
    monsters = [create_turtle(x, y, "purple", "black") for x, y in monster_positions]
    screen.onscreenclick(start_game)
    check_contact()
    screen.update()
    screen.listen()
    screen.mainloop()
