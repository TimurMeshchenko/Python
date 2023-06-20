import requests
import json
import urllib.request
import os 

class Parser():
    
    def __init__(self):
        self.json_data = str()
        self.string_key_value = str()
        self.request_categories_genres = str()        
        self.dir_name = str()        

    def get_catalog_titles(self):
        columns = ['categories', 'genres', 'rus_name','dir','cover_high','type','total_views','total_votes','avg_rating',
                'issue_year']
        title_counts = 1

        for title_number in range(title_counts):
            url = "https://api.remanga.org/api/search/catalog/?count=30&exclude_bookmarks=0&ordering=-rating&page=1"
            self.request_get_json_data(url)

            self.add_db_reqeust(columns, title_number)
            # self.get_title_page(title_number)

        #     print('Title.objects.create({})'.format(self.string_key_value.replace('dir', 'dir_name').replace('type', 'manga_type')
        # .replace('cover_high', 'img_url').replace('titles/', '')[0:-1]))            
            # print(self.request_categories_genres)
            # self.get_chapters(dir_name)   
            self.__init__()         
 
    def request_get_json_data(self, new_url):
        response = requests.get(new_url)
        self.json_data = json.loads(response.text)['content']

    def add_db_reqeust(self, columns, title_number, condition = 6):
        for column_index in range(len(columns)):
            column = columns[column_index]
            is_first_call = 'issue_year' not in self.string_key_value

            def add_str_request(column_value, quotes = ''):
                self.string_key_value += '{}={quotes}{}{quotes},'.format(column, str(column_value), quotes=quotes)
                           
            if is_first_call:
                column_value = self.json_data[title_number][column]
                self.dir_name = self.json_data[title_number]['dir']
            else:
                column_value = self.json_data[column]

            def add_value_quotes():
                if is_first_call:
                    add_str_request(column_value, '"')
                else:
                    description = ''.join(column_value.splitlines())
                    add_str_request(description, '"') 

            if column_index < 2 and is_first_call:
                for name_id in range(len(column_value)):
                    self.request_categories_genres += 'Title.objects.get(dir_name="{}").{}.add({}.objects.get(name="{}"))\n'.format(
                        self.dir_name, column, column.title(), column_value[name_id]['name'])   
            elif column_index < condition: 
                add_value_quotes()                           
            else:
                add_str_request(column_value)

            if column == 'cover_high':
                self.download_cover(column_value)                

    def download_cover(self, column_value):
        url = 'https://remanga.org/media/{}'.format(str(column_value))
        dir_name = url.rsplit('/')[-2]
        parent_dir = 'remanga/media/titles/{}/'.format(dir_name) 
        file_name = url.rsplit('/')[-1]
        
        try:
            os.mkdir(parent_dir)
        except:
            pass

        file_path = parent_dir + file_name
        urllib.request.urlretrieve(url, file_path)        

    def get_title_page(self, title_number):    
        url = 'https://api.remanga.org/api/titles/' + str(self.dir_name)
        self.request_get_json_data(url)
        columns = ['description', 'count_bookmarks', 'count_chapters', 'count_rating']
        self.add_db_reqeust(columns, title_number, 1)

    def get_chapters(self, dir_name):
        branches_id = self.json_data['branches'][0]['id']   

        try:
            for number_page in range(1,1000):
                url = 'https://api.remanga.org/api/titles/chapters/?branch_id={}&ordering=-index&user_data=1&count=40&page={}'.format(branches_id, number_page)
                self.request_get_json_data(url)

                for index in range(40):
                    chapter = self.json_data[index]['chapter']
                    tome = self.json_data[index]['tome']

                    print('Title.objects.get(dir_name="{}").chapters.add(Chapters.objects.get_or_create(chapter="{}", tome={})[0])'
                          .format(dir_name, chapter, tome))
        except:
            pass

Parser().get_catalog_titles()     

    # print('q = Title.objects.get(dir_name="{}")'.format(str(dir_name)))                     
    # print('q.count_rating={}'.format(str(column_value['count_rating'])))
    # print('q.save()')

