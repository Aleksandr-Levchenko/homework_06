import sys
import os
import re
from pathlib import Path
import shutil # 
import tarfile
import platform # для clearscrean()


def main() ->str:
    
    # очищення екрану
    clear_screen()
    
    # try:
    #     sort_path = sys.argv[1]
    # except:
    #     return ("Add an argument (a path to folder) in command line before to run the file.py\nExample: python *.py [disk://folder//]")
    
     #строка для отладки без передачи ПАРАМЕТРОВ argv[]
    sort_path = "D:\\1._Test\\test_DIR_hw_06" 
    
    # 3. отримаємо абсолютний шлях для СОРТУВАННЯ
    sort_path = Path(sort_path)
    
    print("Тестовая папка для сортировки : ", sort_path)
    
    # перевіремо наявність шляху
    if not sort_path.exists(): return f"The path {sort_path} isn't available."
    
    # передамо шлях до теки де виконаємо сортування файлів
    sort_folder(sort_path, sort_path)
    
    # виводимо результати роботи з зформованого списку
    for line in formated_lines():
        print(line)
            
    return "The end of programm."
# =======================================================    
    


# ========================================
# Функція виконує РОЗБІР теки із ХЛАМОМ 
# ========================================       
def sort_folder(pth, parent_folder):
    category = ""
    
    # проходимо циклом по древу каталогів
    for item in pth.iterdir():
        category = "other"
        full_name = pth.joinpath(item) 
        
        # працюємо з файлом
        if item.is_file():
            category = get_category(item.name)
        
        # працюємо з текою
        else:
            category = "folder"
            if is_folder(full_name):
                sort_folder(full_name, parent_folder)
        
        # нормалізація імені папки або файла
        if not category == "other":
            norm_name = m_normalize(item.name)
        else:
            norm_name = item.name
        
        # перевіремо зміни у імені
        if item.name != norm_name:
            full_name.rename(pth.joinpath(norm_name))
        
        # працюємо з файлом
        if category != "folder":
            # додамо у словник НОВИЙ елемент для ЗНАЙДЕНОЇ інф.
            # is_makedir=True сигналізує, що ITEM був доданий через обробку Exception
            # тоб то теки для цієї катеогрії ще не існує
            is_makedir = search_result_add_item(category, norm_name)
            search_result_add_extension(category, norm_name)
            if is_makedir: # створимо ПЕРШИЙ раз теку для КАТЕГОРІЇ
                parent_folder.joinpath(category).mkdir()

            # розберемо файли по теках для своїх КАТЕГОРІЙ
            source = full_name
            destination = parent_folder.joinpath(category)
            destination = destination.joinpath(source.name)
            try:
                source.rename(destination)  # ПЕРЕМІЩЕННЯ!!!
            except:
                # сформуємо нове ім'я для файлу
                new_filename = f"{source.stem}_copy{source.suffix}"
                new_source = pth.joinpath(new_filename)
                
               # якщо файл існує з таким ім'ям
                source.rename(new_source)
                
                destination = parent_folder.joinpath(category)
                destination = destination.joinpath(new_filename)
                shutil.copy(new_source, destination)
                new_source.unlink()  # видалення файла
                
                norm_name = new_filename
               # оновимо інф. у словнику стосовно нового файлу
                search_result_update(category, norm_name)
               
            # якщо це архів розпакуємо його
            if category == "archives":
                # створимо теку для архіву
                name_archive_folder = norm_name.split(".")[0]
                extension = norm_name.split(".")[-1]
                
                archive_folder = parent_folder.joinpath(category)
                archive_folder.joinpath(name_archive_folder).mkdir()
                
                archive_path = archive_folder.joinpath(norm_name)
                
                destination_folder = archive_folder.joinpath(name_archive_folder)
                try:
                    shutil.unpack_archive(archive_path, destination_folder, extension)
                except:
                    print("The error has accurred during unpuck an archive!")
        
        else:  # працюємо з текою
               # якщо тека з якою працюємо ВЖЕ порожня ВИДАЛЕМО її
            norm_path = pth.joinpath(norm_name)   
            
            if not(is_folder(norm_path)):
                norm_path.rmdir()
                

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~ Допоміжні функції ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def clear_screen():
    os_name = platform.system().lower()
    
    if os_name == 'windows':
        os.system('cls')
    elif os_name == 'linux' or os_name == 'darwin':
        os.system('clear')
        
        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# замінює кирилицю на латинский словник
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def cyr_lat(name)->str:
    # создадим таблицу
    trans_table = str.maketrans(translate_dict)
    return name.translate(trans_table)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Перевірка ну порожню ТЕКУ 
# Повертає True = full; False = empty
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
    
    
# ========================================        
# Формуємо таблицю для друку
# ========================================         
def formated_lines():
    lst = []
    lst.append("|" + "=" * 50 + "|")
    for category, value in dict_search_result.items():
        # Шапка
        lst.append("|{:^50}|".format(category))
        lst.append("|" + "=" * 50 + "|")
        
        ext = "Extensions: " 
        for extension in value[1]:
            ext += extension + ", "
        ext = ext[:-2]    
        lst.append("|{:<50}|".format(ext))
        lst.append("|" + "-" * 50 + "|")
        
        # формуємо елементи таблиці
        for element in value[0]:
            lst.append("|{:<50}|".format(element))
        
        lst.append("|" + "=" * 50 + "|")    
    return lst

    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Функція повертає КАТЕГОРІЮ до якої відноситься файл
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_category(file_name:str) ->str:
    category = "other"
    for ct,value in dict_category.items():
        extension = file_name.split(".")[-1]
        if extension:
            if extension.upper() in value:
                category = ct 
                break
    return category

   
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Функція нормалізує [name] теки/файла
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def m_normalize(name:str) ->str:
    
    # 1. замена кирилицы на лат
    name = cyr_lat(name)
    
    # если файл то получим его имя    
    extension = ""
    
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
        dict_search_result[category][1].add(extension)
            
            
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
# Додає знайдений елемент до list() СЛОВНИКА
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
def search_result_add_item(category, item) -> bool:
    try:
            dict_search_result[category][0].append(item)
            return False
    except KeyError:
        dict_search_result[category] = [[],set()]
        dict_search_result[category][0].append(item)
        return True # папки для этой категории еще НЕ существует


# Місце входу у програму
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
    
    print(main())
    