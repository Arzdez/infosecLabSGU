import os
import sys


my_name = os.path.basename(__file__)
block = 2
name_and_hash = {}

if os.path.exists("my_hash.txt"):
    
    with open("my_hash.txt", 'r') as f:
        chek_file = f.readline()
        
    if "first run!" in chek_file:
        print("Вижу волшебное слово! Это мой первый запуск, запишу свой хэш")
        with open(my_name, 'rb') as f:
            xor_hash = f.read(block)
                            
            for i in range(f.tell(), os.path.getsize(my_name) // 2):
                xor_hash = bytes(x ^ y for x, y in zip(xor_hash, f.read(block)))
                                
            if (os.path.getsize(my_name) != f.tell()):
                zero_end = b'0'*(os.path.getsize(my_name) - f.tell())
                xor_hash = bytes(x ^ y for x, y in zip(xor_hash, f.read() + zero_end))
                
            name_and_hash[my_name] = xor_hash
            
        with open("my_hash.txt", 'w') as f:
            for key, val in name_and_hash.items():
                f.write(f'{key}- {val} \n')

    else:
        print("Волшебного слова нет - Проверяюсь")
        block = 2
        hashes_tmp = []
        hashes = {}
        name_files = []
        with open("my_hash.txt", "r") as f:
            data = f.readlines()

            for i in data:
                tmp = i.replace("\n",'')
                hashes_tmp = tmp.replace("-","").split()
                hashes[hashes_tmp[0]] = hashes_tmp[1]
                name_files.append(hashes_tmp[0])
                
        with open(my_name, 'rb') as f:
            xor_hash = f.read(block)
                            
            for i in range(f.tell(), os.path.getsize(my_name) // 2):
                xor_hash = bytes(x ^ y for x, y in zip(xor_hash, f.read(block)))
                                
            if (os.path.getsize(my_name) != f.tell()):
                zero_end = b'0'*(os.path.getsize(my_name) - f.tell())
                xor_hash = bytes(x ^ y for x, y in zip(xor_hash, f.read() + zero_end))
            
            
            if str(xor_hash) not in hashes[my_name]:
                print("Я повреждён")
                        
            else:
                print("Я успешно прошёл проверку")
                
else: 
    print("Файла для проверки целостности не обнаружено, прекращаю работу")
            
    


        

