from .write_dict_as_txt import write_to_txt_from_dict


def return_settings_to_default():

    settings = {
        "Файл конфигурации": "Файл не выбран",
        "Рабочая папка": "Папка не выбрана",
        "Папка вывода итогового файла": "Собранные pdf"
    }
    additional_settings = {
        "Метка названия итогового файла": "Итоговый файл:",
        "Метка списка исходных файлов": "Исходные файлы:"
    }

    write_to_txt_from_dict("settings/Основные настройки.txt",
                           settings, ": ",
                           list_splitter=", ")
    write_to_txt_from_dict("settings/Прочие настройки.txt",
                           additional_settings, ": ",
                           list_splitter=", ")
