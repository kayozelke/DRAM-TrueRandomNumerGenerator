import matplotlib.pyplot as plt

from Crypto.Cipher import AES
import time

st = time.time()

numbers = []
numbers_8bit = []


# Wczytanie liczb z pliku
with open('output.txt') as f:
    for x in f.readlines():
        x_int = int(x)  # konwersja na liczbe calkowita
        numbers.append(int(x_int))


with open('preprocessing.txt', 'w') as f:
    for x in numbers:
        bits = format(x & 0b111, '03b')  # pobieramy 3 ostatnie bity i formatujemy jako 3-znakowy ciag binarny z wiodacymi zerami
        f.write(bits)  # zapisujemy do pliku

with open('preprocessing.txt') as f:
    line = f.readline().strip()  # odczytujemy jedyna linie pliku i usuwamy biale znaki na koncach

    # tworzymy nowa liste z podzialem kazdych 8 znakow na osobne elementy
    data = [line[i:i+8] for i in range(0, len(line), 8)]
    for string_x in data:
        # zamiana ciagu znakow string
        # "2" w drugim argumencie oznacza konwersje z systemu binarnego
        numbers_8bit.append(int(string_x, 2))






key = b'Klucz Szyfrujacy'
cipher = AES.new(key, AES.MODE_ECB)
encrypted_16bit_packs = []

with open('preprocessing.txt', 'rb') as f:
    while True:
        # czytaj 16 bitow
        data = f.read(16)
        
        # jesli nie udalo sie nic wiecej odczytac, przerwij petle
        if not data:
            break
    

        encrypted_16bit = cipher.encrypt(data)
        encrypted_16bit_packs.append(encrypted_16bit)



# Konwertowanie zaszyfrowanych danych na ciag zer i jedynek
binary_data = ''
for pack in encrypted_16bit_packs:
    for b in pack:
        binary_data += format(b, '08b')
# Zapisanie ciagu zer i jedynek do pliku
with open('final_trn.txt', 'w') as f:
    f.write(binary_data)



    
et = time.time()
print('Execution time:', '{0:.10f}'.format((et - st)*(10**(9))), 'ns')
