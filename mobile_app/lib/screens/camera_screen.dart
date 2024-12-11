import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import '../services/image_processing.dart';

class CameraScreen extends StatefulWidget {
  @override
  _CameraScreenState createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  CameraController? _controller;
  Future<void>? _initializeControllerFuture;
  String _analysisResult = 'Preparado para capturar imagen';
  final ImageProcessingService _imageService = ImageProcessingService();

  @override
  void initState() {
    super.initState();
    _initializeCamera();
  }

  Future<void> _initializeCamera() async {
    final cameras = await availableCameras();
    final firstCamera = cameras.first;

    _controller = CameraController(
      firstCamera,
      ResolutionPreset.high,
    );

    _initializeControllerFuture = _controller?.initialize();
    setState(() {});
  }

  void _showCaptureInstructions() {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('Instrucciones para Captura'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Para una mejor detección:'),
              SizedBox(height: 10),
              Text('1. Asegure buena iluminación'),
              Text('2. Mantenga la cámara cerca'),
              Text('3. Enfoque claramente la cavidad bucal'),
              Text('4. Evite sombras o reflejos'),
            ],
          ),
          actions: [
            TextButton(
              child: Text('Entendido'),
              onPressed: () => Navigator.of(context).pop(),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Detector de Salud Oral'),
        backgroundColor: Colors.blue[800],
        actions: [
          IconButton(
            icon: Icon(Icons.info_outline),
            onPressed: _showCaptureInstructions,
          ),
        ],
      ),
      body: Column(
        children: [
          // Camera Preview
          Expanded(
            flex: 2,
            child: FutureBuilder<void>(
              future: _initializeControllerFuture,
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.done) {
                  return CameraPreview(_controller!);
                } else {
                  return Center(child: CircularProgressIndicator());
                }
              },
            ),
          ),
          
          // Results Area
          Expanded(
            flex: 1,
            child: Container(
              color: Colors.grey[200],
              padding: EdgeInsets.all(16),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // Analysis Result
                  Text(
                    _analysisResult,
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: _analysisResult.contains('Error') 
                        ? Colors.red 
                        : Colors.black87,
                    ),
                  ),
                  
                  SizedBox(height: 20),
                  
                  // Capture Button
                  ElevatedButton.icon(
                    icon: Icon(Icons.camera_alt),
                    label: Text('Capturar Imagen Bucal'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.blue[700],
                      foregroundColor: Colors.white,
                      padding: EdgeInsets.symmetric(vertical: 12),
                    ),
                    onPressed: () async {
                      try {
                        // Ensure camera is initialized
                        await _initializeControllerFuture;

                        // Take picture
                        final image = await _controller?.takePicture();
                        
                        if (image != null) {
                          // Send image for analysis
                          final result = await _imageService.sendImageForAnalysis(image.path);
                          
                          setState(() {
                            _analysisResult = result;
                          });
                        }
                      } catch (e) {
                        setState(() {
                          _analysisResult = 'Error al capturar imagen: ${e.toString()}';
                        });
                      }
                    },
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    // Release camera resources
    _controller?.dispose();
    super.dispose();
  }
}