import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/goal_provider.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  void initState() {
    super.initState();
    // Use a post-frame callback to fetch goals after the first frame is built.
    // This ensures that the context is available.
    WidgetsBinding.instance.addPostFrameCallback((_) {
      Provider.of<GoalProvider>(context, listen: false).fetchGoals();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('My Goals'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              Provider.of<GoalProvider>(context, listen: false).fetchGoals();
            },
          ),
        ],
      ),
      body: Consumer<GoalProvider>(
        builder: (context, goalProvider, child) {
          switch (goalProvider.state) {
            case NotifierState.loading:
              return const Center(child: CircularProgressIndicator());
            case NotifierState.error:
              return Center(
                child: Text(
                  'Error: ${goalProvider.errorMessage}\n\n'
                  'Is the backend server running at http://127.0.0.1:8000?',
                  textAlign: TextAlign.center,
                ),
              );
            case NotifierState.loaded:
              if (goalProvider.goals.isEmpty) {
                return const Center(
                  child: Text(
                    'No goals yet. Tap the + button to add one!',
                    textAlign: TextAlign.center,
                  ),
                );
              }
              return ListView.builder(
                itemCount: goalProvider.goals.length,
                itemBuilder: (context, index) {
                  final goal = goalProvider.goals[index];
                  return ListTile(
                    title: Text(goal.title),
                    subtitle: Text('Target: ${goal.targetDate.toLocal().toString().substring(0, 10)}'),
                    trailing: const Icon(Icons.chevron_right),
                    onTap: () {
                      // Navigate to goal details screen (to be implemented)
                    },
                  );
                },
              );
            default:
              return const Center(child: Text('Press the refresh button to load goals.'));
          }
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // Open create goal screen (to be implemented)
        },
        tooltip: 'Add Goal',
        child: const Icon(Icons.add),
      ),
    );
  }
}
