from LzwCompressor.utils import BadCompression as exc
from LzwCompressor.utils import ValueError as exc3
import os
import shutil
import stat
import math


'''
@author: Sedoni Enrico
'''
class LzwCompressor():
    '''
    Classe che implemente il compressore Lempel Ziv Welch nella sua interezza.
    Mette a disposizione la seguente interfaccia:
        compress: metodo per la compressione di un file
        uncompress: metodo per la decompressione di un file compresso

    dispone inoltre di un metodo aggiuntivo 'lg' per il calcolo del numero 
    di bit minimo necessario per scrivere il dato nel file
    '''
    def __init__(self, debug=False):
        self.input_file = []
        self.__debugMode = debug
        self.dict_initial_size = 256
        
    def __lg(self,x):
        '''
        Metodo per il calcolo del numero di bit minimo necessario a rappresentare il valore x
        nel file compresso, in questo modo si aumenta ulteriormente la capacità di compressione.
        Es: valore 260 -> 9 bit
        '''
        if x == 0:
            return 1
        else: 
            return (math.floor(math.log(x, 2))+1)

    def compress(self, file_path, flag_v = False):
        '''
        Metodo per la compressione di un file, prende in input il path al file
        e il flag verbose (flag_v), fa uso di un dizionario che mappa uno o più
        caratteri ai codici rispettivi, si basa sull'algoritmo lempel ziv welch
        di compressione. Il file viene scritto in byte per risparmiare ulteriormente
        spazio e anche perchè il file compresso non deve venir letto dall'utente
        '''
        #salvo la dimensione del file originale, che servirà in un momento sucessivo
        old_size = os.path.getsize(file_path)

        counter = self.dict_initial_size 
        #vado a creare il dizionario iniziale del seguente tipo: caratteri -> codice
        dictionary = {chr(i): i for i in range(self.dict_initial_size)}
        dictionary['END'] = self.dict_initial_size
        self.input_file.clear()
        #provo prima ad aprirlo come file testuale, se genera eccezione vuol dire che
        #è un altro tipo di file e lo apro in modalità binaria
        try:
            with open(file_path, 'r', 'latin-1') as f:
                data = f.read()
            for i in data:
                self.input_file.append(i)
        except:
            with open(file_path, 'rb') as f:
                data = f.read()
            for i in data:
                #nel caso il file sia aperto in modalità binaria, di ogni byte letto ne
                # prendo la rappresentazione carattere, che serve per comodità all'algoritmo
                self.input_file.append(chr(i))
            
   
        #appendo alla fine del nome l'estenzione '.Z'
        compress_file_name = file_path+'.Z'
        #apro il file in modalità binaria
        fout = open(compress_file_name, "wb")
        #copio i permessi del file in quello nuovo, si utilizza il modulo 
        #python shutil per copiare la maschera dei permessi e il modulo stat per copiare
        #nel file nuovo, utente e gruppo proprietari del file
        shutil.copystat(file_path, compress_file_name)
        file_stat = os.stat(file_path)
        owner = file_stat[stat.ST_UID]
        group = file_stat[stat.ST_GID]
        os.chown(compress_file_name, owner, group)
        #Algoritmo principale per la compressione del file. Ad ogni ciclo vedo se il carattere o la sequenza
        #di caratteri è già presente nel dizionario oppure no. Se è presente nel dizionario vado a prendere 
        #il carattere sucessivo da codificare e lo appendo alla sequenza, altrimenti vado ad aggiungere la nuova 
        #sequenza al dizionario e scrivo il codice nel file compresso relativo alla sequenza precedente di cui possiedo il codice
        s = ''
        try:
            for c in self.input_file:
                sc = s+c
                if sc in dictionary:
                    s = sc
                else: 
                    p = dictionary[s]
                    counter += 1
                    dictionary[sc] = counter
                    nbytes = math.ceil(self.__lg(counter)/8)
                    fout.write(p.to_bytes(nbytes, 'big'))   
                    s = c
                    sc = ''
            #se l'ultima combinazione di caratteri è una già nel dizionario devo scriverla sul file
            if sc != '':
                p = dictionary[sc]
                fout.write(p.to_bytes(nbytes, 'big')) 
        except:
            fout.close()
            #la compressione non è avvenuta con successo, rimuovo il file compresso che si trova in una
            #situazione inconsistente
            os.remove(compress_file_name)
            raise exc3.ValueError
        end = dictionary['END']
        nbytes = math.ceil(self.__lg(counter)/8)
        fout.write(end.to_bytes(nbytes, 'big'))
        fout.close()
        if not self.__debugMode: 
            #se la dimensione del file compresso è maggiore di quella del file originale
            #devo rimuovere il file compresso ed informare l'utente, si utilizza il modulo built in di python "os"
            #per recuperare la dimensione dei file
            new_size = os.path.getsize(compress_file_name)
            if new_size > old_size:
                if flag_v == True:
                    print("Non è stata effettuata compressione perchè il file compresso "\
                        "è più grande di quello non compresso. File: ", file_path)
               
                os.remove(compress_file_name)
                return False
            #se la dimensione del file compresso è minore di quella del file originale
            #mi calcolo lo spazio risparmiato in byte e in percentuale
            if flag_v == True:
                diff = old_size - new_size
                perc = (100*new_size)/old_size
                diff_perc = 100-perc
                print("Compressione effettuata  con successo, spazio risparmiato in byte {0}, "\
                    "in percentuale: {1} %".format(diff, round(diff_perc, 2)))

        return True

    def uncompress(self, file_path):
        '''
        Metodo per la decompressione di un file compresso ('.Z'), prende in input
        solamente il path al file. Per la decompressione utilizza un dizionario 
        del tutto simile a quello utilizzato per la compressione, ma invertito (per comodità
        dell'algoritmo), ovvero se per la compressione era: 'A' : 65, per la decompressione 
        sarà 65 : 'A'.
        Per la decompressione l'unica informazione da conoscere in partenza è la dimensione del 
        dizionario utilizzato per la compressione.
        '''
        counter = self.dict_initial_size + 1
        
        #in questo caso ho il dizionario invertito, la chiave è il codice
        dictionary = {i: chr(i) for i in range(self.dict_initial_size)}
        #salvo il carattere di end
        dictionary[self.dict_initial_size] = '\n'
        self.input_file.clear()
        
        #se è già un file decompresso non ha senso provare a decomprimere,
        #  deve essere quindi di estensione .Z per procedere
        if file_path.endswith('.Z'):
            with open(file_path, 'rb') as f:
               data = f.read()
            #recupero nome del file togliendo l'estensione '.Z'
            uncompress_file_name = file_path[0:(len(file_path)-2)]
            #apro il file in modalità scrittura binaria
            fdcomp = open(uncompress_file_name, "wb")
            #copio i permessi del file in quello nuovo, si utilizza il modulo 
            #python shutil per copiare la maschera dei permessi e il modulo stat per copiare
            #nel file nuovo, utente e gruppo proprietari del file
            shutil.copystat(file_path, uncompress_file_name)
            file_stat = os.stat(file_path)
            owner = file_stat[stat.ST_UID]
            group = file_stat[stat.ST_GID]
            os.chown(uncompress_file_name, owner, group)

            #siccome non so quanti byte sono stati utilizzati in fase di compressione per ogni codice, il
            # file in input (quello composto dai codici effettivi da decodificare) viene ricostruito man mano
            # durante l'algoritmo sulla base del valore del contatore. I primi codici certamente saranno stati scritti
            # con due byte (per le proprietà dell'algoritmo di compressione), quindi per far partire l'algoritmo
            #sarà necessario almeno inserire i primi due codici nella struttura dati 'input_file' che contiene i codici
            j = 2+math.ceil(self.__lg(counter)/8)
            self.input_file.append(int.from_bytes(data[0:2], 'big'))
            self.input_file.append(int.from_bytes(data[2: j], 'big'))
            
            val = self.input_file.pop(0)
            s = chr(val)
            fdcomp.write(val.to_bytes(1, 'big'))
            for code in self.input_file:
                #se il codice è all'interno del dizionario (e quasi certamente lo sarà
                #perchè o è presente nel dizionario iniziale o viene inserito il passo prima) la variabile
                #new_value viene inizializzata con i caratteri relativi al codice
                if code in dictionary:
                    new_value = dictionary[code]
                #caso speciale in cui incontro come secondo carattere uno già codificato 
                # es: file compresso: 65 257 ... quindi il caso in cui ho tre caratteri 
                # uguali all'inizio del file da comprimere
                elif code == counter:
                    new_value = s+s[0]
                    
                else:
                    raise exc.BadCompression
                #inserisco una nuova entry nel dizionario 
                dictionary[counter] = s+new_value[0]
                s = new_value
                counter += 1
                #scrivo nel file di output decompresso i vari byte
                for i in new_value:
                    fdcomp.write(ord(i).to_bytes(1, 'big'))
                
                #vado a leggere il prossimo dato dal file compresso e lo inserisco nell'array
                #del file di input
                k = j+ math.ceil(self.__lg(counter+1)/8)
                val = int.from_bytes(data[j: k], 'big')
                #se il codice letto è quello di end file, devo uscire dal ciclo principale
                if val == self.dict_initial_size:
                    break
                self.input_file.append(val)
                j = k    
            #scrivo il carattere di end file
            #fdcomp.write(ord(dictionary[self.dict_initial_size]).to_bytes(1,'big'))
            fdcomp.close()
            
            return True
        return False
