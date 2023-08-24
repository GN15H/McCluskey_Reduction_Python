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

    def pair_data(self):
        unused_terms = []
        initial_length = 1
        while len(unused_terms) != initial_length:
            self.initialize_new_dict()
            unused_terms = [sublist for sublist_list in self._m_dict.values() for sublist in sublist_list]
            initial_length = len(unused_terms)
            for i in range(self._n_variables):
                self.pair_minterms(i, unused_terms)
            self._m_dict = dict(self._new_dict)
            self.implicants += unused_terms

        for item in self.implicants:
            item.sort()

        self.implicants = self.remove_duplicates(self.implicants)

    def pair_minterms(self, i, unused_terms):
        first_pairs=self._m_dict[i]
        for first_pair in first_pairs:
            self.pair_minterm(first_pair,i, unused_terms)
    
    def pair_minterm(self, first_pair,i, unused_terms):
        second_pairs=self._m_dict[i+1]
        for second_pair in second_pairs:
            is_valid = False
            if sum(first_pair)<sum(second_pair) and first_pair[0]<second_pair[0] and first_pair[int(log(len(second_pair), 2))]<second_pair[int(log(len(second_pair), 2))]:
                if log(second_pair[0]-first_pair[0], 2) == log(second_pair[int(log(len(second_pair), 2))] - first_pair[int(log(len(second_pair), 2))], 2):
                    is_valid = True

            if is_valid:
                self._new_dict[i].append(first_pair+second_pair)
                if first_pair in unused_terms:
                    unused_terms.remove(first_pair)
                if second_pair in unused_terms:    
                    unused_terms.remove(second_pair)
