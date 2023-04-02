# 성서유니온
import requests
from datetime import datetime

from bansuk_bot.schemas import BodyBible, BodyBibleContent

class unionClient:
    
    def __init__(self) -> None:
        self.today = datetime.today().strftime('%Y-%m-%d')
        self.url = "https://sum.su.or.kr:8888"
        self.body_top_path = "/Ajax/Bible/BodyTop"
        self.body_bible_path = "/Ajax/Bible/BodyBible"
        self.body_bible_content_path = "/Ajax/Bible/BodyBibleCont"
        
        self.top = self._get_top()
        self.bible = self._get_bible()
        self.content = self._get_bible_content()

    def _get_top(self) -> dict:
        response = requests.post(
            url=self.url + self.body_top_path, 
            data={ 'qt_ty' : 'QT1' , 'Base_de' : self.today},
        )
        return response.json()

    def _get_bible(self) -> dict:
        response = requests.post(
            url=self.url + self.body_bible_path,
            data={ 'qt_ty' : 'QT1' , 'Base_de' : self.today},
        )
        return response.json()

    def _get_bible_content(self) -> dict:
        response = requests.post(
            url=self.url + self.body_bible_content_path,
            data={ 'qt_ty' : 'QT1' , 'Base_de' : self.today, 'Bibletype' : '1'},
        )
        return response.json()


    def fetch_body_bible(self) -> BodyBible:
        return BodyBible(
            date=self.top["BibleDay"],
            week_day=self.top["BibleDateGetWeek"],
            title=self.content['Qt_sj'],
            bible_name=self.content["Bible_name"],
            bible_range=self.content["Bible_chapter"],
            bible_text=[
                {line["Verse"]:line["Bible_Cn"]} for line in self.bible
            ]
        )
    
    def fetch_body_bible_content(self) -> BodyBibleContent:
        Qt_q = ["Qt_q1_str", "Qt_q2_str", "Qt_q3_str", "Qt_q4_str"]
        QT_a = ["Qt_a1", "Qt_a2", "Qt_a3", "Qt_a4"]

        content_data = [
            {self.content[Qt_q[i]]:self.content[QT_a[i]]}  for i in range(4) if self.content[QT_a[i]]
        ]
        return BodyBibleContent(
            content_title=self.content["Qt_Brf"],   
            content_data=content_data 
        )

        

        
     
