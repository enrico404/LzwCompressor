'''
@author: Sedoni Enrico

'''

class ValueError(Exception):
    '''  
     Eccezione che viene invocata nel caso in cui il file 
     di input abbia caratteri non presenti nel dizionario iniziale
    '''
    def __init__(self, *args, **kwargs):
        return super().__init__("Value must be in range(0,255)!", **kwargs)


