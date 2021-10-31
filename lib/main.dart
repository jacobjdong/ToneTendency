import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:speech_to_text_example/page/home_page.dart';
import '../page/globals.dart' as globals;
import 'package:http/http.dart' as http;

Future main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]);

  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  static final String title = 'ToneTendency';

  @override
  Widget build(BuildContext context) => MaterialApp(
        debugShowCheckedModeBanner: false,
        title: title,
        theme: ThemeData(
            primarySwatch: Colors.purple,
          appBarTheme: AppBarTheme(
            color: const Color(0xFF151026),
          )
        ),
        home: HomePage(),
      );
}