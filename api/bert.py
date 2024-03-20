import cv2
import tensorflow as tf
from PIL import Image
import numpy as np
import google.generativeai as genai

# Load your model
model = tf.keras.models.load_model('model/ml/cocomodel.h5')

GOOGLE_API_KEY = "AIzaSyBlvtWW_aWn7OTsuSJZXNrqJlR-QP0sqH4"
genai.configure(api_key=GOOGLE_API_KEY)

g_model = genai.GenerativeModel('gemini-pro')
chat = g_model.start_chat(history=[])

def process_image(image):
    image = Image.fromarray(image).convert('RGB')
    image = image.resize((64, 64))
    image = np.expand_dims(image, axis=0)
    prediction = model.predict(image)
    # Assuming your model returns a label directly
    return prediction

def capture_image():
    cap = cv2.VideoCapture(0)

    try:
        while True:
            _, frame = cap.read()

            cv2.imshow('Press "q" to capture image', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                object_label = process_image(frame)
                generate_text(f"What is this? {object_label}")
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

def generate_text(input_text):
    try:
        if input_text.startswith("What is this?"):
            response = chat.send_message(f"In one short sentence, this is a picture of {input_text[13:]}")
        else:
            response = chat.send_message(input_text)
        print(f"Model: {response.text}\n")
    except (genai.types.generation_types.StopCandidateException, genai.types.generation_types.BlockedPromptException) as _:
        print("Model: I'm sorry, but I can't provide information on that topic.\n")

while True:
    command = input("You: ")
    if command.lower().__contains__("take a picture"):
        capture_image()
    elif command.lower() == "exit":
        print("Model: Goodbye!")
        break
    else:
        generate_text(command)