# Generator file

class Generator:
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
            if bool == -1 or index > bool:
                char = command[index]
                # recc is the number of following reccurence
                recc = 1
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

    def steps(self):
        tab = self.open_file("file.txt")
        tab = self.__command(tab, "@#***")
        # tab = add_special_characters(tab)
        # tab = add_number(tab, 2')
        # print_tab(tab)
        self.write_file("result.txt", tab)
