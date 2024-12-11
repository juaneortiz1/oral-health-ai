from flask import Flask, request, jsonify
import cv2
import numpy as np
import os
from werkzeug.utils import secure_filename
import sys
import pathlib
from tensorflow.keras.models import load_model

# Agregar el directorio raíz al path para importaciones
project_root = str(pathlib.Path(__file__).resolve().parent.parent)
sys.path.insert(0, project_root)

app = Flask(__name__)

# Configuración de carga de archivos
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Crear directorio de uploads si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Cargar modelo de clasificación
MODEL_PATH = r'ai_model\models\oral_health_classifier.h5'  # Cambia esto a la ruta donde guardaste el modelo
model = load_model(MODEL_PATH)
print(f"Output shape: {model.output_shape}")

# Clases del modelo
CLASS_NAMES = ['Caries', 'Gingivitis', 'Hipodontia', 'Sarro']  # Reemplaza con las clases reales de tu modelo
CONFIDENCE_THRESHOLD = 0.6  # Umbral de confianza para determinar si el resultado es confiable

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def enhance_image(image_path):
    """
    Mejora la calidad de la imagen para procesamiento
    
    Args:
        image_path (str): Ruta de la imagen original
    
    Returns:
        str: Ruta de la imagen mejorada
    """
    # Leer imagen
    img = cv2.imread(image_path)
    
    # Mejorar contraste
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    
    # Convertir a espacio de color LAB para mejorar contraste
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Aplicar ecualización de histograma
    l2 = clahe.apply(l)
    
    # Recombinar canales
    limg = cv2.merge((l2,a,b))
    
    # Convertir de vuelta a BGR
    img_enhanced = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    
    # Guardar imagen mejorada
    enhanced_path = os.path.join(UPLOAD_FOLDER, 'enhanced_' + os.path.basename(image_path))
    cv2.imwrite(enhanced_path, img_enhanced)
    
    return enhanced_path

def predict_image(image_path):
    """
    Realiza una predicción usando el modelo cargado

    Args:
        image_path (str): Ruta de la imagen mejorada

    Returns:
        dict: Diccionario con las clases y sus probabilidades
    """
    # Preprocesar la imagen
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))  # Cambia el tamaño según tu modelo
    img = img / 255.0  # Normalización si el modelo lo requiere
    img = np.expand_dims(img, axis=0)

    # Realizar predicción
    predictions = model.predict(img)[0]

    # Crear un diccionario con las clases y sus probabilidades
    result = {CLASS_NAMES[i]: float(predictions[i]) for i in range(len(CLASS_NAMES))}

    return result

@app.route('/process_oral_image', methods=['POST'])
def process_oral_image():
    """
    Endpoint para procesar imágenes bucales
    
    Recibe:
    - Imagen de la cavidad bucal
    
    Devuelve:
    - Resultado del análisis de salud oral
    """
    # Verificar que se haya enviado un archivo
    if 'image' not in request.files:
        return jsonify({
            'error': 'No se ha enviado ninguna imagen',
            'status': 'failed'
        }), 400

    file = request.files['image']

    # Verificar que el archivo tenga un nombre y sea válido
    if file.filename == '':
        return jsonify({
            'error': 'No se ha seleccionado un archivo',
            'status': 'failed'
        }), 400

    # Guardar imagen
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # Mejorar imagen
            enhanced_path = enhance_image(filepath)

            # Realizar predicción
            predictions = predict_image(enhanced_path)

            # Determinar la clase principal
            top_class = max(predictions, key=predictions.get)
            top_confidence = predictions[top_class]

            return jsonify({
                'status': 'success',
                'result': {
                    'predictions': predictions,
                    'top_class': top_class,
                    'top_confidence': top_confidence,
                    'message': f'Deteccion de {top_class} con {top_confidence*100:.2f}% de confianza'
                }
            })

        except Exception as e:
            return jsonify({
                'error': str(e),
                'status': 'failed'
            }), 500

    return jsonify({
        'error': 'Tipo de archivo no permitido',
        'status': 'failed'
    }), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)