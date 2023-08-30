from math import log, ceil

class Minterms:
    def __init__(self, minterms_list : list) -> None:
        minterms_list.sort()
        self._m_list = minterms_list
        self._n_variables = self.set_number_of_variables()

        self._m_dict = dict()
        self.set_m_dict()
        self._new_dict = {}
        self.implicants = []

    def get_m_list(self):
        return self._m_list

    def get_number_variables(self):
        return self._n_variables

    def get_m_dict(self):
        return self._m_dict

    def get_implicants(self):
        return self.implicants

    def set_number_of_variables(self):
        return ceil(log(self._m_list[-1], 2))

    def set_m_dict(self):
        for i in range(self._n_variables+1):
            self._m_dict[i] = []
        for item in self._m_list:
            self._m_dict[bin(item).count('1')].append([item])

    def initialize_new_dict(self):
       for i in range(self._n_variables+1):
            self._new_dict[i] = []

    def remove_duplicates(self, lst):
        seen = set()
        result = []
        
        for inner_list in lst:
            inner_tuple = tuple(inner_list)
            if inner_tuple not in seen:
                seen.add(inner_tuple)
                result.append(inner_list)
        
        return result

    def remove_duplicates_1(self, list):
        result=list
        aux_list_1=[]
        for sublist in list:
            aux_list_1= sorted(sublist)
            for index, sublist_2 in enumerate(list):
                if sublist != sublist_2:
                    if (aux_list_1 == sorted(sublist_2)):
                        del result[index]
        return result
        

    def list_dashes(self, lst):
        dashes=[]
        for i in range(int(log(len(lst),2))):
            dashes.append(int(log(lst[pow(2,i)]-lst[0],2)))
        return sorted(dashes)
    
    def compare_list_dashes(self,lst1,lst2):
        flag=False
        if self.list_dashes(lst1) == self.list_dashes(lst2):
            flag=True
        return flag


    def pair_data(self):
        unused_terms = []
        initial_length = 1
        while len(unused_terms) != initial_length:

            self.initialize_new_dict()
            unused_terms = [sublist for sublist_list in self._m_dict.values() for sublist in sublist_list] #contiene todos los elementos del emparejamiento
            initial_length = len(unused_terms)


            for i in range(self._n_variables): #al final del ciclo se habra llenada _new_dict con las parejas nuevas y quitado de unused_terms aquellos terminos emparejados
                self.pair_minterms(i, unused_terms)
            self._m_dict = dict(self._new_dict) #se le pasa la info de _new_dict a _m_dict
            self.implicants += unused_terms   #variable que contiene los implicantes encontrados a lo largo de todo el proceso

        self.implicants = self.remove_duplicates_1(self.implicants)
    #FIN FUNCIÓN pair_data
    

    def pair_minterms(self, i, unused_terms):
        first_pairs=self._m_dict[i]
        for first_pair in first_pairs:
            self.pair_minterm(first_pair,i, unused_terms)
        self.remove_duplicates_1(self._m_dict[i])
    
    def pair_minterm(self, first_pair,i, unused_terms):
        second_pairs=self._m_dict[i+1]
        for second_pair in second_pairs:
            is_valid = False

            if first_pair[0]<second_pair[0]:
                if ceil(log(second_pair[0]-first_pair[0],2)) == log(second_pair[0]-first_pair[0],2) and self.compare_list_dashes(first_pair,second_pair):
                    is_valid = True

            if is_valid:
                self._new_dict[i].append(first_pair+second_pair)  #añadir a _new_dict en la llave i y appendear los valores conjuntos de first_pair y second_pair
                if first_pair in unused_terms:
                    unused_terms.remove(first_pair)  #remover de unused_terms en caso de ser valido 
                if second_pair in unused_terms: 
                    unused_terms.remove(second_pair)
