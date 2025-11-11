apt-get update && apt-get install -y libjpeg-dev zlib1g-dev
sed -i 's/Pillow==8.0.0/Pillow>=8.0.0/' requirements.txt
pip install -r requirements.txt
pip install --upgrade setuptools