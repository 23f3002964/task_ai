import 'package:flutter/material.dart';
import '../models/goal.dart';
import '../services/api_service.dart';

enum NotifierState { initial, loading, loaded, error }

class GoalProvider with ChangeNotifier {
  final ApiService _apiService = ApiService();

  NotifierState _state = NotifierState.initial;
  List<Goal> _goals = [];
  String _errorMessage = '';

  NotifierState get state => _state;
  List<Goal> get goals => _goals;
  String get errorMessage => _errorMessage;

  Future<void> fetchGoals() async {
    _state = NotifierState.loading;
    notifyListeners();

    try {
      _goals = await _apiService.getGoals();
      _state = NotifierState.loaded;
    } catch (e) {
      _errorMessage = e.toString();
      _state = NotifierState.error;
    } finally {
      notifyListeners();
    }
  }
}
