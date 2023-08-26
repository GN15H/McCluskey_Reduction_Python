from math import log, ceil

class Row:
    def __init__(self,minterms, implicants) -> None:
        self._is_discarded=False
        self._is_implicant=False
        self._implicants=implicants
        self._minterms=minterms
        self._weight=len(implicants)
        self._reductions= int(log(len(implicants),2))
        self._row=list()
        self.create_row()

    def create_row(self):
        for minterm in self._minterms:
            self._row.append(1 if minterm in self._implicants else 0)
    
    def is_implicant(self):
        self._is_implicant=True
    
    def is_discarded(self):
        self._is_discarded=True

    def get_is_implicant(self):
        return self._is_implicant
    
    def get_is_discarded(self):
        return self._is_discarded

    def reduce_weight(self,i):
        self._weight-=1
        #print("Reducción a la fila",i)
    
    def get_weight(self):
        return self._weight
    
    def get_reductions(self):
        return self._reductions

    def get_implicants(self):
        return self._implicants
    
    def get_at(self,position):
        return self._row[position]
    
    def set_at(self,position,value):
        self._row[position] = value
    
    def get_row(self):
        return self._row