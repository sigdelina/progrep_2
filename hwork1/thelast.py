import random

def openFile():                                                                 #эта функция запрашивает у пользователя номер темы и после прочитывает тхт-файлы
    a = input('Добро пожаловать в игру!\n\nВам предлагается на выбор три темы:\
              \n1. Еда\n2. Реки России\n3. Математические термины\n\
              \nВыберите одну из них!Укажите цифру выбранной темы: ')
    while a != '1' and a != '2' and a != '3':
        a = input('Указанный вами номер отсутсвует или набран неправильно,'
                    'выбирите тему еще раз: ')
        if a == '1' or a == '2' or a == '3':
            break
    if a == '1':
        with open('еда.txt', encoding='utf-8') as file:
            t = file.read()
    elif a == '2':
        with open('Реки России.txt', encoding='utf-8') as file:
            t = file.read()
    elif a == '3':
        with open('Математические термины.txt', encoding='utf-8') as file:
            t = file.read()
    return t

def spisok(t):                                                                  #функция делает список из тхт-файла, в котором хранятся слова, соответсвующие выбранной теме
    sp = t.strip().split('\n')
    return sp

def sluchano(sp):                                                               #функция выбирает случайное слово из списка и приводит все буквы к нижнему регистру
    rand = random.choice(sp).lower()
    #print(rand)
    return rand

def oshibki():                                                                  #в функции хранятся изменения в рисунке виселицы в зависмости от количесвтва ошибок
    ne_verno = ['_________\n|/\n|\n|\n|\n|\n|\n|\n|\ \n|_\___________________'
                                                    '\n//////////////////////',
                '_________\n|/\n|\n|\n|\n|\n|\n|\n|\   ______\n|_\__|____|'
                                         '___________\n//////////////////////',
                '_________\n|/      |\n|       |\n|\n|\n|\n|\n|\n|\   ______\n'
                              '|_\__|____|___________\n//////////////////////',
                '_________\n|/      |\n|       |\n|       O\n|\n|\n|\n|\n|\  '
                     ' ______\n|_\__|____|___________\n//////////////////////',
                '_________\n|/      |\n|       |\n|       O\n|'
                                '       *\n|       |\n|\n|\n|\   ______\n|_\__'
                                   '|____|___________\n//////////////////////',
                '_________\n|/      |\n|       |\n|       O\n|      /'
                '*\ \n|       |\n|\n|\n|\   ______\n|_\__|____|'
                                         '___________\n//////////////////////',
                '_________\n|/      |\n|       |\n|       O\n|      /*\ \n|   '
                              '    |\n|      / \ \n|\n|\   ______\n|_\__|____|'
                                         '___________\n//////////////////////',
                '_________\n|/      |\n|       |\n|      >_<\n|      /*\ \n|'
                              '       |\n|      / \ \n|\n|\   ______\n|_\__|'
                                    '____|___________\n//////////////////////']
    return ne_verno
    
def spisForLet():                                                               #функция создает список для букв в выбранном слове
    spisok_bukv = []
    return spisok_bukv

def wrongLet():                                                                 # в функции лежит список для букв, введнных пользователем,но не входящих в рандомное слово
    wrong_bukv = []
    return wrong_bukv

def kolichestvoOshibok():                                                       #количесвто ошибок, которые может допустить пользователь
    oshibki = 8
    return  oshibki

def skl(oshibki):
    sklonenie = ['попыток', 'попыток', 'попыток',
                 'попыток', 'попытки', 'попытки',
                            'попытки', 'попытка']
    return sklonenie

def uslovie(rand, spisok_bukv, ne_verno, wrong_bukv, oshibki, sklonenie):       #функция запрашивает у пользователя букву, приводит ее к нижнему регистру и, если такая существует, меняет _ на букву 
    while len(wrong_bukv) != 8:                                                 #цикл на одну попытку для пользователя
        stro = ''                                                               #строчка, в которую будут записываться _
        for letters in rand:                                                    # для рандомного слова создается строчка из _, в которой по ходу выполнения цикла будет выводиться либо буква,либо _ 
            if letters not in spisok_bukv:
                stro += '_ '
            else:
                stro += letters + ' '
        print('\n\nУ Вас есть ', oshibki, sklonenie[len(wrong_bukv)],          #попытки = количество допустимых ошибок
                   ', чтобы угадать слово из ', len(rand), ' букв\n',
                                                  '\n\t', stro, '\n')
        let = input('Введите букву) если такая буква есть в слове,'
                    'то _ заменится на нее: ').lower()
        if let in spisok_bukv and len(let) == 1:                               #если буква уже есть в списке верных букв, то она отгадана, если пользователь ввел уже имеющуюся букву больше 1 раза это ОШИБКА!
            wrong_bukv.append(let)
            oshibki -= 1
           # print(oshibki)
            print('Буква', let, 'уже отгадна')
        else:                                                                  #ситуация, когда верная буква введена первый раз
            for letters in rand:
                if let == letters:
                    spisok_bukv.append(let)
        #print(spisok_bukv)
        if let not in spisok_bukv:                                              #рассматривается введенный символ,если его нет в слове
            wrong_bukv.append(let)
            print('Вы не угадали букву')
            #print(wrong_bukv)
            oshibki -= 1
            #print(oshibki)
            if let not in 'бвгдеёжзийклмнопрстуфхцчшщъыьэюя' and len(let) == 1: # ниже рассматриваются ситуации, когда вводится буква не заданного алфавита или сочетание (0) символов
                if let in 'abcdefghijklmnopqrstuvxyz':
                    print('Error: Введите киррилический символ')
                else:
                    print('Error: Введенный Вами символ не буква')
            else:
                if len(let) > 0:
                    print('Error: Количество введенных символов больше одного')
                if let == '':
                    print('Error: Количество введенных символов меньше одного')
        if len(wrong_bukv) > 0:                                                #выводится рисунок в зависимости от длины списка из неправильных букв
            print(ne_verno[len(wrong_bukv)-1])
        if len(wrong_bukv) == 8 or len(spisok_bukv) == len(rand):              #условия, при которых цикл завершается - либо слово угадано,либо закончились попытки
            break
        continue
    return wrong_bukv

def itog(wrong_bukv, rand):                                                     #функция определяет, было ли угадано слово, и выводит его
    if len(wrong_bukv) == 8:
        it = "\nВы проиграли!(\n"
    else:
        it = '\nВы выиграли!\n'
    zagadannoe = str(it) + 'Было загаданно слово:'
    print(zagadannoe, rand)

def returnF(zagadannoe):                                                        #функция спрашивает у пользователя,хочет ли он сыграть еще раз, если да - игра продолжается, если нет - просиходит выход из программы
    again = input('\n\nЧтобы сыграть еще раз введите Да,'
                              'чтобы выйти введите Нет: ')
    if again.lower() == 'да':
        main()
    else:
        exit(0)
        
def main():                                                                    #здесь лежат все функции
    spi = spisok(openFile())
    ran = sluchano(spi)
    letter_spi = spisForLet()
    wrong_letters = wrongLet()
    os = oshibki()
    kol_vo = kolichestvoOshibok()
    forma_slov = skl(kol_vo)
    tema = uslovie(ran, letter_spi, os, wrong_letters, kol_vo, forma_slov)
    final = itog(tema, ran)
    ret = returnF(final)
    
main()
