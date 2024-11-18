import zipfile

class LZ78:
    """
    Клас за компресия и декомпресия на текст с помощта на алгоритъма LZ78.
    Предоставя методи за:
    - Компресия на текст.
    - Декомпресия на компресиран текст.
    - Запис на компресирани данни в ZIP файл.
    - Зареждане на текст от файл.
    """
    
    def __init__(self):
        """
        Инициализира речниците, използвани за компресия и декомпресия.
        - `self.dictionary` е речник за компресия.
        - `self.inverse_dictionary` е обратен речник за декомпресия.
        """
        self.dictionary = {}  # Речник за компресия
        self.inverse_dictionary = {}  # Обратен речник за декомпресия

    def compress(self, input_text: str):
        """
        Компресира текст, използвайки алгоритъма LZ78.
        Параметри:
            input_text (str): Текстът, който трябва да бъде компресиран.
        Връща:
            list of tuples: Списък от двойки (индекс, символ), представляващ компресирания текст.
        """
        self.dictionary = {}
        compressed_data = []
        current_phrase = ""
        dict_size = 1

        for char in input_text:
            new_phrase = current_phrase + char
            if new_phrase not in self.dictionary:
                # Добавя нова фраза в речника
                self.dictionary[new_phrase] = dict_size
                dict_size += 1

                if current_phrase == "":
                    compressed_data.append((0, char))
                else:
                    compressed_data.append((self.dictionary[current_phrase], char))

                current_phrase = ""
            else:
                current_phrase = new_phrase

        # Обработва остатъчната фраза, ако има такава
        if current_phrase:
            compressed_data.append((self.dictionary[current_phrase], ""))

        return compressed_data

    def decompress(self, compressed_data):
        """
        Декомпресира данни, използвайки алгоритъма LZ78.
        Параметри:
            compressed_data (list of tuples): Компресирани данни, генерирани от `compress`.
        Връща:
            str: Оригиналният текст, възстановен от компресираните данни.
        """
        self.inverse_dictionary = {}
        decompressed_text = ""
        dict_size = 1

        for index, char in compressed_data:
            if index == 0:
                phrase = char
            else:
                phrase = self.inverse_dictionary[index] + char

            decompressed_text += phrase
            self.inverse_dictionary[dict_size] = phrase
            dict_size += 1

        return decompressed_text

    def save_compressed_to_zip(self, compressed_data, zip_filename):
        """
        Записва компресирани данни в ZIP файл.
        Параметри:
            compressed_data (list of tuples): Компресирани данни, генерирани от `compress`.
            zip_filename (str): Името на ZIP файла, в който ще бъдат записани данните.
        """
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Конвертира компресираните данни в низ за запис в ZIP
            compressed_string = str(compressed_data)
            zipf.writestr("compressed_data.txt", compressed_string)

    def load_text_from_file(self, filename):
        """
        Чете текст от файл.
        Параметри:
            filename (str): Името на файла, от който ще се чете текстът.
        Връща:
            str: Съдържанието на файла като текст.
        """
        with open(filename, 'r') as file:
            return file.read()

if __name__ == "__main__":
    lz78 = LZ78()

    input_filename = "input_text.txt"  
    text = lz78.load_text_from_file(input_filename)
    print("Оригинален текст:", text)

    compressed = lz78.compress(text)
    print("Компресиран текст:", compressed)

    zip_filename = "compressed_output.zip"
    lz78.save_compressed_to_zip(compressed, zip_filename)
    print(f"Компресираните данни са записани в {zip_filename}")

    decompressed = lz78.decompress(compressed)
    print("Декомпресиран текст:", decompressed)