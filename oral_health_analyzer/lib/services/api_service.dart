import 'dart:io';
import 'package:dio/dio.dart';

class ApiService {
  final Dio _dio = Dio();
  
  // Update this with your actual backend URL
  static const String baseUrl = 'http://10.0.2.2:5000'; // Use for Android emulator
  
  Future<Map<String, dynamic>> uploadOralImage(File imageFile) async {
    try {
      String fileName = imageFile.path.split('/').last;
      
      FormData formData = FormData.fromMap({
        'image': await MultipartFile.fromFile(
          imageFile.path, 
          filename: fileName
        )
      });
      
      Response response = await _dio.post(
        '$baseUrl/process_oral_image', 
        data: formData,
        options: Options(
          headers: {
            'Content-Type': 'multipart/form-data',
          }
        )
      );
      
      return response.data;
    } on DioException catch (e) {
      print('Upload error: ${e.message}');
      throw Exception('Failed to upload image');
    }
  }
}