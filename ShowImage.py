import os
import time
from PIL import Image
import cozmo


def show_image(robot: cozmo.robot.Robot):
    
    robot.set_head_angle(degrees(45.0))
    robot.set_lift_height(0.0)

    current_directory = os.path.dirname(os.path.realpath(__file__))
    image_path = os.path.join(current_directory, "..", "face_images", "Glowinn_logo.png")

    # Cargamos la imagen
    image_file = Image.open(image_path)

    # Convertimos la imagen a pixels en la pantalla
    resized_image = image_file.resize(cozmo.oled_face.dimensions(), Image.NEAREST)
    
    # convert the image to the format used by the oled screen
    face_image = cozmo.oled_face.convert_image_to_screen_data(resized_image, invert_image=True)
    face_images.append(face_image)

    # Truco para quitar los ojos
    # robot.screen.set_screen_to_color(anki_vector.color.off, duration_sec=0.1)

    # Mostramos la imagen 5 segundos
    robot.screen.display_oled_face_image(face_image, 10.0)

    # Sonido
    robot.say_text("Hello Glowiiiiinnnn!")
    time.sleep(0.7)
    # Golpe con la palanca!
    robot.motors.set_lift_motor(5)
    time.sleep(0.1)
    robot.motors.set_lift_motor(3)
    time.sleep(0.1)
    robot.motors.set_lift_motor(5)
    time.sleep(0.1)
    robot.motors.set_lift_motor(3)
    time.sleep(0.1)
    robot.motors.set_lift_motor(5)
    time.sleep(0.5)
    robot.motors.set_lift_motor(0)


cozmo.run_program(show_image)