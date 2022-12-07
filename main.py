#!/usr/bin/env python3
import sys
import os.path


def open_file(file_path):
    array = []
    f = open(file_path, "r")
    for i in f:
        array.append(i.strip())
    return array


def write_file(file_path, word_list):
    f = open(file_path, "w")
    for word in word_list:
        f.write(word + "\n")


def merge_file(file_path, word_list):
    f = open(file_path, "a")
    for word in word_list:
        f.write(word + "\n")


# number = the number of digit
def add_number(word_list, digit):
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


def add_special_characters(word_list):
    new_word_list = []
    special_characters_tab = ["#", "@", "!", "?", "-", "_", "<", ">", ';', ':', ',', '/', "\\", " "]
    for word in word_list:
        # new_word_list.append(word)
        for char in special_characters_tab:
            new_word_list.append(word + char)
    return new_word_list


def print_tab(word_list):
    write_file("result.txt", word_list)
    for i in word_list:
        print(i, end="\t")
    print("\n#" + str(len(word_list)))


# make every combinaison of list1+list2
def mix_list(list1, list2):
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
def command(word_list, command):
    digi_tab = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    special_characters_tab = ["#", "@", "!", "?", "-", "_", "<", ">", ';', ':', ',', '/', "\\", " "]
    new_word_list = []
    bool = -1

    for index in range(len(command)):

        char = command[index]
        if char == "#":
            if new_word_list == []:
                new_word_list = word_list
            else:
                new_word_list = mix_list(new_word_list, word_list)
        if char == "*":
            if new_word_list == []:
                new_word_list = digi_tab
            else:
                new_word_list = add_number(new_word_list, 1)

        if char == "@":
            if new_word_list == []:
                new_word_list = special_characters_tab
            else:
                new_word_list = add_special_characters(new_word_list)

    return new_word_list


def add_tranformation(word_list):
    new_word_list = []
    transformations = [
        {'a': ['@', '4', 'A']},
        {'b': '8'},
        {'e': ['3', 'E']},
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
        temp = add_tranformation(new_word_list)
        return temp
    else:
        return word_list


def steps():
    tab = open_file("file.txt")
    # tab = command(tab, "#@")
    # tab = add_special_characters(tab)
    # tab = add_number(tab, 2')
    tab = add_tranformation(tab)
    # print_tab(tab)
    write_file("result.txt", tab)


def print_help():
    print("Utilisation : ./main.py [_input.txt] [OPTIONS]")
    print("\t -c  'COMMAND': Appliquer la commande COMMAND a la liste de mot")
    print("\t -t : transformation des mots de la liste")
    print("\t -o file.txt : export la liste de mot dans file.txt")
    print("-------")

    print("Utilisation des commandes\n# = word\n* = digit\n@ = special characters\nExample : '#@****' = for each word in the word list add a special character and four digit")


def main(argv):
    if len(argv) == 1:
        print_help()
    if len(argv) > 2:
        if os.path.isfile(argv[1]):
            tab = open_file(argv[1])
        else:
            print("error give a valid name")
            return 0
        if '-t' in argv:
            tab = add_tranformation(tab)

        if '-c' in argv:
            index = sys.argv.index('-c')
            if index + 1 <= len(argv):
                tab = command(tab, argv[index + 1])
        if '-o' in argv:
            index = sys.argv.index('-o')
            if index + 1 <= len(argv):
                write_file(argv[index + 1], tab)
        if '-no_print' not in argv:
            print_tab(tab)


if __name__ == '__main__':
    # steps()
    main(sys.argv)
