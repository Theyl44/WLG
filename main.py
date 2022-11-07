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
    for i in word_list:
        print(i)


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
                    new_word_list = mix_list(new_word_list, word_list)
                elif recc > 0:
                    for i in range(recc):
                        new_word_list = mix_list(new_word_list, word_list)
            if char == "*":
                if new_word_list == []:
                    new_word_list = digi_tab
                    recc -= 1
                if recc == 1:
                    new_word_list = add_number(new_word_list, 1)
                elif recc > 0:
                    new_word_list = add_number(new_word_list, recc)
            if char == "@":
                if new_word_list == []:
                    new_word_list = special_characters_tab
                    recc -= 1
                if recc == 1:
                    new_word_list = add_special_characters(new_word_list)
                elif recc > 0:
                    for i in range(recc - 1):
                        new_word_list = add_special_characters(new_word_list)
    return new_word_list


def steps():
    tab = open_file("file.txt")
    tab = command(tab, "##@@")
    # tab = add_special_characters(tab)
    # tab = add_number(tab, 2')
    # print_tab(tab)
    write_file("result.txt", tab)


if __name__ == '__main__':
    steps()
