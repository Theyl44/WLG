# Generator file

class Generator:
    def __init__(self):
        self.__typo = "@#***"
        self.__result = []

    def setTypo(self, typo):
        self.__typo = typo

    def getTypo(self):
        return self.__typo

    def open_file(self, file_path):
        array = []
        f = open(file_path, "r")
        for i in f:
            array.append(i.strip())
        f.close()
        return array

    def write_file(self, file_path, word_list):
        f = open(file_path, "w")
        for word in word_list:
            f.write(word + "\n")
        f.close()

    def __merge_file(self, file_path, word_list):
        f = open(file_path, "a")
        for word in word_list:
            f.write(word + "\n")
        f.close()

    # number = the number of digit
    def __add_number(self, word_list, digit):
        new_word_list = []
        if word_list == []:
            for number in range(0, (10 ** digit)):
                new_word_list.append(str(number))
        else:
            for word in word_list:
                # new_word_list.append(word)
                for number in range(0, (10 ** digit)):
                    new_word_list.append(word + str(number))

        return new_word_list

    def __add_special_characters(self, word_list):
        new_word_list = []
        special_characters_tab = ["#", "@", "!", "?", "-", "_", "<", ">", ';', ':', ',', '/', "\\", " "]
        for word in word_list:
            # new_word_list.append(word)
            for char in special_characters_tab:
                new_word_list.append(word + char)
        return new_word_list

    def __print_tab(self, word_list):
        for i in word_list:
            print(i)

    def __set_result(self, word_list):
        self.__result = word_list

    def get_result(self):
        return self.__result

    # make every combinaison of list1+list2
    def __mix_list(self, list1, list2):
        l3 = []
        for l1 in list1:
            for l2 in list2:
                l3.append(l1 + l2)
        return l3

    # command = the order for the wordlist
    # # = word
    # * = digit
    # @ = special characters
    # Example : "#@****" = for each word in the word list add a special character and four digit
    def __command(self, word_list, command):
        digi_tab = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        special_characters_tab = ["#", "@", "!", "?", "-", "_", "<", ">", ';', ':', ',', '/', "\\", " "]
        new_word_list = []
        bool = -1

        for index in range(len(command)):
            recc = 1
            if bool == -1 and index > bool:
                char = command[index]
                # recc is the number of following reccurence
                # recc = 1
                if index + 1 <= len(command) - 1:
                    while char == command[index + 1]:
                        recc += 1
                        bool = recc
                        if index + 1 >= len(command) - 1:
                            break
                        else:
                            index += 1
                if char == "#":
                    if new_word_list == []:
                        new_word_list = word_list
                        recc -= 1
                    if recc == 1:
                        new_word_list = self.__mix_list(new_word_list, word_list)
                    elif recc > 0:
                        for i in range(recc):
                            new_word_list = self.__mix_list(new_word_list, word_list)
                if char == "*":
                    if new_word_list == []:
                        new_word_list = digi_tab
                        recc -= 1
                    if recc == 1:
                        new_word_list = self.__add_number(new_word_list, 1)
                    elif recc > 0:
                        new_word_list = self.__add_number(new_word_list, recc)
                if char == "@":
                    if new_word_list == []:
                        new_word_list = special_characters_tab
                        recc -= 1
                    if recc == 1:
                        new_word_list = self.__add_special_characters(new_word_list)
                    elif recc > 0:
                        for i in range(recc - 1):
                            new_word_list = self.__add_special_characters(new_word_list)
        return new_word_list

    def add_tranformation(self, word_list):
        new_word_list = []
        transformations = [
            {'a': ['@', '4']},
            {'b': '8'},
            {'e': '3'},
            {'g': ['9', '6']},
            {'i': ['1', '!']},
            {'o': '0'},
            {'s': ['$', '5']},
            {'t': '7'}
        ]
        check = 0
        for word in word_list:
            new_word_list.append(word)
            for item in transformations:
                for key in item:
                    for elem in item[key]:
                        x = word.replace(key, elem, 1)
                        if x not in word_list and x not in new_word_list:
                            check = 1
                            new_word_list.append(x)

        if check == 1:
            temp = self.add_tranformation(new_word_list)
            return temp
        else:
            return word_list

    def print_help():
        print("Utilisation : ./main.py [_input.txt] [OPTIONS]")
        print("\t -c  'COMMAND': Appliquer la commande COMMAND a la liste de mot")
        print("\t -t : transformation des mots de la liste")
        print("\t -o file.txt : export la liste de mot dans file.txt")
        print("-------")

        print(
            "Utilisation des commandes\n# = word\n* = digit\n@ = special characters\nExample : '#@****' = for each word in the word list add a special character and four digit")

    def steps(self, file):
        tab = self.open_file(file)
        tab = self.__command(tab, self.__typo)
        self.__set_result(tab)
        # tab = add_tranformation(tab)
        # tab = add_special_characters(tab)
        # tab = add_number(tab, 2')
        # print_tab(tab)
        self.write_file("result.txt", tab)
