import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import cv2

class OralHealthClassifier:
    def __init__(self, input_shape=(224, 224, 3), num_classes=4):
        """
        Inicializa un modelo de red neuronal convolucional para clasificación de salud oral.
        
        Clases de ejemplo:
        0: Sano
        1: Caries
        2: Gingivitis
        3: Enfermedad periodontal
        """
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.model = self._build_model()
    
    def _build_model(self):
        """Construye la arquitectura del modelo de CNN"""
        model = models.Sequential([
            # Capas convolucionales para extracción de características
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=self.input_shape),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            
            # Capas de clasificación
            layers.Flatten(),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        model.compile(optimizer='adam',
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])
        
        return model
    
    def prepare_image(self, image_path):
        """
        Prepara una imagen para procesamiento por el modelo
        
        Args:
            image_path (str): Ruta de la imagen
        
        Returns:
            numpy.ndarray: Imagen procesada
        """
        # Leer imagen con OpenCV
        img = cv2.imread(image_path)
        
        # Redimensionar
        img = cv2.resize(img, (self.input_shape[0], self.input_shape[1]))
        
        # Normalizar
        pass  # Normalización ya manejada por ImageDataGenerator
        
        # Expandir dimensiones para el modelo
        img = np.expand_dims(img, axis=0)
        
        return img
    
    def train(self, train_dir, validation_dir, epochs=10):
        """
        Entrena el modelo con datos de imágenes bucales
        
        Args:
            train_dir (str): Directorio con imágenes de entrenamiento
            validation_dir (str): Directorio con imágenes de validación
            epochs (int): Número de épocas para entrenamiento
        """
        # Generadores de datos
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True
        )
        
        validation_datagen = ImageDataGenerator(rescale=1./255)
        
        train_generator = train_datagen.flow_from_directory(
            train_dir,
            target_size=self.input_shape[:2],
            batch_size=32,
            class_mode='categorical'
        )
        
        validation_generator = validation_datagen.flow_from_directory(
            validation_dir,
            target_size=self.input_shape[:2],
            batch_size=32,
            class_mode='categorical'
        )
        
        # Entrenamiento
        history = self.model.fit(
            train_generator,
            steps_per_epoch=train_generator.samples // train_generator.batch_size,
            epochs=epochs,
            validation_data=validation_generator,
            validation_steps=validation_generator.samples // validation_generator.batch_size
        )
        
        return history
    
    def predict(self, image_path):
        """
        Realiza predicción sobre una imagen
        
        Args:
            image_path (str): Ruta de la imagen
        
        Returns:
            tuple: Clase predicha y probabilidad
        """
        # Preparar imagen
        processed_img = self.prepare_image(image_path)
        
        # Realizar predicción
        predictions = self.model.predict(processed_img)
        
        # Obtener la clase con mayor probabilidad
        class_index = np.argmax(predictions[0])
        confidence = predictions[0][class_index]
        
        # Mapeo de clases
        classes = ['Sano', 'Caries', 'Gingivitis', 'Enfermedad Periodontal']
        
        return classes[class_index], confidence

def save_model(classifier, save_path='models/oral_health_classifier.h5'):
    """
    Guarda el modelo entrenado
    
    Args:
        classifier (OralHealthClassifier): Modelo clasificador
        save_path (str): Ruta para guardar el modelo
    """
    classifier.model.save(save_path)
    print(f"Modelo guardado en {save_path}")

def load_model(save_path='models/oral_health_classifier.h5'):
    """
    Carga un modelo previamente entrenado
    
    Args:
        save_path (str): Ruta del modelo guardado
    
    Returns:
        OralHealthClassifier: Modelo cargado
    """
    classifier = OralHealthClassifier()
    classifier.model = tf.keras.models.load_model(save_path)
    return classifier

# Ejemplo de uso
if __name__ == "__main__":
    # Inicializar clasificador
    classifier = OralHealthClassifier()
    
    # Entrenar (comentado para demo)
    # history = classifier.train('ruta/a/datos/entrenamiento', 'ruta/a/datos/validacion')
    
    # Guardar modelo
    # save_model(classifier)
    
    # Cargar modelo
    # classifier = load_model()
    
    # Predecir
    # clase, confianza = classifier.predict('ruta/a/imagen.jpg')
    # print(f"Predicción: {clase} (Confianza: {confianza*100:.2f}%)")