import 'package:flutter/material.dart';
import 'package:posthog_flutter/posthog.dart';
import 'config.dart';

void main() {
  Posthog().init(Config.posthogApiKey, host: Config.posthogHost);
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ETF Tracker',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(),
    );
  }
}
