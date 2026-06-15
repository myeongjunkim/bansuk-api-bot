# 성서유니온
import os
from datetime import datetime

import requests

from bansuk_bot.schemas import BodyBible, BodyBibleContent

import tenacity

# (connect, read) 타임아웃(초). connect를 명시하지 않으면 연결이 막혔을 때
# OS 기본값까지(약 2분) 매달리므로 짧게 끊고 재시도하도록 한다.
REQUEST_TIMEOUT = (5, 30)

# union API의 직접 주소. GitHub Actions(Azure) egress가 이 서버에 간헐적으로
# 차단되므로, 비-Azure 네트워크(Deno Deploy 등)에 올린 프록시를 거치도록
# UNION_BASE_URL 환경변수로 덮어쓸 수 있다. 미설정 시 직접 호출(로컬 등).
DEFAULT_BASE_URL = "https://sum.su.or.kr:8888"


class unionClient:

    def __init__(self) -> None:
        self.today = datetime.today().strftime('%Y-%m-%d')
        # 빈 문자열(시크릿 미설정 시 GitHub이 ""로 주입)도 기본값으로 처리하도록 `or` 사용.
        self.url = (os.environ.get("UNION_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self._proxy_token = os.environ.get("UNION_PROXY_TOKEN") or None
        self.body_top_path = "/Ajax/Bible/BodyTop"
        self.body_bible_path = "/Ajax/Bible/BodyBible"
        self.body_bible_content_path = "/Ajax/Bible/BodyBibleCont"
        self._request_data()

    def _headers(self) -> dict:
        # 프록시를 오픈 릴레이로 두지 않기 위한 공유 토큰. 직접 호출 시엔 빈 헤더.
        return {"x-proxy-token": self._proxy_token} if self._proxy_token else {}

    @tenacity.retry(
        # 짧은 네트워크 블립(DNS 실패·간헐적 연결 끊김)을 흡수하기 위해
        # 지수 백오프로 재시도한다. requests가 던지는 예외는 builtin
        # TimeoutError가 아니라 RequestException 계열이므로 그걸로 잡아야
        # 실제로 재시도가 걸린다.
        wait=tenacity.wait_exponential(multiplier=2, min=2, max=20),
        stop=tenacity.stop_after_attempt(5),
        retry=tenacity.retry_if_exception_type(requests.exceptions.RequestException),
        reraise=True,
    )
    def _request_data(self) -> None:
        self.top = self._get_top()
        self.bible = self._get_bible()
        self.content = self._get_bible_content()

    def _get_top(self) -> dict:
        response = requests.post(
            url=self.url + self.body_top_path,
            data={ 'qt_ty' : 'QT1' , 'Base_de' : self.today},
            headers=self._headers(),
            timeout=REQUEST_TIMEOUT,
        )
        return response.json()

    def _get_bible(self) -> dict:
        response = requests.post(
            url=self.url + self.body_bible_path,
            data={ 'qt_ty' : 'QT1' , 'Base_de' : self.today},
            headers=self._headers(),
            timeout=REQUEST_TIMEOUT,
        )
        return response.json()

    def _get_bible_content(self) -> dict:
        response = requests.post(
            url=self.url + self.body_bible_content_path,
            data={ 'qt_ty' : 'QT1' , 'Base_de' : self.today, 'Bibletype' : '1'},
            headers=self._headers(),
            timeout=REQUEST_TIMEOUT,
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

        

        
     
