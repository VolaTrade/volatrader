echo "Running DataBase Test Script"
python3 DataBaseTestScript.py
cd ..
pwd
echo "Running BackTest Test Script"
python3 -m unittest tests/BackTesterOutputTest.py