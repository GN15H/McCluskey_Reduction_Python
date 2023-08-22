from math import log, ceil

class Minterms:
    def __init__(self, minterms_list : list) -> None:
        minterms_list.sort()
        self._m_list = minterms_list
        self._n_variables = self.set_number_of_variables()

        self._m_dict = dict()
        self.set_m_dict()

    def get_m_list(self):
        return self._m_list

    def get_n_variables(self):
        return self._n_variables

    def get_m_dict(self):
        return self._m_dict

    def set_number_of_variables(self):
        return ceil(log(self._m_list[-1], 2))

    def set_m_dict(self):
        for i in range(self._n_variables):
            self._m_dict[i] = []

        for item in self._m_list:
            self._m_dict[bin(item)[2:].count('1')].append(item)
