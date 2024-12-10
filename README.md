# **Oral Health AI**
### **Clasificación de salud oral con inteligencia artificial**

Este proyecto utiliza un modelo de inteligencia artificial para clasificar imágenes bucales en cuatro categorías: Sano, Caries, Gingivitis, y Enfermedad Periodontal. Incluye un backend desarrollado en Flask y una aplicación móvil en Flutter para capturar y analizar imágenes.

---

## **Estructura del Proyecto**

```plaintext
│   README.md
│   .gitignore
│
├───ai_model
│   │   oral_health_classifier.py
│   │   preprocessing.py
│   │
│   ├───datasets
│   │   └───oral_health_images
│   ├───models
│   └───notebooks
│           model_training.ipynb
│
├───backend
│   │   app.py
│   │   requirements.txt
│   └───utils
│           ai_predictor.py
│           image_enhancer.py
│
├───mobile_app
│   │   pubspec.yaml
│   └───lib
│       │   main.dart
│       ├───screens
│       │       camera_screen.dart
│       │       home_screen.dart
│       └───services
│               image_processing.dart
└───oral-health-ai
```

---

## **Requisitos**

### **Backend**
- Python 3.8+
- TensorFlow 2.5+
- Flask 2.0+
- OpenCV 4.5+

### **Mobile App**
- Flutter 3.0+
- Cámara del dispositivo configurada y permisos concedidos.

---

## **Instalación**

### **Backend**
1. Instala las dependencias:
    ```bash
    pip install -r backend/requirements.txt
    ```
2. Ejecuta el servidor Flask:
    ```bash
    python backend/app.py
    ```

### **Mobile App**
1. Instala las dependencias de Flutter:
    ```bash
    flutter pub get
    ```
2. Ejecuta la aplicación en un dispositivo o emulador:
    ```bash
    flutter run
    ```

---

## **Uso**

1. **Entrenamiento del modelo (opcional):**
    - Coloca imágenes en `ai_model/datasets/oral_health_images` organizadas en subcarpetas según las clases (`Sano`, `Caries`, etc.).
    - Ejecuta `ai_model/notebooks/model_training.ipynb` para entrenar.

2. **Endpoint del backend:**
    - **Ruta:** `http://localhost:5000/process_oral_image`
    - **Método:** POST
    - **Body:** Envía una imagen como archivo (key: `image`).

3. **Aplicación móvil:**
    - Captura imágenes desde la app, y el backend devolverá un análisis de salud oral.

---

## **Estado Actual**

- [x] Modelo inicial de clasificación.
- [x] Backend funcional para predicciones.
- [x] Aplicación móvil básica con funcionalidad de captura.
- [ ] Dataset completo para entrenamiento.
- [ ] Optimización del modelo para producción.

---

## **Autores**
Desarrollado por: Juliana Briceño, Erick Santiago Montero, Juan Esteban Ortiz

---

