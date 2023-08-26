from math import log, ceil
from row import Row


class Table:
    def __init__(self,minterms,implicants) -> None:
        self._minterms=minterms
        self._minterms_dict= self.minterms_dict(minterms)
        self._implicants=implicants
        self._table=[] #contiene una lista de tipo Row
        self.create_table()
        print("Tabla creada")
    #CONSTRUCTOR


    def minterms_dict(self, minterms): #crea un diccionario que contiene de llaves los minterminos
        aux_dict=dict()
        for minterm in minterms:
            aux_dict[minterm]=False
        return aux_dict
    #CREAR DICCIONARIO DE MINTERMINOS

    
    def create_table(self):
        for implicant in self._implicants:
            self._table.append(Row(self._minterms_dict.keys(),implicant)) #añade una Row
    #CREAR TABLA DE COMPROBACIÓN

    def get_smallest_weight(self):
        weights=list()
        for row in self._table:
            if not row.get_is_implicant() and  not row.get_is_discarded():
                weights.append(row.get_weight())
        return min(weights)
    #RETORNA EL MENOR PESO ENCONTRADO


    def get_first_implicants(self):
        first_implicants=list()
        minterms_used=list()
        amount_of_x=0
        column=list()
        for index, (minterm, value) in enumerate(self._minterms_dict.items()):
            amount_of_x=0
            for row in self._table:
                if(row.get_at(index)):
                    column=row.get_implicants()
                    amount_of_x+=1
            if(amount_of_x==1):
                first_implicants.append(column)
                minterms_used.append(minterm)
        print("MINTERMINOS COBIJADOS :",minterms_used)
        return first_implicants
    #RETORNA LOS PRIMEROS IMPLICANTES


    def propagate_implicants(self, first_implicants):
        for row in self._table:
            if (row.get_implicants() in first_implicants):
                self.propagate_implicants_row(row)
                row.is_implicant()
    #CICLA A LOS PRIMEROS IMPLICANTES
    
    def propagate_implicants_row(self,row):
        for index, item in enumerate(row.get_row()):
            if(item):
                self._minterms_dict[self._minterms[index]]=True  #COBIJA LA COLUMNA
                self.propagate_implicants_columns(index)
    #RECORRE LA FILA DEL PRIMER IMPLICANTE
    
    def propagate_implicants_columns(self, index):
        for i, row in enumerate(self._table):
            if row.get_at(index)==1:
                row.reduce_weight(i)
                row.set_at(index,2)
    #RECORRE LA COLUMNA CORRESPONDIENTE AL 1 DEL PRIMER IMPLICANTE




    def search_smallest_row(self):
        smallest=self.get_smallest_weight()
        for index, row in enumerate(self._table):
            if not row.get_is_implicant() or  not row.get_is_discarded():
                if row.get_weight() == smallest:
                    print("FILA MAS PEQUEÑA", index)
                    self.discard_smallest_row(row)
    #BUSCA FILAS QUE TENGAN EL MENOR PESO Y LLAMA self.discard_smallest_row()


    def discard_smallest_row(self,row):
        weight=row.get_weight()
        for index,item in enumerate(row.get_row()):
            if item == 1:
                if self.search_coincidences(row.get_implicants(), weight, row.get_reductions(), index):
                    weight-=1

        if weight == 0:
            row.is_discarded()

    
    def search_coincidences(self, implicants, weight, reductions, index):
        coincidence=False
        for row in self._table:
            if row.get_implicants() != implicants and row.get_at(index) == 1  and weight<row.get_weight():
                coincidence=True
        return coincidence
        

                





    def discard_implicants(self):
        for row in self._table:
            if row.get_weight()==0 and not row.get_is_implicant():
                row.is_discarded()
    #DESCARTA FILAS CON CERO PESO Y QUE NO SON IMPLICANTES


    def show_true_implicants(self):
        for row in self._table:
            if row.get_is_implicant():
                print(row.get_implicants())

    def show_checked_columns(self):
        checked=list()
        for keys,values in self._minterms_dict.items():
            if(values):
                checked.append(keys)
        print("COLUMNAS TOTALES COBIJADAS",checked)



    





    def show(self):
        print(self._minterms)
        for row in self._table:
            print(row.get_row(), row.get_weight(), "IMPLICANTE" if row.get_is_implicant() else ("DESCARTADO" if row.get_is_discarded() else " "))
    #MOSTRAR TABLA