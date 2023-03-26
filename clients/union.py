# 성서유니온

import requests
from datetime import datetime

class unionClient:
    
    def __init__(self) -> None:
        self.today = datetime.today().strftime('%Y-%m-%d')
        self.url = "https://sum.su.or.kr:8888"
        self.body_top_path = "/Ajax/Bible/BodyTop"
        self.body_bible_path = "/Ajax/Bible/BodyBible"
        self.body_bible_content_path = "/Ajax/Bible/BodyBibleCont"

    def get_top(self) -> dict:
        response = requests.post(
            url=self.url + self.body_top_path, 
            data={ 'qt_ty' : 'QT1' , 'Base_de' : self.today},
        )
        return response.json()

    def get_bible(self) -> dict:
        response = requests.post(
            url=self.url + self.body_bible_path,
            data={ 'qt_ty' : 'QT1' , 'Base_de' : self.today},
        )
        return response.json()

    def get_bible_content(self) -> dict:
        response = requests.post(
            url=self.url + self.body_bible_path,
            data={ 'qt_ty' : 'QT1' , 'Base_de' : self.today, 'Bibletype' : '1'},
        )
        return response.json()