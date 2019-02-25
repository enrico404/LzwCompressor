'''
@author: Sedoni Enrico

'''

class UnsupportedEncoding(Exception):
    '''  
     Eccezione che viene invocata nel caso in cui il file 
     in input abbia un encoding non supportato dal programma
    '''
    def __init__(self, *args, **kwargs):
        return super().__init__("Encoding del file non supportato!", **kwargs)