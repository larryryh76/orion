@echo off
echo Installing Flutter...
git clone https://github.com/flutter/flutter.git -b stable
set PATH=%PATH%;%cd%\flutter\bin

echo Getting dependencies...
flutter pub get

echo Building APK...
flutter build apk

echo APK built at: build\app\outputs\flutter-apk\app-release.apk
pause