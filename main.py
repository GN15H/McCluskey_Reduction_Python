from minterms import Minterms

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
    #'''
    #print(minterms.list_dashes([1,3,5,7]))
    #print(minterms.list_dashes([33,35,37,39]))
    #print(minterms.compare_list_dashes([1,3,5,7],[33,35,37,39]))


main()
