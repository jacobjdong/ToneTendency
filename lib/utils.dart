import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import '../page/globals.dart';

class Command {
  static final all = [email, browser1, browser2];

  static const email = 'write email';
  static const browser1 = 'open';
  static const browser2 = 'go to';
}

class Utils {

  static void scanText(String rawText) {
    final text = rawText.toLowerCase();
  }
}