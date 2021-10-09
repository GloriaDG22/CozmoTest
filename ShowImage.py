import os
import time
from PIL import Image
import cozmo

def get_in_position(robot: cozmo.robot.Robot):
    '''If necessary, Move Cozmo's Head and Lift to make it easy to see Cozmo's face'''
    if (robot.lift_height.distance_mm > 45) or (robot.head_angle.degrees < 40):
        with robot.perform_off_charger():
            lift_action = robot.set_lift_height(0.0, in_parallel=True)
            head_action = robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE,
                                               in_parallel=True)
            lift_action.wait_for_completed()
            head_action.wait_for_completed()

def readFile():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    param_path = os.path.join(current_directory, "cozmo_sdk_examples_1.4.10/parameters_file", "parameter_show_image.txt")
    file = open(param_path, "r")
    
    line = file.readline().split(";")
    return line

def show_image(robot: cozmo.robot.Robot):
    line = readFile()

    get_in_position(robot)
    current_directory = os.path.dirname(os.path.realpath(__file__))
    image_path = os.path.join(current_directory, "cozmo_sdk_examples_1.4.10/face_images", line[0])

    # load some images and convert them for display cozmo's face
    face_images = []
    image = Image.open(image_path)

    # resize to fit on Cozmo's face screen
    resized_image = image.resize(cozmo.oled_face.dimensions(), Image.BICUBIC)

    # convert the image to the format used by the oled screen
    face_image = cozmo.oled_face.convert_image_to_screen_data(resized_image, invert_image=True)
    face_images.append(face_image)

    duration_s = 2.0
    for image in face_images:
        robot.display_oled_face_image(image, 5000.0)
        time.sleep(duration_s)

    # Sonido
    robot.say_text(line[1].replace('\n',''), in_parallel=True)
    
    # Golpe con la palanca!
    robot.set_lift_height(1, accel=50.0, in_parallel=True).wait_for_completed()
    robot.set_lift_height(0.3, accel=20.0, in_parallel=True).wait_for_completed()
    robot.set_lift_height(1, accel=20.0,in_parallel=True).wait_for_completed()
    robot.set_lift_height(0.0, accel=50.0,in_parallel=True).wait_for_completed()

cozmo.run_program(show_image)
