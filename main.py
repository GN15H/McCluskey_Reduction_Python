from minterms import Minterms
from table import Table

def get_data():
    try:
        data = input("Enter minterms separated by a single blank space:\n").strip()
        data = data.split(" ")
        data = list(map(int, data))
        if len(set(data)) != len(data):
            raise Exception("No valid data")
        return data
    except Exception as e:
        print(e)
        return []
    



def main():
    
    data = get_data()
    print(data)

    if len(data) == 0:
        return

    minterms = Minterms(data)
    #'''
    print(minterms.get_m_dict())
    minterms.pair_data()
    #print(minterms.get_m_dict())
    print(minterms.get_implicants())
    print(len(minterms.get_implicants()))
    print(minterms._m_list)
    table = Table(minterms._m_list,minterms.get_implicants())
    table.show()
    #'''
    print(table.get_first_implicants())
    table.propagate_implicants(table.get_first_implicants())
    table.search_smallest_row()
    print(" ")
    table.show()
    table.show_true_implicants()
    table.show_checked_columns()


main()
