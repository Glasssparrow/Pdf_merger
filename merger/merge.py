from PyPDF2 import PdfMerger
from datetime import datetime


def merge_pdf(path_input_folder, configuration_file_name,
              output_folder_name,
              output_mark, list_mark):
    output_file_name = read_file_name_from_txt(
        f"{path_input_folder}/{configuration_file_name}",
        output_mark=output_mark,
        list_mark=list_mark
    )
    files_list = read_files_list_from_txt(
        f"{path_input_folder}/{configuration_file_name}",
        output_mark=output_mark,
        list_mark=list_mark
    )
    time = datetime.now()
    output_path = f"{path_input_folder}/{output_folder_name}/" \
                  f"{output_file_name} {time:%d.%m %Hч%Mм}.pdf"
    input_paths = []
    for file in files_list:
        input_paths.append(f"{path_input_folder}/{file}.pdf")
    merge(list_of_pdfs=input_paths, path_output=output_path)


def merge(list_of_pdfs, path_output):
    merger = PdfMerger()
    with open(path_output, "wb") as output_file:
        for file in list_of_pdfs:
            merger.append(file)
        merger.write(output_file)


def read_file_name_from_txt(path_to_txt, output_mark, list_mark):
    file = open(path_to_txt, "r", encoding="utf-8")
    try:
        text = file.read()
    except Exception as error:
        error.args = (f"Не удалось прочитать файл {path_to_txt}",)
        raise
    finally:
        file.close()

    text_list = text.split("\n")

    mark_was_found = False
    for strings_with_whitespace in text_list:
        string = strings_with_whitespace.strip()
        # Пропускаем строку если она пуста
        if not string:
            continue
        if string == output_mark:
            mark_was_found = True
            continue
        if mark_was_found is True and string == list_mark:
            break
        if mark_was_found:
            return string
    raise Exception(f"Не найдена строка {output_mark}.\n"
                    f"В файле {path_to_txt}")


def read_files_list_from_txt(path_to_txt, output_mark, list_mark):
    file = open(path_to_txt, "r", encoding="utf-8")
    try:
        text = file.read()
    except Exception as error:
        error.args = (f"Не удалось прочитать файл {path_to_txt}",)
        raise
    finally:
        file.close()

    text_list = text.split("\n")

    files_list = []
    mark_was_found = False
    for strings_with_whitespace in text_list:
        string = strings_with_whitespace.strip()
        # Пропускаем строку если она пуста
        if not string:
            continue
        if string == list_mark:
            mark_was_found = True
            continue
        if mark_was_found is True and string == output_mark:
            break
        if mark_was_found:
            files_list.append(string)
    if files_list:
        return files_list
    raise Exception(f"Не найдена строка {list_mark} или нет "
                    f"данных по файлам после этой строки.\n"
                    f"В файле {path_to_txt}")
