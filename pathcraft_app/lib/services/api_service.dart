import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/goal.dart';

class ApiService {
  // For development, ensure your backend is running and accessible at this URL.
  // For Android emulator, this is typically 10.0.2.2.
  final String _baseUrl = "http://127.0.0.1:8000";
  final http.Client _client = http.Client();

  Future<List<Goal>> getGoals() async {
    try {
      final response = await _client.get(Uri.parse('$_baseUrl/goals/'));

      if (response.statusCode == 200) {
        final List<dynamic> body = jsonDecode(response.body);
        final List<Goal> goals =
            body.map((dynamic item) => Goal.fromJson(item)).toList();
        return goals;
      } else {
        // Consider more specific error handling based on status code
        throw Exception('Failed to load goals from the API');
      }
    } catch (e) {
      // Handle network errors or other exceptions
      throw Exception('Failed to connect to the API: $e');
    }
  }

  // Future<Goal> createGoal(GoalCreate data) async { ... }
  // Future<void> deleteGoal(String id) async { ... }
  // etc.
}
