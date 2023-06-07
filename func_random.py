def find_count_dice(message: str, dice):
    try:
        lang = find_count_lang(message)
        dot = message.find(lang+str(dice))
        try:
            count = int(message[dot-2:dot])
        except:
            try:
                count = int(message[dot-1:dot])
            except:
                count = 1
        return count
    except:
        pass


def find_count_lang(message: str):
    for char in message:
        if char == "d" or char == "к":
            return char


def find_dice(text):
    i = 100
    while i != 0:
        if text.find('к' + str(i)) != -1 or text.find('d' + str(i)) != -1:
            return i
        i = i - 1