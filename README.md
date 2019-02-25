# Progetto per il corso di linguaggi dinamici.

Sedoni Enrico. Matr: 108801


## Nome progetto: 

	Lempel Ziv Welch Compressor (LzwCompressor)

## Descrizione:

	semplice compressore lossless (senza perdita di dati) che utilizza 
	l'algoritmo ideato da Lempel, Ziv e Welch.

## Requisiti di sistema:
	- Linux
	- python3

## Procedura di installazione:

	- aprire un terminale all'interno della directory
	- digitare i seguenti comandi:
		- chmod u+x setup.py
		- sudo ./setup.py install

NB: l'installazione richiede i permessi di amministratore

## Come si usa l'applicazione:

	compressione:
		compress.py [ -v ] [ -r ] [ -h ] [file ...]

		-v : modalità verbose
   		-r : modalità di operamento ricorsiva (per directory)
    		-h : help sull'utilizzo del comando

	decompressione:
		uncompress.py [-r] [ -h ] [file ...]
		
		-r : modalità di operamento ricorsiva (per directory)
   		-h : help sull'utilizzo del comando
		


