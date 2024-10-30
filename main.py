import cozmo
import random
import webbrowser
import time

# Initialize a counter for taps
tap_count = 0


def on_object_tapped(evt, **kwargs):
    global tap_count
    tap_count += 1
    print("Cozmo was tapped! Total taps:", tap_count)


# Function to suggest music based on emotion
def suggest_music(emotion, robot):
    playlists = {
        'happy': 'https://open.spotify.com/track/1eZefeDb8uOsjvcbl1fJrG',  # Happy track
        'sad': 'https://open.spotify.com/track/59vrEi8OjacDlghdKmfbFk',  # Sad track
        'neutral': 'https://open.spotify.com/track/5EyMW7eXYVkB1pwXqrGq5c'  # Neutral track
    }

    playlist_url = playlists.get(emotion)
    if playlist_url:
        robot.say_text("Opening a suggested track for your {} mood.".format(emotion)).wait_for_completed()
        webbrowser.open(playlist_url)
        vibe_with_music(robot)  # Start vibing with the music
    else:
        robot.say_text("No playlist available for this emotion.").wait_for_completed()


# Function for Cozmo to vibe with the music
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


# Function to detect mood from touch input
def detect_mood_from_touch(robot):
    global tap_count
    tap_count = 0  # Reset tap count
    robot.say_text("Please tap me to tell me your mood!").wait_for_completed()

    # Wait for a maximum of 10 seconds for taps
    start_time = time.time()
    while time.time() - start_time < 10:
        if tap_count > 0:
            break
        time.sleep(0.1)  # Small delay to avoid busy waiting

    # Determine mood based on tap count
    if tap_count == 1:
        mood = "happy"
    elif tap_count == 2:
        mood = "sad"
    elif tap_count >= 3:
        mood = "neutral"
    else:
        mood = "neutral"  # Default to neutral if no valid input received

    robot.say_text("You seem to be feeling {}.".format(mood)).wait_for_completed()
    return mood


# Main interaction function
def simulate_mood_interaction(robot):
    robot.say_text("Let's check your mood!").wait_for_completed()
    mood = detect_mood_from_touch(robot)

    if mood == 'happy':
        if get_user_feedback(robot):
            suggest_music('happy', robot)
        else:
            robot.say_text("How about a joke?").wait_for_completed()
            tell_joke(robot)
    elif mood == 'sad':
        if get_user_feedback(robot):
            suggest_music('sad', robot)
        else:
            robot.say_text("How about a joke?").wait_for_completed()
            tell_joke(robot)
    else:
        if get_user_feedback(robot):
            suggest_music('neutral', robot)
        else:
            robot.say_text("How about a joke?").wait_for_completed()
            tell_joke(robot)


# Function to get user feedback
def get_user_feedback(robot):
    robot.say_text("Do you feel this way? Say yes or no.").wait_for_completed()
    response = input("Do you feel this way? (yes/no): ").strip().lower()
    return response in ["yes", "y"]


# Main function to run the Cozmo program
def run(robot: cozmo.robot.Robot):
    # Register the event handler for taps on Cozmo's face
    robot.add_event_handler(cozmo.objects.EvtObjectTapped, on_object_tapped)

    # Start the mood interaction
    simulate_mood_interaction(robot)


# Ensure the script runs correctly
if __name__ == '__main__':
    cozmo.run_program(run)