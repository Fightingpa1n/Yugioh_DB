:: Init Script (setup docker db and python server)
@echo off

echo Installing required Python packages...
pip install -r init/requirements.txt

:: run python init script
echo running python init script (because bat files are fricking awful to make complex stuff with)
python init/init.py

echo Setup complete. You can now run the app using run.bat
