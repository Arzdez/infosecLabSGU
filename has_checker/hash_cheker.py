import os 
from tkinter import filedialog as fd
from termcolor import cprint



def init_hash(path):
    
    block = 2
    name_and_hash = {}
    os.chdir(path)
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if "hash_list" not in name:
                with open(os.path.join(root, name), 'rb') as f:
                    xor_hash = f.read(block)
                    
                    
                    for i in range(f.tell(), os.path.getsize(os.path.join(root, name)) // 2):
                        xor_hash = bytes(x ^ y for x, y in zip(xor_hash, f.read(block)))
                        
                    if (os.path.getsize(os.path.join(root, name)) != f.tell()):
                        zero_end = b'0'*(os.path.getsize(os.path.join(root, name)) - f.tell())
                        xor_hash = bytes(x ^ y for x, y in zip(xor_hash, f.read() + zero_end))

                name_and_hash[name] = xor_hash
                print(f"Хэш файла {name} - {xor_hash}")
    
    with open("hash_list.txt", 'w') as f:
        for key, val in name_and_hash.items():
            f.write(f'{key}- {val} \n')
        
                    

def hash_chek(path):
    
    os.chdir(path)
    block = 2
    hashes_tmp = []
    hashes = {}
    name_files = []
    
    
    with open("hash_list.txt", "r") as f:
        data = f.readlines()

        for i in data:
            tmp = i.replace("\n",'')
            hashes_tmp = tmp.replace("-","").split()
            hashes[hashes_tmp[0]] = hashes_tmp[1]
            name_files.append(hashes_tmp[0])
            
            
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if "hash_list" not in name:
                with open(os.path.join(root, name), 'rb') as f:
                    xor_hash = f.read(block)
                    
                    for i in range(f.tell(), os.path.getsize(os.path.join(root, name)) // 2):
                        xor_hash = bytes(x ^ y for x, y in zip(xor_hash, f.read(block)))
                        
                    if (os.path.getsize(os.path.join(root, name)) != f.tell()):
                        zero_end = b'0'*(os.path.getsize(os.path.join(root, name)) - f.tell())
                        xor_hash = bytes(x ^ y for x, y in zip(xor_hash, f.read() + zero_end))
                    
                    
                    if name in hashes.keys():
                        name_files.remove(name)
                        
                    try:    
                        if str(xor_hash) not in hashes[name]:
                            print(f"Файл {name} -  повреждён")
                        
                        else:
                            print(f"Файл {name} - успешно прошёл проверку")
                    except  KeyError as error:
                        print(f'Внимание в папке появился новый файл c именем - {name}!')  

    if name_files:
        print("Следующие файлы были удалены:")
        for i in name_files:
            print(i)

                    

        
    



if __name__ == "__main__":
    
    target = fd.askdirectory()
    if os.path.exists(target+"/hash_list.txt"):
        print("Папка уже была захэшированна - сверяю записанные хэши")
        hash_chek(target)

    else:
        print("Файла с хэшэм не обнаружено - провожу расчёт хэша")
        init_hash(target)