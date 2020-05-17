from functions import *

frases = get_from_file()    #falta verificar enviando um path que o arquivo nao é em ingles
send_to_file(frases, translate_phrases(frases))

#TODO: CRIAR teste para isso abaixo e determinar se essa será a melhor forma para chamar a função
'''
if len(frases) > 0:
    send_to_file(frases, translate_phrases(frases))


get_from_file pega as lista de strings do arquivo tratada -> essa lista é enviada para send_to_file -> dentro de send_to_file, a função translate é responsável por verificar o tipo de entrada (se é lista e o len > 0) ...?
'''