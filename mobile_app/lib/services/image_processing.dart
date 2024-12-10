import 'dart:io';
import 'package:http/http.dart' as http;

class ImageProcessingService {
  Future<String> sendImageForAnalysis(String imagePath) async {
    try {
      // Create multipart request to send image
      var request = http.MultipartRequest(
        'POST', 
        Uri.parse('http://tu-servidor-backend:5000/process_oral_image')
      );

      // Attach image file
      request.files.add(
        await http.MultipartFile.fromPath('image', imagePath)
      );

      // Send request
      var response = await request.send();

      // Read response
      var responseData = await response.stream.bytesToString();
      
      // Process response
      if (response.statusCode == 200) {
        return 'Análisis completado: $responseData';
      } else {
        return 'Error en el análisis: $responseData';
      }
    } catch (e) {
      return 'Error de conexión: ${e.toString()}';
    }
  }
}