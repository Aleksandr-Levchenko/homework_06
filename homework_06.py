import sys
import os
import re
from pathlib import Path
import unicodedata # для использования normalize()
import shutil # 
import tarfile
import platform # для clearscrean()




def main():
    
    
    #name = "f№il?eпервый_1@_1.txt"
    #name = normalize(name)
    
    #!!!! if len(sys.argv) > 1:
    sargv = "/Test_HWork_06"
    if len(sargv) > 1:
        # 1. выполним замену символов "/" ПАРАМЕТРА из командной строки sys.argv[1]
        # "/Test_HWork_06"  на "\\Test_HWork_06"
        # sort_dir - это папка в которой будт выполняться все опреции по ДЗ
        # sort_dir - передается как параметр для script в формате /folder
        #!!!! sort_dir = re.sub(r"/",r"\\",sys.argv[1]) 
        # sort_dir = re.sub(r"/",r"\\","/Test_HWork_06") 
        sort_dir = "Test_HWork_06" 
        
        # 2. Получаем текущую папку
        # file_path = sys.argv[0]
        # print("Argv = " + os.path.dirname(file_path))
        # current_dir = os.path.abspath(os.curdir)
        # print("Абсалютный путь" + current_dir)
        # current_dir = os.getcwd()
        # current_dir = "D:\\1. Software\\Python projects\\GoIT_Cource\\1. Python_Core\\homework_06"
        current_dir = sys.argv[0]
        print("Cur dir ARGV 1>>" + current_dir)
        current_dir = current_dir[:current_dir.rfind("\\")]
        print("Cur dir ARGV 2>>" + current_dir)
        
        
        
        # 3. Получим абсолютный путь для СОРТИРОВКИ
        sort_path = os.path.join(current_dir, sort_dir)
        #sort_path = current_dir + sort_dir  # "homework_06\Test_HWork_06"
        
        print("Cur dir >>" + current_dir)
        print("Sort path >>" + sort_path)
        
        # передаем путь к папке на сортировку
        sort_folder(sort_path, sort_path)
    else:
        print("Add an argument(path to folder) in command line before to run the file.py\nExample: python *.py [disk://folder//]")
    
    clear_screen()
    for line in formated_lines():
        print(line)
        # if line.find("==========") > 0:
            
        
    print("The end of programm.")       
# =======================================================    
    

def clear_screen():
    os_name = platform.system().lower()
    
    if os_name == 'windows':
        os.system('cls')
    elif os_name == 'linux' or os_name == 'darwin':
        os.system('clear')


# ========================================        
# Формируем таблицу для печати
# ========================================         
def formated_lines():
    lst = []
    lst.append("|" + "=" * 50 + "|")
    for category, value in dict_search_result.items():
        # Шапка
        #lst.append("|" + "=" * 50 + "|")
        lst.append("|{:^50}|".format(category))
        lst.append("|" + "=" * 50 + "|")
        
        ext = "Extensions: " 
        for extension in value[1]:
            ext += extension + ", "
        ext = ext[:-2]    
        lst.append("|{:<50}|".format(ext))
        lst.append("|" + "-" * 50 + "|")
        
        # Элементы таблицы
        for element in value[0]:
            lst.append("|{:<50}|".format(element))
        
        lst.append("|" + "=" * 50 + "|")    
    return lst

 
# ========================================
# Функция выполняет РАЗБОР папки с ХЛАМОМ 
# ========================================       
def sort_folder(pth, parent_folder):
    # print("*" * 15)
    # print(pth)
    category = ""
    p = Path(pth)
    
    # проходим циклом по дереву каталогов
    for item in p.iterdir():
        category = "uknown"
        full_name = f"{pth}\\{item.name}"
        
        # работаем с файлом
        if item.is_file():
            category = get_category(item.name)
        
        # работаем с папкой
        else:
            category = "folder"
            if is_folder(full_name):
                sort_folder(full_name, parent_folder)
        
        # нормализуем имя папки/файла
        if not category == "uknown":
            norm_name = normalize(item.name)
        if item.name != norm_name:
            ren_item(full_name, f"{pth}\\{norm_name}")
        
        # работаем с файлом
        if category != "folder":
            # добавим новый елемент в словарь найденого.
            # is_makedir=True сигнализирует item был добавлен через обработку исключения
            # т.е. папки для этой катеогрии еще не существует 
            is_makedir = search_result_add_item(category, norm_name)
            search_result_add_extension(category, norm_name)
            if is_makedir: # создадим ПЕРВЫЙ раз папку для КАТЕГОРИИ
                os.mkdir(f"{parent_folder}\\{category}")

            # разнесем файлы по папкам категорий
            source = full_name
            destination = f"{parent_folder}\\{category}" 
            try:
                shutil.move(source, destination)
            except:
                new_filename = "copy_" + source[source.rfind("\\") + 1:]
                new_source = f"{pth}\\{new_filename}"
                
               # если файл существует с таким именем
                os.rename(source, new_source)
                shutil.copy(new_source, destination)
                os.remove(new_source)
                norm_name = new_filename
               # обновим инф. в словаре о новом файле
                search_result_update(category, norm_name)
               
                
            # если архив тогда распакуем его
            if category == "archives":
                # создадим под-директорию
                name_archive_folder = norm_name.split(".")[0]
                extension = norm_name.split(".")[-1]
                os.mkdir(f"{parent_folder}\\archives\\{name_archive_folder}")
                archive_path = f"{parent_folder}\\archives\\{norm_name}"
                destination_folder = f"{parent_folder}\\archives\\{name_archive_folder}"
                try:
                    shutil.unpack_archive(archive_path, destination_folder, extension)
                except:
                    print("The error has accurred during unpuck an archive!")
        
        else:  # работаем с папкой
               # если текущая папка после переноса файлов УЖЕ пустая УДАЛИМ ее
            norm_path = f"{pth}\\{norm_name}"
            if not(is_folder(norm_path)):
                del_folder(norm_path)
                
# =========================================
# =========================================


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# заменяет кирилицу на латинский словарь
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def cyr_lat(name)->str:
    # создадим таблицу
    trans_table = str.maketrans(translate_dict)
    return name.translate(trans_table)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Функция нормализует [name] пакпи/файла
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def normalize(name:str) ->str:
    
    # 1. замена кирилицы на лат
    name = cyr_lat(name)
    
    # если файл то получим его имя    
    extension = ""
    # if len(name.split(".")[0]) > 0:
    if name.rfind(".") > 0:
        extension = "." + name.split(".")[-1]
        name = name.split(".")[0]
        
    
    # 2. Оставим a-z, A_Z, 0-9;  ^ - означает отрицание
    pattern = "[^a-zA-Z0-9]"
    name = re.sub(rf"{pattern}","_", name)
    return f"{name}{extension}"
        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
# Обновим инф. о найденом элементе в СЛОВАРЕ 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   
def search_result_update(category, item):
    dict_search_result[category][0][-1] = item


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
# Добавляет найденое расширение в set() СЛОВАРЯ
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
def search_result_add_extension(category, item):
    try:
        extension = item.split(".")[-1]
        dict_search_result[category][1].add(extension)
    except:
        #dict_search_result["extension"][1] = set()
        dict_search_result[category][1].add(extension)
            
            
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
# Добавляет найденый элемент в list() СЛОВАРЯ
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
def search_result_add_item(category, item) -> bool:
    try:
        # if len(dict_search_result[category]) > 0:
            dict_search_result[category][0].append(item)
            return False
    except KeyError:
        dict_search_result[category] = [[],set()]
        dict_search_result[category][0].append(item)
        return True # папки для этой категории еще НЕ существует


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
# Переименовывает папку
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def ren_item(old_path, norm_path):
    os.rename(old_path, norm_path)
    
    # if type == False:
    #     os.rename(old_path, norm_path)
    #     # old_name = os.path.basename(path)
    # else:
    #     os.rename(old_path, norm_path)
        
       
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
# Удаляет папку. Вызывается когда папка была ПУСТОЙ
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def del_folder(folder_path:str) ->None:
    os.rmdir(folder_path)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# проверка на пустой каталог
# Возвращает True = full; False = empty
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def is_folder(folder_path:str) ->bool:
    # Получить список файлов и папок в папке
    contents = os.scandir(folder_path)

    # Преобразовать итератор в список
    contents_list = list(contents)

    # Проверить, является ли список пустым
    if len(contents_list) == 0:
        return False
    else:
        return True


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Функция возвращает КАТЕГОРИЮ к которой относится файл
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_category(file_name:str) ->str:
    category = "uknown"
    for ct,value in dict_category.items():
        extension = file_name.split(".")[-1]
        if extension:
            if extension.upper() in value:
                category = ct 
                break
    return category
    


# Точка входа в программу
if __name__ == "__main__":
    dict_category = {"images":["JPEG", "PNG", "JPG", "SVG"],\
                    "documents":["DOC", "DOCX", "TXT", "PDF", "XLSX", "PPTX"],\
                    "audio":["MP3", "OGG", "WAV", "AMR"],\
                    "video":["AVI", "MP4", "MOV", "MKV"],\
                    "archives":["ZIP", "GZ", "TAR"]}
    
    dict_search_result = {}
    
    translate_dict = {ord("а"):"a", ord("б"):"b", ord("в"):"v", ord("г"):"h", ord("ґ"):"g",\
    ord("д"):"d", ord("е"):"e", ord("є"):"ye", ord("ж"):"zh", ord("з"):"z", ord("и"):"y",\
    ord("і"):"i", ord("к"):"k", ord("л"):"l", ord("м"):"m", ord("н"):"n", ord("о"):"o",\
    ord("п"):"p", ord("р"):"r", ord("с"):"s", ord("т"):"t", ord("у"):"u", ord("ф"):"f",\
    ord("х"):"kh", ord("ц"):"ts", ord("ч"):"ch", ord("ш"):"sh", ord("щ"):"shch", ord("ъ"):"",\
    ord("ы"):"y", ord("ь"):"", ord("э"):"e", ord("ю"):"yu", ord("я"):"ya", ord("й"):"i",\
    ord("ё"):"yo", ord("Є"):"YE", ord("А"):"A", ord("Б"):"B", ord("В"):"V", ord("Г"):"G",\
    ord("Д"):"D", ord("Е"):"E", ord("Ё"):"YO", ord("Ж"):"ZH", ord("З"):"Z", ord("И"):"Y", ord("Й"):"I",\
    ord("К"):"K", ord("Л"):"L", ord("М"):"M", ord("Н"):"N", ord("О"):"O", ord("П"):"P", ord("Р"):"R",\
    ord("С"):"S", ord("Т"):"T", ord("У"):"U", ord("Ф"):"F", ord("Х"):"KH", ord("Ц"):"TS", ord("Ч"):"CH",\
    ord("Ш"):"SH", ord("Щ"):"SHCH", ord("Ъ"):"", ord("Ы"):"Y", ord("Ь"):"", ord("Э"):"E", ord("Ю"):"YU",\
    ord("Я"):"YA", ord("ї"):"yi", ord("Ґ"):"G", ord("Ї"):"YI", ord(" "):"_", ord("І"):"I"}
    
    main()
    