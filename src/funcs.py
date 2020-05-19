import os

def get_from_file(file='frases.txt'):    
    while True:
        if os.path.isfile(file) and str(file).endswith('.txt'):            
            with open(file, 'r') as f:                
                phrases = [line.strip() for line in f.read().split('\n') if line.strip() != '']        
                return phrases  
        else:
            print(f'\n\n"{file}" não é um arquivo ou um path de arquivo válido.')
            file = input('\nInsira um arquivo existente no mesmo path da VENV ou insira um path de arquivo válido: ')
