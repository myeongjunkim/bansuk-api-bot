import requests

def send_message_v2(webhook_url:str) -> None:
    data = {
	"text": "2023.05.01(월)" + "\n" + "유랑이 행진으로",
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "2023.05.01(월)" + "\n" + "유랑이 행진으로",
				"emoji": True
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "#본문",
				"emoji": True
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "민수기(Numbers) 21:1 - 21:20"
			}
		},
        {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "2. 네겝에 거주하는 가나안 사람 곧 아랏의 왕이 이스라엘이 아다림 길로 온다 함을 듣고 이스라엘을 쳐서 그 중 몇 사람을 사로잡은지라\n\n3. 이스라엘이 여호와께 서원하여 이르되 주께서 만일 이 백성을 내 손에 넘기시면 내가 그들의 성읍을 다 멸하리이다\n\n4. 여호와께서 이스라엘의 목소리를 들으시고 가나안 사람을 그들의 손에 넘기시매 그들과 그들의 성읍을 다 멸하니라 그러므로 그 곳 이름을 호르마라 하였더라"
			}
		},
        {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*해설*",
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "> 시내산에서의 행군 준비(1-10장), 가데스 바네아에서의 원망과 38년 광야 유랑(11-20장)을 거쳐, 이제 이스라엘은 요단 동편에서의 여정을 시작합니다(21-36장)."
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*📌 하나님은 어떤 분입니까?* \n\n 1-3절   패배와 수치로 점철된 민수기의 둘째 단락(11-20장)을 매듭지으시고, 회복과 승리의 셋째 단락(21-36장)을 여십니다. 38년 전 '호르마'는 이스라엘 군대가 멸망당한 치욕의 땅이었지만(14:39-45), 이제는 이스라엘이 대적을 멸망시킨 새 역사의 분수령이 됩니다. 출애굽 2년 차에 가나안으로 들어가라 하면 애굽으로 돌아가겠다 하고, 광야로 가라 하시면 가나안으로 진격하던 청개구리 이스라엘이, 출애굽 40년 차에는 하나님께 묻고 순종하여 방향을 설정합니다. 5월 첫날, 우리도 성숙과 성취의 새 단락을 시작합시다. \n\n 4-9절   이스라엘을 포기하지 않으십니다. 불뱀을 통한 재앙과 놋뱀을 통한 치유를 사용하셔서 끝끝내 이스라엘의 회개를 받아내십니다. 모압으로 향하는 지름길이 막혀(20:21) 결국 우회로를 통한 고된 행군이 지속되자, 이스라엘 백성은 금세 예전 모습으로 돌변하여 불신하고 원망의 말을 쏟아냅니다. 신앙의 훈련과 연단을 거쳐 어느 정도 영적 성숙에 이르렀음에 감사하다가도, 어느 한순간 작은 시험과 유혹에 무너져 밑바닥을 드러내는 우리의 자화상 같지 않습니까? 그럼에도 하나님이 우리를 사생자가 아닌 자녀로 여기셔서 주시는 징계(히 12:7-11)가 있다면, 우리는 광야로의 퇴행이 아닌, 가나안을 향한 전진의 국면에 여전히 속해 있는 것입니다. 불뱀과도 같은 그 징계와 시험으로 인해, 장대(십자가)에 매달리신(요 3:14) 예수님을 쳐다보는 것 외에 아무것도 할 수는 상황에 이르렀다면, 하나님은 여전히 우리를 포기하지 않으신 것입니다. 요구하시는 그 믿음을 내어드리십시오."
			}
		},
	]
	}
    requests.post(url=webhook_url, json=data)

send_message_v2("https://hooks.slack.com/services/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")
