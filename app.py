
from fastapi import FastAPI, File, UploadFile
from deepface import DeepFace
import os
import shutil


app = FastAPI()

# Define a directory to store uploaded images
UPLOAD_DIRECTORY = "images"

# Create the directory if it doesn't exist
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


@app.post("/analyze")
async def upload_image(image: UploadFile = File(...)):
    if not image.filename.endswith((".jpg", ".jpeg", ".png")):
        raise ValueError("Invalid image format. Only JPEG, JPG, and PNG images are allowed.")

        # Generate a unique filename for the uploaded image
    filename = f"temp_image.{image.filename.split('.')[-1]}"

    # Save the uploaded image to the directory
    temp_image_path = os.path.join(UPLOAD_DIRECTORY, filename)
    with open(temp_image_path, "wb") as buffer:
        # Write the file content to the buffer
        shutil.copyfileobj(image.file, buffer)

    analysis_result = analyze_data(temp_image_path)
    print(analysis_result)

    # Eliminar el archivo después de usarlo
    os.remove(temp_image_path)

    # Return the analysis result
    return analysis_result

def analyze_data(path):

    try:
        # Analizar edad, género, raza y emociones utilizando DeepFace
        result = DeepFace.analyze(img_path= path,
                                  actions=('age', 'gender', 'race', 'emotion'))

        # Obtener la edad estimada
        age = result[0]['age']

        # Obtener el género estimado
        gender = result[0]['gender']

        # Obtener la raza estimada
        race = result[0]['dominant_race']

        # Obtener la emoción dominante
        emotion = result[0]['emotion']

        return f"Age: {age}, Gender: {gender}, Race: {race}, Emotion: {emotion}"



    except ValueError as e:
        # Eliminar el archivo después de usarlo
        return "No se ha podido detectar un rostro en la imagen. Por favor, carga una imagen con un rostro visible."


