import 'package:flutter/material.dart';
import 'screens/camera_screen.dart';

void main() {
  runApp(OralHealthAnalyzerApp());
}

class OralHealthAnalyzerApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Oral Health Analyzer',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: CameraScreen(),
    );
  }
}