from .settings.settings import return_settings_to_default
from .settings.read_txt_as_dict import read_as_dict
from tkinter import filedialog as fd
from tkinter import Button, Tk, Label
from merger.merge import merge_pdf
from datetime import datetime


class Gui:

    title_text = "Объединитель pdf 1.0"
    settings_label_text = "Сброс настроек закроет окно"

    # Функция нужна для формирования пути к папке из пути к файлу.
    @staticmethod
    def _cut_filename(path_to_file, return_path=True):
        """
        Обрабатывает путь к файлу в формате - ххх/ххх/file.file.
        Отсекает часть /file.file оставляя ххх/ххх
        """
        split = path_to_file.split("/")
        # Получаем длину последнего фрагмента после "/".
        # Прибавляем единицу т.к. "/" тоже убираем.
        delete = len(split[len(split)-1])+1
        if return_path:
            return path_to_file[:-delete]
        else:
            return path_to_file[len(path_to_file)-delete+1:]

    # Функция выбора пути к файлу с исходными данными
    def _choose_filename(self):
        """
        Функция для кнопки выбора файла.
        Записывает в словарь settings путь к файлу и путь к папке.
        """
        path_to_txt = (
            fd.askopenfilename(title="Выберите файл",
                               initialdir=(
                                   self.settings["Рабочая папка"])
                               )
        )
        self.settings["Файл конфигурации"] = self._cut_filename(
            path_to_txt, return_path=False
        )
        self._text_path.configure(
            text=self.settings["Файл конфигурации"]
        )
        self.settings["Рабочая папка"] = (
            self._cut_filename(path_to_txt)
        )
        self._text_folder.configure(text=(
            self.settings["Рабочая папка"])
        )

    def _choose_folder(self):
        """
        Функция выбора папки в которую будет выводиться файл с выполненными
        расчетами.
        """
        self.settings["Папка вывода итогового файла"] = self._cut_filename(
            fd.askdirectory(title="Выберите папку",
                            initialdir=(self.settings["Рабочая папка"])),
            return_path=False
        )
        self._text_output_folder.configure(text=(
            self.settings["Папка вывода итогового файла"])
        )

    def _correct_path(self):
        self._read_settings()
        self._text_path.configure(text=self.settings["Файл конфигурации"])
        self._text_folder.configure(text=self.settings["Рабочая папка"])
        self._text_output_folder.configure(
            text=self.settings["Папка вывода итогового файла"])

    def _return_settings_to_default(self):
        return_settings_to_default()
        self._settings_window.destroy()
        self._correct_path()

    def _open_settings(self):
        self._settings_window = Tk()
        self._settings_window.title("Настройки")
        self._settings_window.geometry("230x50")

        self._return_to_default_button = (
            Button(self._settings_window,
                   text="Вернуть настройки по умолчанию",
                   command=self._return_settings_to_default)
        )
        self._return_to_default_button.grid(column=0, row=1)

        self._warning_text = Label(self._settings_window,
                                   text=self.settings_label_text)
        self._warning_text.grid(column=0, row=0)

        self._settings_window.mainloop()

    def _merge(self):
        try:
            args = {
                "path_input_folder":
                    self.settings["Рабочая папка"],
                "configuration_file_name":
                    self.settings["Файл конфигурации"],
                "output_folder_name":
                    self.settings["Папка вывода итогового файла"],
                "output_mark":
                    self.additional_settings[
                        "Метка названия итогового файла"],
                "list_mark": self.additional_settings[
                    "Метка списка исходных файлов"]
            }
            merge_pdf(**args)
            time = datetime.now()
            text = f"Объединение выполнено. Время: {time: %H:%M:%S} \n"
            self._text_warning.configure(text=text)
        except Exception as error:
            time = datetime.now()
            text = f"Возникла ошибка. Время: {time: %H:%M:%S} \n"
            for er in error.args:
                text += str(er) + "\n"
            self._text_warning.configure(text=text)

    def _read_settings(self):
        """
        Считываем данные из текстовых файлов настрое
        """
        self.settings = read_as_dict(
            "settings/Основные настройки.txt")
        self.additional_settings = read_as_dict(
            "settings/Прочие настройки.txt")

    def __init__(self):
        self._read_settings()
        # Оформление окна
        self._window = Tk()
        self._window.title(self.title_text)
        self._window.geometry("580x220")
        # Ширина для кнопок
        width = 12

        # Кнопка выбора файла
        self._file_selection_button = (
            Button(self._window, text="Выбрать файл исходных данных",
                   width=width * 3 + 3,
                   command=self._choose_filename,
                   bg="green")
        )
        self._file_selection_button.grid(columnspan=3, column=2,
                                         row=0)

        # Кнопка выбора папки
        self._folder_selection_button = (
            Button(self._window, text="Выбрать папку для печати",
                   width=width * 2 + 2,
                   command=self._choose_folder)
        )
        self._folder_selection_button.grid(columnspan=2, column=0,
                                           row=0)

        # Кнопка окна настроек
        self._settings_button = (
            Button(self._window, text="Настройки",
                   width=width,
                   command=self._open_settings))
        self._settings_button.grid(columnspan=1, column=5, row=0)

        # Текст пути к файлу
        self._text_path = (
            Label(text=self.settings["Файл конфигурации"]))
        self._text_path.grid(columnspan=6,
                             column=0, row=1)

        # Текст пути к рабочей папке
        self._text_folder = (
            Label(text=self.settings["Рабочая папка"]))
        self._text_folder.grid(columnspan=6,
                               column=0, row=2)

        # Текст пути к папке в которую будем печатать
        self._text_output_folder = (
            Label(text=self.settings["Папка вывода итогового файла"]))
        self._text_output_folder.grid(columnspan=6,
                                      column=0, row=3)

        # Кнопка расчета
        self._calculate_button = (
            Button(self._window, text="Рассчитать",
                   width=width * 6 + 6,
                   command=self._merge,
                   bg="green")
        )
        self._calculate_button.grid(columnspan=6, column=0,
                                    row=4)

        # Текст ошибки
        self._text_warning = (
            Label(text="Расчет еще не выполнялся"))
        self._text_warning.grid(columnspan=6,
                                column=0, row=5)

        # Запускаем окно
        self._window.mainloop()
