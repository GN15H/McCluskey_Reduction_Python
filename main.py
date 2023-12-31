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

    if len(data) == 0:
        return
    elif len(data) == 1 :
        if data[0] == 1:
            print('A')
            return
        if data[0] == 0:
            print("A'")
            return

    minterms = Minterms(data)
    minterms.pair_data()
    table = Table(minterms._m_list,minterms.get_implicants(), minterms.get_number_variables())
    table.show()
    print(" ")
    table.solve()

main()
