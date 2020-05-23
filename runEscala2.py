import os, subprocess
from time import sleep

#os.chdir(r'.\venv\Scripts')
subprocess.call(r'venv\Scripts\activate.bat')
#os.chdir(r'..\..\ ')
subprocess.Popen(r'venv\Scripts\python.exe -m escala2Main')

print('Executando o AnkiBot...')


