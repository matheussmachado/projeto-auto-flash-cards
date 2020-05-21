import os, subprocess
from time import sleep

os.chdir(r'.\venv\Scripts')

#Parece que não necessita executar a ativação da venv
#subprocess.call('activate.bat')
os.chdir(r'..\..\ ')
subprocess.call(r'venv\Scripts\python.exe -m escala2Main')


