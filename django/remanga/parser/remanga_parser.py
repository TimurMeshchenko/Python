import requests
import json
import urllib.request
import os 

class Remanga_parser():
    def __init__(self):
        self.json_data: str = str()    
        self.dir_name: str = str()        

    def print_catalog_titles(self) -> None:
        title_data_keys: list[str] = ['categories', 'genres', 'rus_name','dir','cover_high','type','total_views','total_votes',
                                      'avg_rating', 'issue_year']
        
        catalog_url: str = "https://api.remanga.org/api/search/catalog/?count=30&exclude_bookmarks=0&ordering=-rating&page=1"
        title_counts: int = 1
        
        for title_number in range(title_counts):
            self.db_request: str = str()
            self.request_categories_genres: str = str() 

            self.request_json_data(catalog_url)
            self.dir_name: str = self.json_data[title_number]['dir']

            self.add_db_reqeust(title_data_keys, title_number)
            self.get_title_page(title_number)

            self.print_title_creating_db_request()
   
    def request_json_data(self, url: str) -> None:
        response = requests.get(url)
        self.json_data = json.loads(response.text)['content']

    def add_db_reqeust(self, title_data_keys: list[str], title_number: int, count_string_data: int = 6) -> None:
        is_request_completed: bool = 'issue_year' in self.db_request

        for title_data_key_index in range(len(title_data_keys)):
            title_data_key: str = title_data_keys[title_data_key_index]     
            title_data: str = self.get_title_data(title_data_key, title_number, is_request_completed)

            if title_data_key in ['categories', 'genres']:
                self.add_to_request_all_categories_or_genres(title_data, title_data_key)            
            elif title_data_key_index < count_string_data: 
                self.add_data_quotes(title_data_key, title_data, is_request_completed)                           
            else:
                self.add_to_db_request(title_data_key, title_data)

            # if title_data_key == 'cover_high':
            #     self.download_cover(title_data)                

    def get_title_data(self, title_data_key: str, title_number: int, is_request_completed: bool) -> None:
        if is_request_completed:
            title_data = self.json_data[title_data_key]
        else:
            title_data = self.json_data[title_number][title_data_key]
        
        return title_data

    def add_to_request_all_categories_or_genres(self, title_data: str, title_data_key: str) -> None:
        for name_id in range(len(title_data)):
            self.request_categories_genres += f'Title.objects.get(dir_name="{self.dir_name}").\
{title_data_key}.add({title_data_key.title()}.objects.get(name="{title_data[name_id]["name"]}"))\n'
            
    def add_data_quotes(self, title_data_key: str, title_data: str, is_request_completed: bool) -> None:
        if is_request_completed:
            description: str = ''.join(title_data.splitlines())
            self.add_to_db_request(title_data_key, description, '"') 
        else:
            self.add_to_db_request(title_data_key, title_data, '"')

    def add_to_db_request(self, title_data_key: str, title_data: str, quotes: str = '') -> None:
        self.db_request += f'{title_data_key}={quotes}{title_data}{quotes},'

    def download_cover(self, title_data: str) -> None:
        url: str = f'https://remanga.org/media/{str(title_data)}'
        dir_name: str = url.rsplit('/')[-2]
        parent_dir: str = f'remanga/media/titles/{dir_name}/'
        file_name: str = url.rsplit('/')[-1]
        
        if not os.path.exists(parent_dir):
            os.mkdir(parent_dir)

        file_path: str = parent_dir + file_name
        urllib.request.urlretrieve(url, file_path)        

    def get_title_page(self, title_number: int) -> None:    
        title_page_data_keys: list[str] = ['description', 'count_bookmarks', 'count_chapters', 'count_rating']
        url: str = 'https://api.remanga.org/api/titles/' + str(self.dir_name)
        count_string_data: int = 1

        self.request_json_data(url)
        self.add_db_reqeust(title_page_data_keys, title_number, count_string_data)

    def print_title_creating_db_request(self) -> None:
        db_request: str = self.db_request.replace('dir', 'dir_name').replace('type', 'manga_type') \
        .replace('cover_high', 'img_url').replace('titles/', '')[:-1]

        # print(f'Title.objects.create({db_request})')    
        # print(self.request_categories_genres)
        # self.print_chapters()

    def print_chapters(self) -> None:
        branches_id: str = self.json_data['branches'][0]['id']   
        default_count_chapters_in_page = count_chapters_in_page = 40
        number_page: int = 1

        while (count_chapters_in_page == default_count_chapters_in_page):
            url: str = f'https://api.remanga.org/api/titles/chapters/?branch_id={branches_id}&ordering=-index&user_data=1&count=40&page={number_page}'
            
            self.request_json_data(url)

            count_chapters_in_page = len(self.json_data)
 
            for index in range(count_chapters_in_page):
                chapter: str = self.json_data[index]['chapter']
                tome: str = self.json_data[index]['tome']
            
                print(f'Title.objects.get(dir_name="{self.dir_name}").chapters.add(Chapters.objects.get_or_create(chapter="{chapter}", tome={tome})[0])')
            
            number_page += 1

if __name__ == "__main__":
    Remanga_parser().print_catalog_titles()     

