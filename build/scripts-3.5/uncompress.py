#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
from LzwCompressor.LzwCompressor import LzwCompressor as lzw

'''
Script per la decompressione di file compressi (con estensione '.Z') richiamato
da riga di comando.
Permette l'utilizzo di diverse opzioni: 
    -r : modalità di operamento ricorsiva (per directory)
    -h : help sull'utilizzo del comando

    SYNOPSIS:
    uncompress.py [ -r ] [ -h ] [ file ... ]

@author: Sedoni Enrico
'''
def uncompress_r(file_name, uncompressor):
    ''' 
        Funzione per la decompressione dei file interni alle 
        directory, funziona in maniera ricorsiva. 
        Se il file è una directory ci entra dentro e prova a decomprimere
        i file al suo interno, se anch'essi sono directory ripete l'operazione
        fino a decomprimere tutti i file.
    '''
    if os.path.isfile(file_name):
        #se ho compresso con successso rimuovo i file non compressi
        if uncompressor.uncompress(file_name):
            #if not file_name.endswith('.txt'):
            os.remove(file_name)
    else: 
        files = os.listdir(file_name)
        os.chdir(file_name)
        for f in files:
            uncompress_r(f, uncompressor)
        os.chdir('..')

if __name__ == "__main__":

    arguments = sys.argv
    uncompressor = lzw()
    flag_r = False
    flag_h = False
    arguments.pop(0)
    count = 0
    for arg in arguments:  
        if arg == '-r':
            flag_r = True
            count += 1
        elif arg == '-h':
            flag_h = True
            count += 1
    for i in range(count):
        arguments.pop(0)

    if flag_h == True:
        print("SYNOPSIS:")
        print("uncompress.py [-r] [ -h ] [file ...]")
        print("DESCRIZIONE: ")
        print("Decompressore di un file compresso con il compressore Lempel-Ziv-Welch")
        print("")
        print("-r : modalità di operamento ricorsiva (per directory)")

    elif flag_r == True:
        origin_path = os.getcwd()
        for f in arguments:
            os.chdir(origin_path)
            uncompress_r(f, uncompressor)
    else: 
        if uncompressor.uncompress(arguments[0]):
            #if not arguments[0].endswith('.txt'):
            os.remove(arguments[0])
            

        


    
