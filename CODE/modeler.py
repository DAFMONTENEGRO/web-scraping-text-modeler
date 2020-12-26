#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import requests
import mysql.connector
from bs4 import BeautifulSoup


class Menu:

    def __init__(self, user="", password=""):
        self.choice = "0"
        self.message = "Modelador de textos"
        self.user = user
        self.password = password
        self.modeler = Modeler(self.user, self.password)
        if self.modeler.sql_connection():
            self.app()
        else:
            self.start()

    def start(self):
        self.select(self.message, "Conexión al servidor:")
        self.user = input("      Para continuar, por favor inicie sesion.\n\n        - Usuario: ")
        self.password = input("        - Contraseña: ")
        self.modeler = Modeler(self.user, self.password)
        print("\n      Estableciendo una conexión... ", end="")
        if self.modeler.sql_connection():
            print("Sistema conectado al servidor.")
            time.sleep(2)
            self.app()
        else:
            print("Acceso denegado, por favor intentelo de nuevo.".format(self.user))
            time.sleep(2)
            self.start()

    def app(self):
        options_menu = ("Crear script", "Consultar datos", "Ver funcionalidades", "Configurar conexión al servidor",
                        "Ayuda", "Salir")
        self.select(self.message, "Menu principal:", options_menu)
        if self.choice == "1":
            options_submenu_1 = ("Desde un texto", "Desde una carpeta", "Desde la web (web scraping)", "Atras")
            self.select(self.message, "Crear script:", options_submenu_1)
            if self.choice == "1":
                Menu.clear(self.message)
                choice = input("    Escribe la ruta del archivo que deseas agregar: ")
                choice_two = input("    Escribe el nombre con el que lo deseas guardar: ")
                self.modeler.add_script(choice, choice_two, message=self.message + "\n\n")
                input("\n    ¡Script creado exitosamente!"
                      "\n\n    Presiona cualquier tecla para continuar...")
            elif self.choice == "2":
                Menu.clear(self.message)
                choice = input("    Escribe el nombre de la carpeta que deseas agregar: ")
                choice_two = input("    Escribe el nombre con el que deseas guardar el archivo: ")
                self.modeler.add_folder(choice, choice_two, message=self.message + "\n\n")
                input("\n    ¡Script creado exitosamente!"
                      "\n\n    Presiona cualquier tecla para continuar...")
            elif self.choice == "3":
                Menu.clear(self.message)
                choice = input("    Web Scraping\n\n        Escribe la url desde la que quieres extraer un texto: ")
                try:
                    html = Menu.get_page(choice)
                    print("\n            ¡Documento html extraido con exito!\n")
                    choice = input("        Escribe el tipo del elemento html del cual deseas extraer el texto: ")
                    choice_2 = input("        Escribe el valor 'class' del elemento del cual deseas extraer el texto: ")
                    html = html.find(choice, {"class": choice_2}).find_all("p")
                    paragraphs = ""
                    for element in html:
                        paragraphs += element.text + "\n"
                        print(element.text)
                    choice = input("        Escribe el nombre del archivo con el cual quieres guardar este texto: ")
                    Menu.save_file(choice, paragraphs)
                    input("\n    ¡Script creado exitosamente!"
                          "\n\n    Presiona cualquier tecla para continuar...")
                except requests.exceptions.MissingSchema:
                    print("\nError imprevisto con la url:", choice)
                time.sleep(5)
            self.app()
        elif self.choice == "2":
            options_submenu_2 = ("Ver palabras", "Ver codificación", "Ver textos", "Ver frases", "Atras")
            self.select(self.message, "Consultar datos (limite muestra: 1000):", options_submenu_2)
            if self.choice == "1":
                options_submenu_2_1 = ("Vista datos crea", "Vista datos scripts", "Vista total palabras", "Ver errores",
                                       "Atras")
                self.select(self.message, "Ver palabras:", options_submenu_2_1)
                if self.choice == "1":
                    query = self.modeler.sql_execute("SELECT * FROM crea LIMIT 1000 ;")
                    sum_q = self.modeler.sql_execute("SELECT COUNT(*) FROM crea ;")[0][0]
                    Menu.show_table(self.message, "Vista datos crea (1000):", ["Word", "Frequency"], query, sum_q)
                elif self.choice == "2":
                    query = self.modeler.sql_execute("SELECT * FROM scripts LIMIT 1000 ;")
                    sum_q = self.modeler.sql_execute("SELECT COUNT(*) FROM scripts ;")[0][0]
                    Menu.show_table(self.message, "Vista datos scripts (1000):", ["Word", "Frequency"], query, sum_q)
                elif self.choice == "3":
                    query = self.modeler.sql_execute("SELECT * FROM total_words LIMIT 1000 ;")
                    sum_q = self.modeler.sql_execute("SELECT COUNT(*) FROM total_words ;")[0][0]
                    Menu.show_table(self.message, "Vista datos total palabras (1000):",
                                    ["Word", "Frequency"], query, sum_q)
                elif self.choice == "4":
                    query = self.modeler.sql_execute("SELECT * FROM mistakes LIMIT 1000 ;")
                    sum_q = self.modeler.sql_execute("SELECT COUNT(*) FROM mistakes ;")[0][0]
                    Menu.show_table(self.message, "Vista datos errores (1000):", ["Word", "Frequency"], query, sum_q)
            elif self.choice == "2":
                query = self.modeler.sql_execute("SELECT * FROM codings LIMIT 1000 ;")
                sum_q = self.modeler.sql_execute("SELECT COUNT(*) FROM codings ;")[0][0]
                Menu.show_table(self.message, "Vista codificación textos (1000):",
                                ["Id", "Come_from", "Next_word", "Frequency"], query, sum_q)
            elif self.choice == "3":
                query = self.modeler.sql_execute("SELECT * FROM texts LIMIT 1000 ;")
                sum_q = self.modeler.sql_execute("SELECT COUNT(*) FROM texts ;")[0][0]
                Menu.show_table(self.message, "Vista textos (1000):", ["Id", "Text_name", "Frequency"], query, sum_q)
            elif self.choice == "4":
                query = self.modeler.sql_execute("SELECT * FROM phrases LIMIT 1000 ;")
                sum_q = self.modeler.sql_execute("SELECT COUNT(*) FROM phrases ;")[0][0]
                Menu.show_table(self.message, "Vista frases (1000):",
                                ["Id", "Id_coding", "Phrase", "Frequency", "Text_name"], query, sum_q)
            self.app()
        elif self.choice == "3":
            if self.user == "guest":
                print("paso aqui")
                options_submenu_3 = ("Buscador de frases", "Corrector de ortografía", "Completar una frase", "Atras")
                self.select(self.message, "Ver funcionalidades:", options_submenu_3)
                if self.choice == "1":
                    while self.choice != "exit()":
                        self.select(self.message, "Buscador de frases.")
                        print(
                            "\n      A continuación escriba por favor la parte de una frase que deseé buscar, "
                            "para salir de esta funcionalidad\n      puede escribir el comando "
                            "'exit()' en lugar de una frase.\n")
                        self.choice = input("\n        - Escriba la parte de la frase aqui: ").lower()
                        if self.choice != "exit()":
                            phrases = self.modeler.find_frase(self.choice)
                            if phrases:
                                print("\n          Las frases que contienen esa parte son las siguientes:\n")
                                for i, phrase in enumerate(phrases):
                                    print("            {}. {} ({})".format(i+1, phrase[0], phrase[1]))
                            else:
                                print("\n          No existe ninguna posible palabra que pueda continuar a la frase")
                            input("\n      Presiona cualquier tecla para continuar...")
                    print("\n    Gracias por usar la funcionalidad, hasta pronto.")
                    time.sleep(1)
                if self.choice == "2":
                    options_submenu_3_2 = ("Datos crea", "Datos scripts", "Total palabras")
                    self.select("Corrector de ortografía.",
                                "Para hacer uso de la aplicacion elija una base de datos:",
                                options_submenu_3_2)
                    data = "total_words"
                    if self.choice == "1":
                        data = "crea"
                    elif self.choice == "2":
                        data = "scripts"
                    while self.choice != "exit()":
                        self.select(self.message, "Corrector de ortografía.")
                        print(
                            "\n      A continuación escriba por favor la frase que desea revisar, para salir de esta "
                            "funcionalidad\n      puede escribir el comando 'exit()' en lugar de una frase.\n")
                        self.choice = input("\n        - Escriba su frase aqui: ")
                        if self.choice != "exit()":
                            phrase = self.modeler.spell_checker(self.choice, table=data)
                            if phrase:
                                print("\n          La frase corregida es la siguiente: {}".format(phrase))
                            else:
                                print("\n          No existe ninguna posible correccion para la frase")
                            input("\n      Presiona cualquier tecla para continuar...")
                    print("\n    Gracias por usar la funcionalidad, hasta pronto.")
                    time.sleep(1)
                if self.choice == "3":
                    while self.choice != "exit()":
                        self.select(self.message, "Completar una frase.")
                        print(
                            "\n      A continuación escriba por favor la frase que desea completar, para salir de esta "
                            "funcionalidad\n      puede escribir el comando 'exit()' en lugar de una frase.\n")
                        self.choice = input("\n        - Escriba su frase aqui: ")
                        if self.choice != "exit()":
                            phrase = Menu.split_lines([self.choice, ])[0]
                            predictive = self.modeler.predictive_text(phrase)
                            if predictive:
                                print("\n          Las posibles continuaciones de esta frase son las siguientes:\n")
                                for i, next_word in enumerate(predictive):
                                    print("            {}. {} {} ({})".format(i+1, self.choice.capitalize(),
                                                                              next_word[0], next_word[1]))
                            else:
                                print("\n          No existe ninguna posible palabra que pueda continuar a la frase")
                            input("\n      Presiona cualquier tecla para continuar...")
                    print("\n    Gracias por usar la funcionalidad, hasta pronto.")
                    time.sleep(1)
                self.app()
            else:
                print("adfafdadf")
                options_submenu_3 = ("Buscador de frases", "Corrector de ortografía", "Completar una frase",
                                     "Entrenar corrector ortografico", "Atras")
                self.select(self.message, "Ver funcionalidades:", options_submenu_3)
                if self.choice == "1":
                    while self.choice != "exit()":
                        self.select(self.message, "Buscador de frases.")
                        print(
                            "\n      A continuación escriba por favor la parte de una frase que deseé buscar, "
                            "para salir de esta funcionalidad\n      puede escribir el comando "
                            "'exit()' en lugar de una frase.\n")
                        self.choice = input("\n        - Escriba la parte de la frase aqui: ").lower()
                        if self.choice != "exit()":
                            phrases = self.modeler.find_frase(self.choice)
                            if phrases:
                                print("\n          Las frases que contienen esa parte son las siguientes:\n")
                                for i, phrase in enumerate(phrases):
                                    print("            {}. {} ({})".format(i + 1, phrase[0], phrase[1]))
                            else:
                                print("\n          No existe ninguna posible palabra que pueda continuar a la frase")
                            input("\n      Presiona cualquier tecla para continuar...")
                    print("\n    Gracias por usar la funcionalidad, hasta pronto.")
                    time.sleep(1)
                if self.choice == "2":
                    options_submenu_3_2 = ("Datos crea", "Datos scripts", "Total palabras")
                    self.select("Corrector de ortografía.",
                                "Para hacer uso de la aplicacion elija una base de datos:",
                                options_submenu_3_2)
                    data = "total_words"
                    if self.choice == "1":
                        data = "crea"
                    elif self.choice == "2":
                        data = "scripts"
                    while self.choice != "exit()":
                        self.select(self.message, "Corrector de ortografía.")
                        print(
                            "\n      A continuación escriba por favor la frase que desea revisar, para salir de esta "
                            "funcionalidad\n      puede escribir el comando 'exit()' en lugar de una frase.\n")
                        self.choice = input("\n        - Escriba su frase aqui: ")
                        if self.choice != "exit()":
                            phrase = self.modeler.spell_checker(self.choice, table=data)
                            if phrase:
                                print("\n          La frase corregida es la siguiente: {}".format(phrase))
                            else:
                                print("\n          No existe ninguna posible correccion para la frase")
                            input("\n      Presiona cualquier tecla para continuar...")
                    print("\n    Gracias por usar la funcionalidad, hasta pronto.")
                    time.sleep(1)
                if self.choice == "3":
                    while self.choice != "exit()":
                        self.select(self.message, "Completar una frase.")
                        print(
                            "\n      A continuación escriba por favor la frase que desea completar, para salir de esta "
                            "funcionalidad\n      puede escribir el comando 'exit()' en lugar de una frase.\n")
                        self.choice = input("\n        - Escriba su frase aqui: ")
                        if self.choice != "exit()":
                            phrase = Menu.split_lines([self.choice, ])[0]
                            predictive = self.modeler.predictive_text(phrase)
                            if predictive:
                                print("\n          Las posibles continuaciones de esta frase son las siguientes:\n")
                                for i, next_word in enumerate(predictive):
                                    print("            {}. {} {} ({})".format(i + 1, self.choice.capitalize(),
                                                                              next_word[0], next_word[1]))
                            else:
                                print("\n          No existe ninguna posible palabra que pueda continuar a la frase")
                            input("\n      Presiona cualquier tecla para continuar...")
                    print("\n    Gracias por usar la funcionalidad, hasta pronto.")
                    time.sleep(1)
                if self.choice == "4":
                    options_submenu_3_4 = ("Datos crea", "Datos scripts", "Total palabras")
                    self.select("Entrenador corrector ortografico.",
                                "Para hacer uso de la aplicacion elija una base de datos:",
                                options_submenu_3_4)
                    data = "total_words"
                    if self.choice == "1":
                        data = "crea"
                    elif self.choice == "2":
                        data = "scripts"
                    while self.choice != "exit()":
                        self.select(self.message, "Entrenador corrector ortografico.")
                        print(
                            "\n      A continuación escriba por favor la palabra que deseé revisar, para salir de esta "
                            "funcionalidad\n      puede escribir el comando 'exit()' en lugar de una palabra.\n")
                        self.choice = input("\n        - Escriba su palabra aqui: ")
                        if self.choice != "exit()" and self.choice.isalnum():
                            word = Menu.split_lines([self.choice, ])[0][0]
                            self.modeler.spell_checker_trainer(word, table=data)
                            input("\n      Presiona cualquier tecla para continuar...")
                    print("\n    Gracias por usar la funcionalidad, hasta pronto.")
                    time.sleep(1)
                self.app()
        elif self.choice == "4":
            self.start()
        elif self.choice == "5":
            Menu.clear(self.message)
            print("        !Proximamente desde aqui podras acceder a la pagina web del proyecto!")
            input("\n      Presiona cualquier tecla para continuar...")
            self.app()
        elif self.choice == "6":
            print("\n    Gracias por usar la aplicacion, hasta pronto.")
            time.sleep(1)
            return self.modeler

    def select(self, title, message, options=tuple()):
        Menu.clear(title)
        print("    {}\n".format(message))
        numbers = []
        for index, option in enumerate(options):
            i = index + 1
            numbers.append(str(i))
            print("      {}. {}".format(i, option))
            if i == len(options):
                self.choice = input("\n    Elige un numero: ")
        if self.choice not in numbers and numbers:
            print("\n    ¡No ingresaste una opcion valida! Por favor intentalo de nuevo.")
            time.sleep(2)
            self.select(title, message, options=options)

    @staticmethod
    def folder_paths(folder, directory=None):
        paths = []
        if directory is None:
            directory = os.getcwd() + "\\" + folder
        try:
            list_directory = os.listdir(directory)
        except (FileNotFoundError, OSError):
            return paths
        else:
            for file in list_directory:
                if file.endswith(".txt"):
                    paths.append([directory + "\\" + file, folder + " - " + file[:-4]])
                elif "." not in file:
                    paths.extend(Menu.folder_paths(file, directory=directory + "\\" + file))
            return paths

    @staticmethod
    def get_page(url):
        page = requests.get(url)
        html = BeautifulSoup(page.content, "html.parser")
        return html

    @staticmethod
    def save_file(name, paragraph, mode="w"):
        with open(name, mode, encoding="utf-8") as file:
            file.write(paragraph)

    @staticmethod
    def open_file(name, show=False):
        try:
            with open(name, "r", encoding="utf-8") as file:
                lines = file.readlines()
        except (FileNotFoundError, OSError):
            return []
        else:
            split = Menu.split_lines(lines)
            if show:
                print("\nArchivo abierto:")
                for i in range(len(lines)):
                    print("{:4d}.".format(i + 1), lines[i], end="")
                print("\n\nFrases encontradas:")
                for i in range(len(split)):
                    print("{:4d}.".format(i + 1), split[i])
                print()
            return split

    @staticmethod
    def split_lines(lines):
        phrases = []
        for line in lines:
            cut = 0
            phrase = []
            for i, char in enumerate(line):
                if not char.isalnum():
                    string = line[cut:i]
                    if string != "":
                        phrase.append(string.lower())
                    if not char.isspace() and phrase:
                        phrases.append(phrase[:])
                        phrase.clear()
                    cut = i + 1
            if len(line) > cut:
                phrase.append(line[cut:].lower())
            if phrase:
                phrases.append(phrase)
        verified_phrases = []
        for i in range(len(phrases)):
            if len(phrases[i]) == 1 and len(phrases) > 1:
                if i == 0:
                    phrases[0].extend(phrases[1])
                    phrases[1] = phrases[0]
                else:
                    verified_phrases[-1].extend(phrases[i])
            else:
                verified_phrases.append(phrases[i])
        return verified_phrases

    @staticmethod
    def show_table(title, message, header, values, num_columns):
        Menu.clear(title)
        lines = ((32 * len(header)) + (len(header) + 1))
        print("    {}\n\n\n      ".format(message) + "-" * lines + "\n      |", end="")
        for colum in header:
            print("{:^32}|".format(colum), end="")
        print("\n      " + "-" * lines)
        for row in values:
            print("      ", end="")
            for value in row:
                short_value = str(value)
                if len(short_value) > 30:
                    short_value = value[:25] + "..."
                print("|{:^32}".format(short_value), end="")
            print("|")
        print("      " + "-" * lines + "\n\n\n    Numero de filas totales en la tabla: {}\n\n".format(num_columns))
        input("\n    Presiona cualquier tecla para continuar...")

    @staticmethod
    def charging_screen(message, percentage, edge="  "):
        Menu.clear(message)
        percentage = int(percentage * 100)
        progress_bar = "[{}{}]".format("#" * percentage, " " * (100 - percentage))
        print("    {}{}{}{}".format(edge, progress_bar[:49], "|{}%|".format(percentage), progress_bar[54:]), end="\n\n")

    @staticmethod
    def clear(message=""):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
        print("\n\n  {}\n\n".format(message))


class Modeler:

    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.info = "USE modeler ;\nSET SQL_SAFE_UPDATES = 0 ;\n\n"

    def sql_connection(self):
        try:
            sql_connection = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host="localhost",
                database="modeler",
                auth_plugin="mysql_native_password")
        except mysql.connector.errors.ProgrammingError:
            return None
        else:
            return sql_connection

    def sql_execute(self, sql):
        sql_connection = self.sql_connection()
        cursor = sql_connection.cursor()
        cursor.execute(sql)
        if sql.startswith("SELECT"):
            cursor = cursor.fetchall()
        sql_connection.commit()
        sql_connection.close()
        return cursor

    def sql_call(self, procedure, values):
        sql_connection = self.sql_connection()
        cursor = sql_connection.cursor()
        result = cursor.callproc(procedure, values)
        sql_connection.commit()
        sql_connection.close()
        return result

    def add_folder(self, path_folder, name_folder, message="", show=False):
        Menu.save_file(os.getcwd() + "\\SQL\\{}.sql".format(name_folder), "")
        paths = Menu.folder_paths(path_folder)
        for path in paths:
            self.add_script(path[0], path[1], message=message, folder=name_folder, show=show)

    def add_script(self, path, name, message="", folder="", show=False):
        phrases = Menu.open_file(path, show=show)
        if phrases:
            message += "\n      Agregando el texto '{}', por favor espere.".format(name)
            Menu.charging_screen(message, 0)
            self.info += "-- ----------------------------------------------------------------------\n" + \
                         "-- {}\n".format(name) + \
                         "-- ----------------------------------------------------------------------\n"
            for i, phrase in enumerate(phrases):
                self.info += "SET @come_from = NULL ;\n"
                for word in phrase:
                    self.info += "CALL insert_word('{}') ;\n".format(word)
                    self.info += "CALL insert_coding(@come_from, '{}') ;\n".format(word)
                self.info += "CALL insert_phrase('{}', '{}', @come_from) ;\n".format(" ".join(phrase), name)
                Menu.charging_screen(message, i / len(phrases))
            if folder:
                Menu.save_file(os.getcwd() + "\\SQL\\{}.sql".format(folder), self.info, mode="a")
            else:
                Menu.save_file(os.getcwd() + "\\SQL\\{}.sql".format(name), self.info)
            self.info = "\nUSE modeler ;\nSET SQL_SAFE_UPDATES = 0 ;\n\n"
            Menu.charging_screen(message, 1)
            time.sleep(1)

    def find_frase(self, phrase):
        sql = "SELECT Phrase, Text_name FROM phrases WHERE Phrase LIKE '%{}%' ;"
        search = self.sql_execute(sql.format(phrase.lower()))
        phrases = []
        for phrase in search:
            phrases.append((phrase[0].capitalize(), phrase[1].capitalize()))
        return phrases

    def predictive_text(self, phrase, come_from="IS NULL"):
        sql = "SELECT cod_id FROM coding WHERE cod_come_from {} AND cod_wor_id = {} ;"
        for word in phrase:
            id_word = self.sql_call("id_word", [word, 0])[1]
            if id_word:
                cod_id = self.sql_execute(sql.format(come_from, id_word))
                if cod_id:
                    come_from = "= " + str(cod_id[0][0])
                else:
                    return []
            else:
                return []
        sql = "SELECT (SELECT wor_string FROM word WHERE wor_id = c1.cod_wor_id), " \
              "c1.cod_frequency FROM coding c1 WHERE cod_come_from {} ;".format(come_from)
        return self.sql_execute(sql)

    def spell_checker(self, phrase, table="total_words"):
        split_phrase = Menu.split_lines([phrase, ])
        if split_phrase:
            correct_phrase = []
            for word in split_phrase[0]:
                sql = "SELECT * FROM " + table + " WHERE Word LIKE '{}' ;"
                search = self.sql_execute(sql.format(word))
                if search:
                    correct_phrase.append(word)
                else:
                    size_word = len(word)
                    possible_words = [word, word + "_"]
                    for i in range(size_word):
                        possible_words.append(word[:i] + word[i + 1:])
                        possible_words.append(word[:i] + "_" + word[i:])
                        if size_word > 1:
                            possible_words.append(word[:i] + "_" + word[i + 1:])
                    frequencies = set()
                    for possible in possible_words:
                        frequencies.update(self.sql_execute(sql.format(possible)))
                    if frequencies:
                        old_frequencies = frequencies.copy()
                        if correct_phrase:
                            predictions = self.predictive_text(correct_phrase)
                            predictions_frequencies = set()
                            for prediction in predictions:
                                predictions_frequencies.update(self.sql_execute(sql.format(prediction[0])))
                            frequencies.intersection_update(predictions_frequencies)
                        if frequencies:
                            correct_phrase.append(max(frequencies, key=lambda x: x[1])[0])
                        else:
                            correct_phrase.append(max(old_frequencies, key=lambda x: x[1])[0])
                    else:
                        correct_phrase.append(word)
            return " ".join(correct_phrase).capitalize()
        else:
            return phrase

    def spell_checker_trainer(self, word, table="total_words"):
        sql = "SELECT * FROM " + table + " WHERE Word LIKE '{}' ;"
        print("\n          Detalles de la corrección:")
        word = word.lower()
        size_word = len(word)
        possible_words = [word, word + "_"]
        for i in range(size_word):
            possible_words.append(word[:i] + word[i + 1:])
            possible_words.append(word[:i] + "_" + word[i:])
            if size_word > 1:
                possible_words.append(word[:i] + "_" + word[i + 1:])
        frequencies = set()
        for possible in possible_words:
            frequencies.update(self.sql_execute(sql.format(possible)))
        if frequencies:
            frequencies = sorted(frequencies, key=lambda x: x[1], reverse=True)
            print("\n            Las posibles correcciones para la palabra '{}' son:\n".format(word))
            choice = ""
            numbers = []
            for index, couple in enumerate(frequencies):
                i = index + 1
                numbers.append(str(i))
                print("              - {}. {}".format(i, couple[0].capitalize()))
                if i == len(frequencies):
                    numbers.append(str(i + 1))
                    print("              - {}. {}".format(i + 1, "Ninguna de las anteriores"))
                    choice = input("\n            Elige un numero:  ")
            while choice not in numbers:
                print("\n                ¡No ingresaste una opcion valida! Por favor intentalo de nuevo.")
                choice = input("\n            Elige un numero:  ")
            choice = int(choice)
            if choice != len(frequencies) + 1:
                word = frequencies[choice - 1][0]
                self.sql_call("insert_word", [word, ])
                print("\n        Se agrego una frecuencia a la palabra "
                      "'{}' en la base de datos.".format(word.capitalize()))
            return frequencies
        else:
            print("\n            No se encontro ninguna posible corrección para la palabra '{}', se agrego "
                  "la palabra a la base de datos errores. ".format(word))
            self.sql_call("insert_mistake", [word, ])
            return word


menu = Menu()