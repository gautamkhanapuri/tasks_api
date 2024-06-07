username="gautamkhanapuri"
cd code
export PYTHONPATH=`pwd`
cd ..
python3 -m venv api_env
source api_env/bin/activate
pip install -U pip
pip install -r requirements.txt
PORTNO=8000
