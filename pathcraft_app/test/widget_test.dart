import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:pathcraft_app/main.dart';

void main() {
  testWidgets('App starts and displays welcome message', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const PathCraftApp());

    // Verify that the welcome message is displayed.
    expect(find.text('Welcome to PathCraft!'), findsOneWidget);
  });
}
