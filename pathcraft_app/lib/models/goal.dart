import 'package:flutter/foundation.dart';

// Note: These models are simplified for the initial UI implementation.
// They will be expanded as more features are added.

class Task {
  final String id;
  final String description;
  final String status;

  Task({
    required this.id,
    required this.description,
    required this.status,
  });

  factory Task.fromJson(Map<String, dynamic> json) {
    return Task(
      id: json['id'],
      description: json['description'],
      status: json['status'],
    );
  }
}

class SubGoal {
  final String id;
  final String description;
  final List<Task> tasks;

  SubGoal({
    required this.id,
    required this.description,
    required this.tasks,
  });

  factory SubGoal.fromJson(Map<String, dynamic> json) {
    var taskList = json['tasks'] as List? ?? [];
    List<Task> tasks = taskList.map((i) => Task.fromJson(i)).toList();

    return SubGoal(
      id: json['id'],
      description: json['description'],
      tasks: tasks,
    );
  }
}

class Goal {
  final String id;
  final String title;
  final DateTime targetDate;
  final List<SubGoal> subGoals;

  Goal({
    required this.id,
    required this.title,
    required this.targetDate,
    required this.subGoals,
  });

  factory Goal.fromJson(Map<String, dynamic> json) {
    var subGoalList = json['sub_goals'] as List? ?? [];
    List<SubGoal> subGoals =
        subGoalList.map((i) => SubGoal.fromJson(i)).toList();

    return Goal(
      id: json['id'],
      title: json['title'],
      targetDate: DateTime.parse(json['target_date']),
      subGoals: subGoals,
    );
  }
}
