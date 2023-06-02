import requests
import json

class Parser():
    
    def __init__(self):
        self.json_data = str()

    def get_catalog_titles(self):
        columns = ['rus_name','dir','cover_high','type','total_views','total_votes','avg_rating',
                'issue_year','categories', 'genres']
        
        for title_number in range(1):
            string_key_value = str()
            request_categories_genres = str()

            url = "https://api.remanga.org/api/search/catalog/?count=30&exclude_bookmarks=0&ordering=-rating&page=1"
            self.request_get_json_data(url)

            for column in columns:
                column_value = self.json_data['content'][title_number][column]
                dir_name = self.json_data['content'][title_number]['dir']

                match column:

                    case 'categories' | 'genres':
                        for name_id in range(len(column_value)):
                            request_categories_genres += 'Title.objects.get(dir_name="{}").{}.add({}.objects.get(name="{}"))\n'.format(
                                dir_name, column, column.title(), column_value[name_id]['name'])
                            
                    case 'rus_name' | 'dir' | 'type' | 'cover_high':
                        string_key_value += '{}="{}",'.format(column, str(column_value))       
                        
                    case _:
                        string_key_value += '{}={},'.format(column, str(column_value))

        #     print('Title.objects.create(' + self.get_title_page(dir_name, string_key_value).replace('dir', 'dir_name').replace('type', 'manga_type')
        # .replace('cover_high', 'img_url').replace('titles/', '')[0:-1] + ')')
            # print(request_categories_genres)
           
            self.get_title_page(dir_name, string_key_value) # without print title.objects.create
            self.get_chapters(dir_name)            

    def request_get_json_data(self, new_url):
        response = requests.get(new_url)
        self.json_data = json.loads(response.text)

    def get_title_page(self, dir_name, string_key_value):    
        url = 'https://api.remanga.org/api/titles/' + str(dir_name)
        self.request_get_json_data(url)
        columns = ['description', 'count_bookmarks', 'count_chapters', 'count_rating']

        for column in columns:
            column_value = self.json_data['content'][column]

            if column == 'description':
                desc = ''.join(column_value.splitlines())
                string_key_value += '{}="{}",'.format(column, desc)             
            else:
                string_key_value += '{}={},'.format(column, str(column_value))
        
        return string_key_value

    def get_chapters(self, dir_name):
        branches_id = self.json_data['content']['branches'][0]['id']   

        try:
            for number_page in range(1,1000):
                url = 'https://api.remanga.org/api/titles/chapters/?branch_id={}&ordering=-index&user_data=1&count=40&page={}'.format(branches_id, number_page)
                self.request_get_json_data(url)

                for index in range(40):
                    chapter = self.json_data['content'][index]['chapter']
                    tome = self.json_data['content'][index]['tome']

                    print('Title.objects.get(dir_name="{}").chapters.add(Chapters.objects.get_or_create(chapter="{}", tome={})[0])'
                          .format(dir_name, chapter, tome))
        except:
            pass


class main:
    parser = Parser()
    parser.get_catalog_titles()     

if __name__ == '__main__':
    main()


    # print('q = Title.objects.get(dir_name="{}")'.format(str(dir_name)))                     
    # print('q.count_rating={}'.format(str(column_value['count_rating'])))
    # print('q.save()')


# def create_genres_table():
#     all_genres = '<div tabindex="-1" aria-expanded="true" role="list" class="jsx-f6904a6ed8e0085 jsx-2945355907 select-dropdown"><span role="option" aria-selected="false" aria-label="Боевые искусства" tabindex="-1" class="jsx-1b57bf17c694e838 ">Боевые искусства</span><span role="option" aria-selected="false" aria-label="Гарем" tabindex="-1" class="jsx-1b57bf17c694e838 ">Гарем</span><span role="option" aria-selected="false" aria-label="Гендерная интрига" tabindex="-1" class="jsx-1b57bf17c694e838 ">Гендерная интрига</span><span role="option" aria-selected="false" aria-label="Героическое фэнтези" tabindex="-1" class="jsx-1b57bf17c694e838 ">Героическое фэнтези</span><span role="option" aria-selected="false" aria-label="Детектив" tabindex="-1" class="jsx-1b57bf17c694e838 ">Детектив</span><span role="option" aria-selected="false" aria-label="Дзёсэй" tabindex="-1" class="jsx-1b57bf17c694e838 ">Дзёсэй</span><span role="option" aria-selected="false" aria-label="Додзинси" tabindex="-1" class="jsx-1b57bf17c694e838 ">Додзинси</span><span role="option" aria-selected="false" aria-label="Драма" tabindex="-1" class="jsx-1b57bf17c694e838 ">Драма</span><span role="option" aria-selected="false" aria-label="История" tabindex="-1" class="jsx-1b57bf17c694e838 ">История</span><span role="option" aria-selected="false" aria-label="Киберпанк" tabindex="-1" class="jsx-1b57bf17c694e838 ">Киберпанк</span><span role="option" aria-selected="false" aria-label="Кодомо" tabindex="-1" class="jsx-1b57bf17c694e838 ">Кодомо</span><span role="option" aria-selected="false" aria-label="Комедия" tabindex="-1" class="jsx-1b57bf17c694e838 ">Комедия</span><span role="option" aria-selected="false" aria-label="Махо-сёдзё" tabindex="-1" class="jsx-1b57bf17c694e838 ">Махо-сёдзё</span><span role="option" aria-selected="false" aria-label="Меха" tabindex="-1" class="jsx-1b57bf17c694e838 ">Меха</span><span role="option" aria-selected="false" aria-label="Мистика" tabindex="-1" class="jsx-1b57bf17c694e838 ">Мистика</span><span role="option" aria-selected="false" aria-label="Мурим" tabindex="-1" class="jsx-1b57bf17c694e838 ">Мурим</span><span role="option" aria-selected="false" aria-label="Научная фантастика" tabindex="-1" class="jsx-1b57bf17c694e838 ">Научная фантастика</span><span role="option" aria-selected="false" aria-label="Повседневность" tabindex="-1" class="jsx-1b57bf17c694e838 ">Повседневность</span><span role="option" aria-selected="false" aria-label="Постапокалиптика" tabindex="-1" class="jsx-1b57bf17c694e838 ">Постапокалиптика</span><span role="option" aria-selected="false" aria-label="Приключения" tabindex="-1" class="jsx-1b57bf17c694e838 ">Приключения</span><span role="option" aria-selected="false" aria-label="Психология" tabindex="-1" class="jsx-1b57bf17c694e838 ">Психология</span><span role="option" aria-selected="false" aria-label="Романтика" tabindex="-1" class="jsx-1b57bf17c694e838 ">Романтика</span><span role="option" aria-selected="false" aria-label="Сверхъестественное" tabindex="-1" class="jsx-1b57bf17c694e838 ">Сверхъестественное</span><span role="option" aria-selected="false" aria-label="Сёдзё" tabindex="-1" class="jsx-1b57bf17c694e838 ">Сёдзё</span><span role="option" aria-selected="false" aria-label="Сёдзё-ай" tabindex="-1" class="jsx-1b57bf17c694e838 ">Сёдзё-ай</span><span role="option" aria-selected="false" aria-label="Сёнэн" tabindex="-1" class="jsx-1b57bf17c694e838 ">Сёнэн</span><span role="option" aria-selected="false" aria-label="Сёнэн-ай" tabindex="-1" class="jsx-1b57bf17c694e838 ">Сёнэн-ай</span><span role="option" aria-selected="false" aria-label="Спорт" tabindex="-1" class="jsx-1b57bf17c694e838 ">Спорт</span><span role="option" aria-selected="false" aria-label="Сэйнэн" tabindex="-1" class="jsx-1b57bf17c694e838 ">Сэйнэн</span><span role="option" aria-selected="false" aria-label="Трагедия" tabindex="-1" class="jsx-1b57bf17c694e838 ">Трагедия</span><span role="option" aria-selected="false" aria-label="Триллер" tabindex="-1" class="jsx-1b57bf17c694e838 ">Триллер</span><span role="option" aria-selected="false" aria-label="Ужасы" tabindex="-1" class="jsx-1b57bf17c694e838 ">Ужасы</span><span role="option" aria-selected="false" aria-label="Фантастика" tabindex="-1" class="jsx-1b57bf17c694e838 ">Фантастика</span><span role="option" aria-selected="false" aria-label="Фэнтези" tabindex="-1" class="jsx-1b57bf17c694e838 ">Фэнтези</span><span role="option" aria-selected="false" aria-label="Школьная жизнь" tabindex="-1" class="jsx-1b57bf17c694e838 ">Школьная жизнь</span><span role="option" aria-selected="false" aria-label="Экшен" tabindex="-1" class="jsx-1b57bf17c694e838 ">Экшен</span><span role="option" aria-selected="false" aria-label="Элементы юмора" tabindex="-1" class="jsx-1b57bf17c694e838 ">Элементы юмора</span><span role="option" aria-selected="false" aria-label="Этти" tabindex="-1" class="jsx-1b57bf17c694e838 ">Этти</span><span role="option" aria-selected="false" aria-label="Юри" tabindex="-1" class="jsx-1b57bf17c694e838 ">Юри</span><span role="option" aria-selected="false" aria-label="Яой" tabindex="-1" class="jsx-1b57bf17c694e838 ">Яой</span></div>'
#     all_genres = all_genres.split('aria-label=')

#     for i in range(1, len(all_genres)):
#         print('Genres.objects.create(name=' + all_genres[i][:all_genres[i].find(' tab')] + ')')

# def create_categories_table():
#     all_categories = '<div tabindex="-1" aria-expanded="true" role="list" class="jsx-f6904a6ed8e0085 jsx-2945355907 select-dropdown"><span role="option" aria-selected="false" aria-label="Веб" tabindex="-1" class="jsx-1b57bf17c694e838 ">Веб</span><span role="option" aria-selected="false" aria-label="В цвете" tabindex="-1" class="jsx-1b57bf17c694e838 ">В цвете</span><span role="option" aria-selected="false" aria-label="Ёнкома" tabindex="-1" class="jsx-1b57bf17c694e838 ">Ёнкома</span><span role="option" aria-selected="false" aria-label="Сборник" tabindex="-1" class="jsx-1b57bf17c694e838 ">Сборник</span><span role="option" aria-selected="false" aria-label="Сингл" tabindex="-1" class="jsx-1b57bf17c694e838 ">Сингл</span><span role="option" aria-selected="false" aria-label="Реинкарнация" tabindex="-1" class="jsx-1b57bf17c694e838 ">Реинкарнация</span><span role="option" aria-selected="false" aria-label="Зомби" tabindex="-1" class="jsx-1b57bf17c694e838 ">Зомби</span><span role="option" aria-selected="false" aria-label="Демоны" tabindex="-1" class="jsx-1b57bf17c694e838 ">Демоны</span><span role="option" aria-selected="false" aria-label="Кулинария" tabindex="-1" class="jsx-1b57bf17c694e838 ">Кулинария</span><span role="option" aria-selected="false" aria-label="Медицина" tabindex="-1" class="jsx-1b57bf17c694e838 ">Медицина</span><span role="option" aria-selected="false" aria-label="Культивация" tabindex="-1" class="jsx-1b57bf17c694e838 ">Культивация</span><span role="option" aria-selected="false" aria-label="Зверолюди" tabindex="-1" class="jsx-1b57bf17c694e838 ">Зверолюди</span><span role="option" aria-selected="false" aria-label="Хикикомори" tabindex="-1" class="jsx-1b57bf17c694e838 ">Хикикомори</span><span role="option" aria-selected="false" aria-label="Магия" tabindex="-1" class="jsx-1b57bf17c694e838 ">Магия</span><span role="option" aria-selected="false" aria-label="Горничные" tabindex="-1" class="jsx-1b57bf17c694e838 ">Горничные</span><span role="option" aria-selected="false" aria-label="Средневековье" tabindex="-1" class="jsx-1b57bf17c694e838 ">Средневековье</span><span role="option" aria-selected="false" aria-label="Антигерой" tabindex="-1" class="jsx-1b57bf17c694e838 ">Антигерой</span><span role="option" aria-selected="false" aria-label="Гяру" tabindex="-1" class="jsx-1b57bf17c694e838 ">Гяру</span><span role="option" aria-selected="false" aria-label="Ниндзя" tabindex="-1" class="jsx-1b57bf17c694e838 ">Ниндзя</span><span role="option" aria-selected="false" aria-label="Офисные работники" tabindex="-1" class="jsx-1b57bf17c694e838 ">Офисные работники</span><span role="option" aria-selected="false" aria-label="Полиция" tabindex="-1" class="jsx-1b57bf17c694e838 ">Полиция</span><span role="option" aria-selected="false" aria-label="Самураи" tabindex="-1" class="jsx-1b57bf17c694e838 ">Самураи</span><span role="option" aria-selected="false" aria-label="Традиционные игры" tabindex="-1" class="jsx-1b57bf17c694e838 ">Традиционные игры</span><span role="option" aria-selected="false" aria-label="Видеоигры" tabindex="-1" class="jsx-1b57bf17c694e838 ">Видеоигры</span><span role="option" aria-selected="false" aria-label="Криминал" tabindex="-1" class="jsx-1b57bf17c694e838 ">Криминал</span><span role="option" aria-selected="false" aria-label="Монстры" tabindex="-1" class="jsx-1b57bf17c694e838 ">Монстры</span><span role="option" aria-selected="false" aria-label="Музыка" tabindex="-1" class="jsx-1b57bf17c694e838 ">Музыка</span><span role="option" aria-selected="false" aria-label="Обратный Гарем" tabindex="-1" class="jsx-1b57bf17c694e838 ">Обратный Гарем</span><span role="option" aria-selected="false" aria-label="Выживание" tabindex="-1" class="jsx-1b57bf17c694e838 ">Выживание</span><span role="option" aria-selected="false" aria-label="Путешествия во времени" tabindex="-1" class="jsx-1b57bf17c694e838 ">Путешествия во времени</span><span role="option" aria-selected="false" aria-label="Боги" tabindex="-1" class="jsx-1b57bf17c694e838 ">Боги</span><span role="option" aria-selected="false" aria-label="Алхимия" tabindex="-1" class="jsx-1b57bf17c694e838 ">Алхимия</span><span role="option" aria-selected="false" aria-label="Ангелы" tabindex="-1" class="jsx-1b57bf17c694e838 ">Ангелы</span><span role="option" aria-selected="false" aria-label="Антиутопия" tabindex="-1" class="jsx-1b57bf17c694e838 ">Антиутопия</span><span role="option" aria-selected="false" aria-label="Апокалипсис" tabindex="-1" class="jsx-1b57bf17c694e838 ">Апокалипсис</span><span role="option" aria-selected="false" aria-label="Армия" tabindex="-1" class="jsx-1b57bf17c694e838 ">Армия</span><span role="option" aria-selected="false" aria-label="Артефакты" tabindex="-1" class="jsx-1b57bf17c694e838 ">Артефакты</span><span role="option" aria-selected="false" aria-label="Борьба за власть" tabindex="-1" class="jsx-1b57bf17c694e838 ">Борьба за власть</span><span role="option" aria-selected="false" aria-label="Будущее" tabindex="-1" class="jsx-1b57bf17c694e838 ">Будущее</span><span role="option" aria-selected="false" aria-label="Вестерн" tabindex="-1" class="jsx-1b57bf17c694e838 ">Вестерн</span><span role="option" aria-selected="false" aria-label="Владыка демонов" tabindex="-1" class="jsx-1b57bf17c694e838 ">Владыка демонов</span><span role="option" aria-selected="false" aria-label="Волшебные существа" tabindex="-1" class="jsx-1b57bf17c694e838 ">Волшебные существа</span><span role="option" aria-selected="false" aria-label="Воспоминания из другого мира" tabindex="-1" class="jsx-1b57bf17c694e838 ">Воспоминания из другого мира</span><span role="option" aria-selected="false" aria-label="Геймеры" tabindex="-1" class="jsx-1b57bf17c694e838 ">Геймеры</span><span role="option" aria-selected="false" aria-label="Гильдии" tabindex="-1" class="jsx-1b57bf17c694e838 ">Гильдии</span><span role="option" aria-selected="false" aria-label="ГГ женщина" tabindex="-1" class="jsx-1b57bf17c694e838 ">ГГ женщина</span><span role="option" aria-selected="false" aria-label="ГГ мужчина" tabindex="-1" class="jsx-1b57bf17c694e838 ">ГГ мужчина</span><span role="option" aria-selected="false" aria-label="Дружба" tabindex="-1" class="jsx-1b57bf17c694e838 ">Дружба</span><span role="option" aria-selected="false" aria-label="Ранги силы" tabindex="-1" class="jsx-1b57bf17c694e838 ">Ранги силы</span><span role="option" aria-selected="false" aria-label="Жестокий мир" tabindex="-1" class="jsx-1b57bf17c694e838 ">Жестокий мир</span><span role="option" aria-selected="false" aria-label="Животные компаньоны" tabindex="-1" class="jsx-1b57bf17c694e838 ">Животные компаньоны</span><span role="option" aria-selected="false" aria-label="Игровые элементы" tabindex="-1" class="jsx-1b57bf17c694e838 ">Игровые элементы</span><span role="option" aria-selected="false" aria-label="Космос" tabindex="-1" class="jsx-1b57bf17c694e838 ">Космос</span><span role="option" aria-selected="false" aria-label="Магическая академия" tabindex="-1" class="jsx-1b57bf17c694e838 ">Магическая академия</span><span role="option" aria-selected="false" aria-label="Месть" tabindex="-1" class="jsx-1b57bf17c694e838 ">Месть</span><span role="option" aria-selected="false" aria-label="Навыки" tabindex="-1" class="jsx-1b57bf17c694e838 ">Навыки</span><span role="option" aria-selected="false" aria-label="Наёмники" tabindex="-1" class="jsx-1b57bf17c694e838 ">Наёмники</span><span role="option" aria-selected="false" aria-label="Насилие / жестокость" tabindex="-1" class="jsx-1b57bf17c694e838 ">Насилие / жестокость</span><span role="option" aria-selected="false" aria-label="Нежить" tabindex="-1" class="jsx-1b57bf17c694e838 ">Нежить</span><span role="option" aria-selected="false" aria-label="Пародия" tabindex="-1" class="jsx-1b57bf17c694e838 ">Пародия</span><span role="option" aria-selected="false" aria-label="Подземелья" tabindex="-1" class="jsx-1b57bf17c694e838 ">Подземелья</span><span role="option" aria-selected="false" aria-label="Политика" tabindex="-1" class="jsx-1b57bf17c694e838 ">Политика</span><span role="option" aria-selected="false" aria-label="Разумные расы" tabindex="-1" class="jsx-1b57bf17c694e838 ">Разумные расы</span><span role="option" aria-selected="false" aria-label="Роботы" tabindex="-1" class="jsx-1b57bf17c694e838 ">Роботы</span><span role="option" aria-selected="false" aria-label="Рыцари" tabindex="-1" class="jsx-1b57bf17c694e838 ">Рыцари</span><span role="option" aria-selected="false" aria-label="Система" tabindex="-1" class="jsx-1b57bf17c694e838 ">Система</span><span role="option" aria-selected="false" aria-label="Стимпанк" tabindex="-1" class="jsx-1b57bf17c694e838 ">Стимпанк</span><span role="option" aria-selected="false" aria-label="Скрытие личности" tabindex="-1" class="jsx-1b57bf17c694e838 ">Скрытие личности</span><span role="option" aria-selected="false" aria-label="Спасение мира" tabindex="-1" class="jsx-1b57bf17c694e838 ">Спасение мира</span><span role="option" aria-selected="false" aria-label="Супергерои" tabindex="-1" class="jsx-1b57bf17c694e838 ">Супергерои</span><span role="option" aria-selected="false" aria-label="Учитель / ученик" tabindex="-1" class="jsx-1b57bf17c694e838 ">Учитель / ученик</span><span role="option" aria-selected="false" aria-label="Шантаж" tabindex="-1" class="jsx-1b57bf17c694e838 ">Шантаж</span><span role="option" aria-selected="false" aria-label="Лоли" tabindex="-1" class="jsx-1b57bf17c694e838 ">Лоли</span><span role="option" aria-selected="false" aria-label="Тупой ГГ" tabindex="-1" class="jsx-1b57bf17c694e838 ">Тупой ГГ</span><span role="option" aria-selected="false" aria-label="ГГ имба" tabindex="-1" class="jsx-1b57bf17c694e838 ">ГГ имба</span><span role="option" aria-selected="false" aria-label="Умный ГГ" tabindex="-1" class="jsx-1b57bf17c694e838 ">Умный ГГ</span><span role="option" aria-selected="false" aria-label="Управление территорией" tabindex="-1" class="jsx-1b57bf17c694e838 ">Управление территорией</span><span role="option" aria-selected="false" aria-label="Исекай" tabindex="-1" class="jsx-1b57bf17c694e838 ">Исекай</span><span role="option" aria-selected="false" aria-label="Аристократия" tabindex="-1" class="jsx-1b57bf17c694e838 ">Аристократия</span><span role="option" aria-selected="false" aria-label="Амнезия" tabindex="-1" class="jsx-1b57bf17c694e838 ">Амнезия</span><span role="option" aria-selected="false" aria-label="Бои на мечах" tabindex="-1" class="jsx-1b57bf17c694e838 ">Бои на мечах</span><span role="option" aria-selected="false" aria-label="ГГ не человек" tabindex="-1" class="jsx-1b57bf17c694e838 ">ГГ не человек</span><span role="option" aria-selected="false" aria-label="Упоротость" tabindex="-1" class="jsx-1b57bf17c694e838 ">Упоротость</span><span role="option" aria-selected="false" aria-label="Грузовик-сан" tabindex="-1" class="jsx-1b57bf17c694e838 ">Грузовик-сан</span><span role="option" aria-selected="false" aria-label="Учебное заведение" tabindex="-1" class="jsx-1b57bf17c694e838 ">Учебное заведение</span></div>'
#     all_categories = all_categories.split('aria-label=')

#     for i in range(1, len(all_categories)):
#         print('Categories.objects.create(name=' + all_categories[i][:all_categories[i].find(' tab')] + ')')


