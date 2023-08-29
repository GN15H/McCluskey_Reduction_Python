from math import log, ceil
from row import Row


class Table:
    def __init__(self,minterms,implicants) -> None:
        self._minterms=minterms
        self._minterms_dict= self.minterms_dict(minterms)
        self._implicants=implicants
        self._table=[] #contiene una lista de tipo Row
        self.create_table()
        # print("Tabla creada")
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

    def get_fattest_weight(self):
        weights=list()
        for row in self._table:
            if not row.get_is_implicant() and  not row.get_is_discarded():
                weights.append(row.get_weight())
        result= max(weights) if weights.count(max(weights)) == 1 else -1 
        # print(result)
        return result

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
                if column not in first_implicants:
                    first_implicants.append(column)
                minterms_used.append(minterm)
        # print("MINTERMINOS COBIJADOS :",minterms_used)
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
                row.set_at(index,0)
        self.show()
        self.show_checked_columns()
    #RECORRE LA COLUMNA CORRESPONDIENTE AL 1 DEL PRIMER IMPLICANTE

    def search_smallest_row(self):
        smallest=self.get_smallest_weight()
        for index, row in enumerate(self._table):
            if not row.get_is_implicant() and  not row.get_is_discarded():
                if row.get_weight() == smallest:
                    # print("FILA MAS PEQUEÑA", index)
                    self.discard_smallest_row(row)
    #BUSCA FILAS QUE TENGAN EL MENOR PESO Y LLAMA self.discard_smallest_row()

    def discard_smallest_row(self,row):
        weight=row.get_weight()
        for index,item in enumerate(row.get_row()):
            if item == 1:
                if self.search_coincidences_smallest_row(row.get_implicants(), weight, row.get_reductions(), index):
                    weight-=1

        if weight == 0:
            row.is_discarded()
    #EN LAS FILAS DE MENOR PESO BUSCA LOS UNOS
    
    def search_fattest_row(self):
        biggest=self.get_fattest_weight()
        if(biggest != -1):
            for index, row in enumerate(self._table):
                if not row.get_is_implicant() and  not row.get_is_discarded():
                    if row.get_weight() == biggest:
                        # print("FILA MAS GRANDE", index)
                        row.is_implicant()
    #BUSCA LA FILA CON MAYOR PASO Y LA ELIGE COMO IMPLICANTE

    def traverse_columns(self):
        flag = True
        for index, (minterm, value) in enumerate(self._minterms_dict.items()):
            if not value and not self.is_finished():
                if flag:
                    self.traverse_columns_implicants(index, minterm, value, flag)
    #RECORRE LAS COLUMNAS QUE AUN NO HAN SIDO COBIJADAS

    def traverse_columns_implicants(self,index,  minterm, value, flag):
        column_implicants=list()
        for row_index, row in enumerate(self._table):
            if row.get_at(index) and not row.get_is_discarded() and not row.get_is_implicant():
                column_implicants.append(row)
        #print("MINTERMINO",minterm ,"FILAS IMPLICANTES",column_implicants)
        if len(column_implicants) != 0:
            flag =  self.compare_rows_discarded_reductions(column_implicants)  
    #CREA UNA LISTA DE LAS FUNCIONES QUE COBIJAN CIERTA COLUMNA

    def compare_rows_discarded_reductions(self, column_implicants):
        discarded_reductions=list()
        for index, row in enumerate(column_implicants):
            self.get_discarded_weights(discarded_reductions, row)

        flag = True
        if all(reductions == discarded_reductions[0] for reductions in discarded_reductions):
            flag = False

        #print("AVISOOOO MINTERMINO INDICE", index)
        minimum_reductions=min(discarded_reductions)
        # print("EL IMPLICANTE ES ", column_implicants[discarded_reductions.index(minimum_reductions)].get_implicants())
        column_implicants[discarded_reductions.index(minimum_reductions)].is_implicant()
        self.propagate_implicants_row(column_implicants[discarded_reductions.index(minimum_reductions)])

        for index, row in enumerate(column_implicants):
            if index != discarded_reductions.index(minimum_reductions):
                row.is_discarded()
        return flag
    #RECORRE LOS IMPLICANTES QUE COBIJAN CIERTA COLUMNA

    def get_discarded_weights(self, discarded_reductions, row):
        total=0
        for index, item in enumerate(row.get_row()):
            if item:
                total+=self.sum_discarded_weights(total, index, row)
        discarded_reductions.append(total)
        # print("REDUCCIONES TOTALES POR LA FILA",row.get_implicants(), total)
    #REVISA LOS 1'S DE LA FILA IMPLICANTE PARA VER QUE OTRAS FILAS COMPARTEN ESE UNO

    def sum_discarded_weights(self, total, index, passed_row):
        aux_total=0
        for row in self._table:
            if row.get_at(index) and row.get_row() != passed_row.get_row() and not row.get_is_implicant() and not row.get_is_discarded():
                aux_total+=row.get_reductions()
        return aux_total
    #SUMA EL TOTAL DE DESCARTES QUE HARÍA LA FILA IMPLICANTE

    def search_coincidences_smallest_row(self, implicants, weight, reductions, index):
        coincidence=False
        for row in self._table:
            if row.get_implicants() != implicants and row.get_at(index) == 1  and weight<row.get_weight():
                coincidence=True
        return coincidence
    #BUSCA LAS COINCIDENCIAS DE UNOS EN UNA MISMA COLUMNA

    def discard_duplicates(self):
        for index,row in enumerate(self._table):
            if not row.get_is_implicant() and not row.get_is_discarded():
                self.search_duplicates(row.get_row(), row.get_weight(), index)
    #REVISA LAS FILAS PARA ENCONTRAR SUS DUPLICADOS

    def search_duplicates(self, passed_row, passed_row_weight, index_1):
        for index,row in enumerate(self._table):
            if not row.get_is_implicant() and not row.get_is_discarded() and index_1 != index:
                if row.get_row() == passed_row and row.get_weight()<=passed_row_weight:
                    row.is_discarded()
    #MARCA COMO DESCARTADOS A LOS DUPLICADOS DE UNA FILA          

    def discard_implicants(self):
        for row in self._table:
            if row.get_weight()==0 and not row.get_is_implicant():
                row.is_discarded()
    #DESCARTA FILAS CON CERO PESO Y QUE NO SON IMPLICANTES

    def is_finished(self):
        is_finished=True
        left_columns=list()
        for key, value in self._minterms_dict.items():
            if(value != True):
                is_finished=False
                left_columns.append(key)

        if is_finished:
            print("FINISHED---------")
            self.show()
            self.show_true_implicants()
        return is_finished
    #REVISA SI YA TODAS LAS COLUMNAS FUERON COBIJADAS

#---------------------------------

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
            print(row.get_row(), row.get_weight(), row.get_reductions(), "IMPLICANTE" if row.get_is_implicant() else ("DESCARTADO" if row.get_is_discarded() else " "))
    #MOSTRAR TABLA

    def solve(self):
        self.propagate_implicants(self.get_first_implicants())
        while not self.is_finished():
            self.search_smallest_row()
            print()
            self.show()
            self.show_checked_columns()
            if not self.is_finished():
                self.discard_duplicates()
                print()
                self.show()
                self.show_checked_columns()
                if not self.is_finished():
                    self.get_fattest_weight()
                    print()
                    self.show()
                    self.show_checked_columns()
                    if not self.is_finished():
                        self.traverse_columns()
                        print()
                        self.show()
                        self.show_checked_columns()
