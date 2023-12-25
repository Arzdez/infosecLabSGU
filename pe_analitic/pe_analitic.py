import os
import pefile
from tkinter import filedialog as fd
from termcolor import cprint
import logging
#Функция загрузки имён искомых функций
path_to_log = r""
#Для удобства записи найденных имён включим логи
logging.basicConfig(level=logging.INFO,
                    filename=path_to_log,
                    filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")


def read_func_names(path):
    
    func_name = []
    with open(path,'r') as f:
        files = f.readlines()
    
    for i in files:
        func_name.append(i.replace('\n',''))
    
    return func_name


def pe_chek(path, name_func):
    
    pefiles = pefile.PE(path)
    files_with_funk = []
    for entry in pefiles.DIRECTORY_ENTRY_IMPORT:
        
        for imp in entry.imports:
            f_name = imp.name.decode("utf-8")
            if f_name in name_func:
                files_with_funk.append(f_name)


    if files_with_funk:
        #print("-----------------------------------------------------------------------------")
        cprint(f"В файле {path} найдены следующие сетевые функции:", 'yellow')
        for i in files_with_funk:
            cprint(i,"green")
        print("-----------------------------------------------------------------------------")   
        logging.info(f"In file {path} The following network functions have been found: {files_with_funk}")
    else:
        
        print("Сетевых функций не обнаружено")
        print("-----------------------------------------------------------------------------")

                
if __name__ == "__main__":

    #Информация для поиска
    ext = [".exe",
           ".dll",
           ".acm",
           ".ax",
           ".cpl",
           ".drv",
           ".efi",
           ".mui",
           ".ocx",
           ".scr",
           ".sys",
           ".tsp", ]
    
    file_with_names = fd.askopenfilename()
    functions_name = read_func_names(file_with_names)
    
    
    #Выбираем папку где ищем сканируем файлики
    folder_with_files = fd.askdirectory()
    os.chdir(folder_with_files)
    
    #Собираем список всех файлов в директрии
    file_name_in_dir = []
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            file_name_in_dir.append(os.path.join(root, name))

    #Анализируем файлы и выводим имена файлов и найденных в них фукнции
    for i in file_name_in_dir:
        for extention in ext:
            if extention in i:
                print(f"Анализ файла {i}")
                try:
                    pe_chek(i, functions_name)
                except Exception as error:
                    cprint(f"Ошибка анализа файла - {i}","red")
                    print("-----------------------------------------------------------------------------")

            
    
    
    