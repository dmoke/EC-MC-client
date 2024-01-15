#!/bin/bash
cd "$(dirname "$0")"
osascript -e 'tell application "Terminal" to do script "java -jar launcher.jar"'

# Sleep for a short duration to allow the Java application to start
sleep 1

# Close the terminal window
osascript -e 'tell application "Terminal" to close (every window whose custom title is "Java -jar launcher.jar")'
