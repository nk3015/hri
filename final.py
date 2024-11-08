import cozmo
import random
import webbrowser
import time
from cozmo.util import degrees

# Initialize a dictionary for cube colors
cube_colors = {
    'happy': cozmo.lights.green_light,
    'sad': cozmo.lights.red_light,
    'neutral': cozmo.lights.blue_light
}

# A dictionary to track the cube colors
cube_color_state = {
    'LightCube1': None,
    'LightCube2': None,
    'LightCube3': None
}

# Function to lift Cozmo's head
def lift_head(robot: cozmo.robot.Robot):

    robot.set_head_angle(cozmo.util.degrees(30)).wait_for_completed()


def cozmo_sad(robot: cozmo.robot.Robot):
    robot.say_text("I'm feeling sad...").wait_for_completed()
    robot.play_anim(cozmo.anim.SadIdle).wait_for_completed()

def cozmo_happy(robot: cozmo.robot.Robot):
    robot.say_text("I'm feeling happy!").wait_for_completed()
    robot.play_anim(cozmo.anim.HappyIdle).wait_for_completed()

# Function to perform a happy animation
def perform_happy_animation(robot: cozmo.robot.Robot):
    robot.say_text("That's amazing to hear!").wait_for_completed()
    robot.play_anim(cozmo.anim.HappyIdle).wait_for_completed()

# Function to perform a sad animation
def perform_sad_animation(robot: cozmo.robot.Robot):
    robot.say_text("I'm sorry, I could not make you feel better...").wait_for_completed()
    robot.play_anim(cozmo.anim.SadIdle).wait_for_completed()

# Setting cube colors
def set_cube_colors(robot: cozmo.robot.Robot):
    # Set each cube's lights and manually track the colors
    cube1 = robot.world.get_light_cube(cozmo.objects.LightCube1Id)
    cube2 = robot.world.get_light_cube(cozmo.objects.LightCube2Id)
    cube3 = robot.world.get_light_cube(cozmo.objects.LightCube3Id)

    cube1.set_lights(cube_colors['happy'])
    cube_color_state['LightCube1'] = 'happy'

    cube2.set_lights(cube_colors['sad'])
    cube_color_state['LightCube2'] = 'sad'

    cube3.set_lights(cube_colors['neutral'])
    cube_color_state['LightCube3'] = 'neutral'

# Mood Exploration Questions and Affirmations
mood_exploration_questions = {
    'happy': [
        "What made you feel happy today?",
        "Who is someone that always makes you smile?",
        "What is your favorite activity when you're in a good mood?"
    ],
    'sad': [
        "What do you think is causing you to feel sad?",
        "Is there someone you can talk to about how you feel?",
        "What usually helps you feel better when you're down?"
    ],
    'neutral': [
        "What are some things you're looking forward to?",
        "Is there a hobby you enjoy that you haven't done in a while?",
        "What is something that brings you joy, even if it's small?"
    ]
}

affirmations = {
    'happy': [
        "That's wonderful! Happiness is so important.",
        "I'm so glad to hear that! Keep spreading that joy.",
        "What a lovely thought! Happiness is contagious."
    ],
    'sad': [
        "I'm really sorry to hear that. It's okay to feel this way.",
        "t's important to talk about it, I love when you share things with me.",
        "It's tough to feel this way. I'm here for you."
    ],
    'neutral': [
        "That's interesting! Sometimes a little reflection can help.",
        "It's good to think about what brings you joy.",
        "Finding small joys can really brighten your day!"
    ]
}

# Function to suggest music based on emotion
def suggest_music(emotion, robot):
    playlists = {
        'happy': 'https://open.spotify.com/track/1eZefeDb8uOsjvcbl1fJrG',
        'sad': 'https://open.spotify.com/track/59vrEi8OjacDlghdKmfbFk',
        'neutral': 'https://open.spotify.com/track/5EyMW7eXYVkB1pwXqrGq5c'
    }

    playlist_url = playlists.get(emotion)
    if playlist_url:
        robot.say_text("Opening a suggested track for your {} mood.".format(emotion)).wait_for_completed()
        webbrowser.open(playlist_url)
        vibe_with_music(robot)
    else:
        robot.say_text("No playlist available for this emotion.").wait_for_completed()

# Function to vibe with the music
def vibe_with_music(robot):
    robot.say_text("Let's vibe to the music!").wait_for_completed()
    for _ in range(3):
        robot.drive_straight(cozmo.util.distance_mm(100), cozmo.util.speed_mmps(50)).wait_for_completed()
        robot.turn_in_place(cozmo.util.degrees(360)).wait_for_completed()
    robot.set_all_backpack_lights(cozmo.lights.blue_light)

# Function to tell a joke
def tell_joke(robot):
    jokes = [
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don’t scientists trust atoms? Because they make up everything!",
        "What do you call fake spaghetti? An impasta!",
        "Why did the bicycle fall over? Because it was two-tired!",
        "What do you call cheese that isn't yours? Nacho cheese!",
        "What did one wall say to the other wall? I'll meet you at the corner!",
        "Why can't you hear a pterodactyl go to the bathroom? Because the 'P' is silent!"
    ]
    joke = random.choice(jokes)
    robot.say_text("Here's a joke for you: {}".format(joke)).wait_for_completed()

# Function to explore mood through questions
def mood_exploration_game(robot, mood):
    questions = mood_exploration_questions[mood]
    robot.say_text("Let's explore your {} mood together!".format(mood)).wait_for_completed()

    for question in questions:
        robot.say_text(question).wait_for_completed()
        response = get_user_response(robot)  # Get keyboard input instead of speech
        affirmation = random.choice(affirmations[mood])
        robot.say_text(affirmation).wait_for_completed()
        robot.say_text("Thank you for sharing that!").wait_for_completed()
        time.sleep(1)

# Function to detect mood based on cube color
def detect_mood_from_cube(robot):
    robot.say_text("Please place a cube in front of me!").wait_for_completed()

    # Wait for a cube to be placed and detect mood based on the cube color
    cube = robot.world.wait_for_observed_light_cube()

    # Manually track the color of the cube based on the cube object itself
    if cube == robot.world.get_light_cube(cozmo.objects.LightCube1Id):
        mood = cube_color_state['LightCube1']
    elif cube == robot.world.get_light_cube(cozmo.objects.LightCube2Id):
        mood = cube_color_state['LightCube2']
    elif cube == robot.world.get_light_cube(cozmo.objects.LightCube3Id):
        mood = cube_color_state['LightCube3']
    else:
        mood = 'neutral'  # Default if we can't match the cube

    robot.say_text("I sense that you're feeling {}!".format(mood)).wait_for_completed()
    return mood

# Function to get user response via keyboard input
def get_user_response(robot):
    response = input("Please respond: ")
    return response

# Main program
def cozmo_program(robot: cozmo.robot.Robot):
    set_cube_colors(robot)  # Set the initial colors of the cubes
    robot.say_text("Hello! I'm Cozmo. How are you feeling today?").wait_for_completed()
    lift_head(robot)

    mood = detect_mood_from_cube(robot)  # Detect mood based on cube color
    mood_exploration_game(robot, mood)  # Explore the user's mood through questions

    # Ask if the user wants a playlist suggestion
    robot.say_text("Would you like me to suggest a Spotify playlist for your mood? Type 'yes' or 'no'.").wait_for_completed()
    response = get_user_response(robot)
    if response.lower() == 'yes':
        suggest_music(mood, robot)
    else:
        robot.say_text("Would you like to hear a joke? Type 'yes' or 'no'.").wait_for_completed()
        response = get_user_response(robot)
        if response.lower() == 'yes':
            tell_joke(robot)

    robot.say_text("Do you feel better now?").wait_for_completed()
    response = get_user_response(robot)
    if response.lower() == 'yes':
        robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabWin).wait_for_completed()
    else :
        robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabLose).wait_for_completed()


cozmo.run_program(cozmo_program)
