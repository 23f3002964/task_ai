import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:pathcraft_app/providers/goal_provider.dart';
import 'package:pathcraft_app/screens/home_screen.dart';

void main() {
  runApp(
    ChangeNotifierProvider(
      create: (context) => GoalProvider(),
      child: const PathCraftApp(),
    ),
  );
}

class PathCraftApp extends StatelessWidget {
  const PathCraftApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'PathCraft',
      theme: ThemeData(
        useMaterial3: true,
        primarySwatch: Colors.deepPurple,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: const HomeScreen(),
    );
  }
}
