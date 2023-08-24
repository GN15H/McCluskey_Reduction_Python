from math import log, ceil

class Minterms:
    def __init__(self, minterms_list : list) -> None:
        minterms_list.sort()
        self._m_list = minterms_list
        self._n_variables = self.set_number_of_variables()

        self._m_dict = dict()
        self.set_m_dict()
        self._new_dict = {}
        self.final_terms = []

    def get_m_list(self):
        return self._m_list

    def get_number_variables(self):
        return self._n_variables

    def get_m_dict(self):
        return self._m_dict

    def set_number_of_variables(self):
        return ceil(log(self._m_list[-1], 2))

    def set_m_dict(self):
        for i in range(self._n_variables+1):
            self._m_dict[i] = []
        for item in self._m_list:
            self._m_dict[bin(item).count('1')].append([item])
            # print(self._m_dict)

    def initialize_new_dict(self):
        for i in range(self._n_variables+1):
            self._new_dict[i] = []

    def pair_data(self):
        self.initialize_new_dict()
        for i in range(self._n_variables):
            self.pair_minterms(i)
        self._m_dict = self._new_dict

    def pair_minterms(self, i):
        first_pairs=self._m_dict[i]
        for first_pair in first_pairs:
            #print(i,"pair", first_pair)
            self.pair_minterm(first_pair,i)
    
    def pair_minterm(self, first_pair,i):
        second_pairs=self._m_dict[i+1]
        #print(i+1,"pairs",first_pair, ":",second_pairs)
        for second_pair in second_pairs:
            is_valid = True
            for j in range(len(first_pair)):
                if(first_pair[j]<second_pair[j]):
                    if ceil(log(second_pair[j]-first_pair[j],2)) != log(second_pair[j]-first_pair[j],2):
                        is_valid = False

            if is_valid:
                self._new_dict[i].append(first_pair+second_pair)


