#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from LzwCompressor.LzwCompressor import LzwCompressor as lzw
'''
Script per la compressione di file che viene richiamato dalla riga di comando.
Permette l'utilizzo di diverse opzioni:
    -v : modalità verbose
    -r : modalità di operamento ricorsiva (per directory)
    -h : help sull'utilizzo del comando
    opzione aggiuntiva per modalità sviluppatore:
        --debug: comprime anche i file per i quali la compressione non è necessaria
                 siccome ne va ad aumentare la dimensione

    SYNOPSIS:
    compress.py [ -v ] [ -r ] [ -h ] [file ...]

@author: Sedoni Enrico

'''

def compress_r(file_name, compressor, flag_v):
    ''' 
        Funzione per la compressione dei file interni alle 
        directory, funziona in maniera ricorsiva. 
        Se il file è una directory ci entra dentro e prova a comprimere
        i file al suo interno, se anch'essi sono directory ripete l'operazione
        fino a comprimere tutti i file.
    '''
    if os.path.isfile(file_name):
        #se ho compresso con successso rimuovo i file non compressi
        print("comprimo: ",file_name, "...")
        if compressor.compress(file_name, flag_v):
            if not file_name.endswith('.Z'):
                os.remove(file_name)
    else: 
        files = os.listdir(file_name)
        os.chdir(file_name)
        for f in files:
            compress_r(f, compressor, flag_v)
        os.chdir('..')


if __name__ == "__main__":
    arguments = sys.argv
    flag_v = False
    flag_r = False
    flag_h = False
    flag_debug = False
    arguments.pop(0)
    count = 0
    for arg in arguments:  
        if arg == '-v':
            flag_v = True 
            count += 1         
        elif arg == '-r':
            flag_r = True
            count += 1
        elif arg == '-h':
            flag_h = True
            count += 1
        elif arg == '--debug':
            flag_debug = True
            count += 1
            
    compressor = lzw(debug = flag_debug)       
    for i in range(count):
        arguments.pop(0)

    if flag_h == True:
        print("SYNOPSIS:")
        print("compress.py [ -v ] [ -r ] [ -h ] [file ...]")
    elif flag_r == True:
        origin_path = os.getcwd()
        for f in arguments:
            os.chdir(origin_path)
            compress_r(f, compressor, flag_v)
    else: 
        
        if compressor.compress(arguments[0], flag_v) :
            if not arguments[0].endswith('.Z'):
                os.remove(arguments[0])
            

        


    
