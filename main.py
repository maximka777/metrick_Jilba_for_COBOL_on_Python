# -*- coding: utf-8 -*-

import pickle, re;

PATH_OPERATORS_DB = r"operators.db"
ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def read_operators_list():
    try:
        f = open(PATH_OPERATORS_DB, 'rb')
        operator_list = pickle.load(f)
        f.close()
    except:
        operator_list = []
    return operator_list

def write_operators_list(operator_list):
    try:
        f = open(PATH_OPERATORS_DB, 'wb')
        pickle.dump(operator_list, f)
        f.close()
    except:
        print("Не удалось записать:)")

def count_conditional_constructions(code):
    n_conditional_constructions = 0
    conditional_constructions = ['IF', 'EVALUATE']
    #для операторов символьных
    entries = 0
    for operator in conditional_constructions:
        print re.compile('\s%s\s' % operator, re.IGNORECASE).findall(code)
        entries += len(re.compile('\s%s\s' %operator, re.IGNORECASE).findall(code))
    n_conditional_constructions += entries
    return n_conditional_constructions

def count_n_operators(code):
    n_operators = 0
    operators_list = read_operators_list()
    #для операторов символьных
    entries = 0
    for operator in operators_list:
         if operator[0] not in ALPHABET:
            print re.compile('\%s' % operator).findall(code)
            entries += len(re.compile('\%s' % operator).findall(code))
    #для операторов (слова)
    for operator in operators_list:
        if operator[0] in ALPHABET:
            print re.compile('\s%s\s' % operator).findall(code)
            entries += len(re.compile('%s' %operator, re.IGNORECASE).findall(code))
    n_operators += entries
    return n_operators

def check_on_max_nesting(max_nesting, stack_of_conditions):
    if len(stack_of_conditions) > max_nesting:
        return len(stack_of_conditions)
    return max_nesting

def count_max_nesting(code):
    max_nesting = 0
    stack_of_conditions = []
    i = code.find('PROCEDURE DIVISION.')
    while i < len(code):
        if code[i:i+len(' evaluate ')].lower() == ' evaluate ':
            stack_of_conditions.append('1')
            max_nesting = check_on_max_nesting(max_nesting, stack_of_conditions)
            i += len(' evaluate ')
        elif code[i:i+len(' if ')].lower() == ' if ':
            stack_of_conditions.append('1')
            max_nesting = check_on_max_nesting(max_nesting, stack_of_conditions)
            i += len(' if ')
        elif code[i:i+len(' end-if')].lower() == ' end-if':
            if len(stack_of_conditions) > 0:
                stack_of_conditions.pop()
            i += len(' end-if')
        elif code[i:i+len(' end-evaluate')].lower() == ' end-evaluate':
            if len(stack_of_conditions) > 0:
                stack_of_conditions.pop()
            i += len(' end-evaluate')
        elif code[i:i+len('.')] == '.':
            if len(stack_of_conditions) > 0:
                stack_of_conditions.pop()
            i += len('.')
        else:
            i += 1
    return max_nesting

def analize_code(code):
    CL = count_conditional_constructions(code)
    n_operators = count_n_operators(code)
    print("n operators: " + str(n_operators))
    max_nesting = count_max_nesting(code)

    try:
        cl = float(CL) / float(n_operators)
    except:
        cl = None
    print(CL, cl, max_nesting)
    print("Кол-во условных конструкций = " + str(CL))
    print("Отношение кол-ва условных конструкций к кол-ву всех операторов = " + str(cl))
    print("Максимальная вложенность = " + str(max_nesting))




def open_file():
    file_path = raw_input("Введите путь к файлу: ")
    try:
        f = open(file_path, "rt")
    except:
        f = None
    return f

def get_code():
        f = open_file()
        if f:
            code = f.read()
            f.close()
        else:
            code = None

        return code


def show_db_operators():
        operators_list = read_operators_list()
        print('Список операторов: \n')
        print(operators_list)

def del_operators_from_db():
    del_operators = (str(raw_input("Удаляемый(е) оператор(ы)(через пробел, если их несколько): "))).split()
    operators_list = read_operators_list()
    for del_operator in del_operators:
        if operators_list:
            if del_operator in operators_list:
                operators_list.remove(del_operator)
    write_operators_list(operators_list)

def add_operators_to_db():
    new_operators = (str(raw_input("Новый(е) оператор(ы)(через пробел, если их несколько): "))).split()
    operators_list = read_operators_list()
    for new_operator in new_operators:
        if new_operator not in operators_list:
            operators_list.append(new_operator)
    write_operators_list(operators_list)




def check_choice(choice, code):
    checking_result = True
    if choice == "1":
        if code:
            analize_code(code)

        else:
            print("Файл с кодом не загружен...")
    elif choice == "2":
        code = get_code()
    elif choice == "3":
        if code:
            print(code)
        else:
            print("Файл с кодом не загружен...")
    elif choice == "0":
        print("Пока...")
    elif choice == "4":
        add_operators_to_db()
    elif choice == "5":
        del_operators_from_db()
    elif choice == "6":
        show_db_operators()
    else:
        checking_result = False
    return checking_result, code

def main():
    choice = None
    code = None
    while choice != "0":
        print("""
              1 - Анализ кода(COBOL)
              2 - Открыть файл с кодом
              3 - Просмотреть код
              4 - add operator
              5 - remove operator
              6 - show operators
              0 - Выйти
              """)
        choice = raw_input("Ваш выбор: ")
        checking_result, code = check_choice(choice, code)
        if not checking_result:
            print("Неправильный ввод...")

if __name__ == "__main__":
    main()