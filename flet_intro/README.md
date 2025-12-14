pip install flet

flet run main.py
flet run --web main.py
flet build windows main.py


# build apk

### run initial build to install jdk and android sdk
flet build apk main.py

### install missing sdk components
export JAVA_HOME=~/java/<version>
cd ~/Android/sdk/cmdline-tools/12.0/bin
./sdkmanager.bat "build-tools;34.0.0"
./sdkmanager.bat "platforms;android-35"
./sdkmanager.bat "platform-tools"

### go back to flet project and run build
flet build apk main.py
