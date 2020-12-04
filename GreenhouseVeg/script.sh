#!/bin/bash
rm main.py my.kv
cp -R /media/psf/GoogleDrive/untitled/* ./
buildozer android debug deploy run
adb logcat | grep python
