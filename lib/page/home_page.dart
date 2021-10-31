import 'package:clipboard/clipboard.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart';
import 'package:speech_to_text_example/api/speech_api.dart';
import 'package:speech_to_text_example/main.dart';
import 'package:speech_to_text_example/widget/substring_highlighted.dart';
import 'package:http/http.dart' as http;

import '../utils.dart';
import 'globals.dart';

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {

  Future<String> getData(String addy, String mp3File) async {
    http.Response response = await http.get(
      Uri.parse(Uri.encodeFull(APIaddress + "/get")),
      headers: {
        "Accept": "application/string"
      }
    );

    print(response.body);
  }
  Future<http.Response> postData(String text) {
    return http.post(
      Uri.parse(Uri.encodeFull(APIaddress + "/post")),
      headers: <String, String>{
        "Content-Type": "application/string"
      },
      body: <String>{text},
    );
  }


  String text = 'Press the button and start speaking';
  bool isListening = false;
  String addresss, finalDisp;

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(
          title: Text(MyApp.title),
          centerTitle: true,
        ),
        body: SingleChildScrollView(
          reverse: true,
          padding: const EdgeInsets.all(30).copyWith(bottom: 150),
          child: SubstringHighlight(
            text: text,
            terms: Command.all,
            textStyle: TextStyle(
              fontSize: 32.0,
              color: Colors.black,
              fontWeight: FontWeight.w400,
            ),
            textStyleHighlight: TextStyle(
              fontSize: 32.0,
              color: Colors.red,
              fontWeight: FontWeight.w400,
            ),
          ),
        ),
        floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
        floatingActionButton: FloatingActionButton(
            child: Icon(isListening ? Icons.mic : Icons.mic_none, size: 36),
            onPressed: () {
              toggleRecording();
              addrezz = postData("");
              addresss = addrezz.toString();
            },
          backgroundColor: Colors.black,
          ),
      );

  Future toggleRecording() => SpeechApi.toggleRecording(
        onResult: (text) => setState(() => {postData(addresss + "," + text), this.text = text}),
        onListening: (isListening) {
          setState(() => this.isListening = isListening);

          if (!isListening) {
            Future.delayed(Duration(seconds: 1), () {
              finalDisp = getData(addresss,addresss).toString();
            });
          }
        },
      );
}
