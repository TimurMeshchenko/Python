from remanga_parser import *

class Test_Remanga_parser():
    remanga_parser = Remanga_parser()

    def test_request_json_data(self):
        catalog_url: str = "https://api.remanga.org/api/search/catalog/?count=30&exclude_bookmarks=0&ordering=-rating&page=1"
        
        self.remanga_parser.json_data = str()
        self.remanga_parser.request_json_data(catalog_url)

        assert len(self.remanga_parser.json_data) > 0
    
    def test_print_catalog_titles(self) -> None:
        title_data_keys: list[str] = ['rus_name','dir','cover_high','type','total_views','total_votes', 'avg_rating', 
                                      'issue_year', 'description', 'count_bookmarks', 'count_chapters', 'count_rating']
        
        self.remanga_parser.print_catalog_titles()
        
        for title_data_key in title_data_keys:
            assert title_data_key in self.remanga_parser.db_request

        assert self.remanga_parser.dir_name in self.remanga_parser.request_categories_genres
        assert '"' in self.remanga_parser.db_request