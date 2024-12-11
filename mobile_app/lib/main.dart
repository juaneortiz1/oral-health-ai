import 'package:flutter/material.dart';
import 'screens/camera_screen.dart';

void main() {
  runApp(OralHealthApp());
}

class OralHealthApp extends StatelessWidget {
  const OralHealthApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Salud Oral IA',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: CameraScreen(),
    );
  }
}