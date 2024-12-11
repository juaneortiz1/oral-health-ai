import 'package:flutter/material.dart';

class ResultsScreen extends StatelessWidget {
  final Map<String, dynamic> analysisResult;

  const ResultsScreen({Key? key, required this.analysisResult}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final result = analysisResult['result'];

    return Scaffold(
      appBar: AppBar(
        title: Text('Oral Health Analysis'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Analysis Results',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            SizedBox(height: 20),
            Text(
              result['message'],
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: _getColorForCondition(result['top_class']),
              ),
            ),
            SizedBox(height: 20),
            _buildPredictionDetails(result['predictions']),
          ],
        ),
      ),
    );
  }

  Widget _buildPredictionDetails(Map<String, dynamic> predictions) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: predictions.entries.map((entry) {
        return Padding(
          padding: const EdgeInsets.symmetric(vertical: 4.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(entry.key),
              Text('${(entry.value * 100).toStringAsFixed(2)}%'),
            ],
          ),
        );
      }).toList(),
    );
  }

  Color _getColorForCondition(String condition) {
    switch (condition) {
      case 'Caries':
        return Colors.red;
      case 'Gingivitis':
        return Colors.orange;
      case 'Hipodontia':
        return Colors.yellow;
      case 'Sarro':
        return Colors.blue;
      default:
        return Colors.green;
    }
  }
}