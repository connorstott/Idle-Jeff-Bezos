PREFIX_NUMBERS = [1,  1000, 1000000, 1000000000, 1000000000000, 1000000000000000, 1000000000000000000]
PREFIXES =       ["", "K",  "M",     "B",        "T",           "P",              "E"]

def displayMoney(money: int) -> str:
    """changes the money into a string <1000 w/ a prefix"""
    display_money = str(round(money, 2))

    # go through the list until you reach a number > itself, and use the previous prefix
    for i in range(len(PREFIX_NUMBERS)):
        if money < PREFIX_NUMBERS[i] and money > 1:
            display_money = str(round(money/PREFIX_NUMBERS[i-1], 2))
            display_money_prefix = PREFIXES[i-1]
            break
        else:
            display_money_prefix = ""

    # Consistent decimal count
    decimal_count = 0
    on_decimals = False
    for character in display_money:
        if character == ".":
            on_decimals = True
        elif on_decimals: # elif as you don't want to count a decimal when you're on the .
            decimal_count += 1
    if decimal_count == 0:
        display_money += "."
    while decimal_count < 2:
        display_money += "0"
        decimal_count += 1
    
    display_money = display_money + display_money_prefix
    return display_money