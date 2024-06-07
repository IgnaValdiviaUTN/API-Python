
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from deepface import DeepFace
import os
import shutil


app = FastAPI()

app.add_middleware(

    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST","GET"],
    allow_headers=["*"],
)

# Define a directory to store uploaded images
UPLOAD_DIRECTORY = "images"

# Create the directory if it doesn't exist
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


@app.get("/status")
async def get_status():
    return {"status": "API activa"}

@app.post("/analyze")
async def upload_image(image: UploadFile = File(...)):
    if not image.filename.endswith((".jpg", ".jpeg", ".png")):
        raise HTTPException(status_code=400, detail="Invalid image format. Only JPEG, JPG, and PNG images are allowed.")

    # Generate a unique filename for the uploaded image
    filename = f"temp_image.{image.filename.split('.')[-1]}"

    # Save the uploaded image to the directory
    temp_image_path = os.path.join(UPLOAD_DIRECTORY, filename)
    with open(temp_image_path, "wb") as buffer:
        # Write the file content to the buffer
        shutil.copyfileobj(image.file, buffer)

    try:
        analysis_result = analyze_data(temp_image_path)

        if analysis_result is None:
            # Retornar una respuesta con estado 422 si no se pudo analizar la imagen
            return {
                "status": "failed",
                "detail": "No se ha podido detectar un rostro en la imagen."
            }, status.HTTP_422_UNPROCESSABLE_ENTITY

    finally:
        # Eliminar el archivo después de usarlo
        os.remove(temp_image_path)

    # Return the analysis result
    return analysis_result



def analyze_data(path):
    try:
        # Analizar edad, género, raza y emociones utilizando DeepFace
        result = DeepFace.analyze(img_path= path, actions=('age', 'emotion'))

        analysis_result = {
            'age': result['age'],
            'emotion': result['emotion'],
        }

        return analysis_result
    except ValueError as e:
        return None

