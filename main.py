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
    print(minterms.get_m_dict(),"\n")
    minterms.pair_data()
    print(minterms.get_m_dict(),"\n")


main()
