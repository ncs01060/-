from flask import Flask, request
import requests
from flask_cors import CORS
from bs4 import BeautifulSoup
from openai import OpenAI

client = OpenAI(api_key='your api key')
app = Flask(__name__)
CORS(app)

@app.route('/bookInfo')
def BookInfo():
    # 사용자 입력 받기
    a = request.args.get('book')
    url = f"https://www.yes24.com/Product/Search?domain=ALL&query={a}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    # 책 제목과 이미지 URL 추출
    books = soup.select('div.itemUnit > div.item_info')
    titles = []
    img = []
    ids = []

    for book in books:
        title = book.select_one('a.gd_name').text.strip()
        titles.append(title)

    a_tags = soup.select('a.lnk_img')
    for a_tag in a_tags:
        # 이미지 태그에서 'data-original' 속성 추출
        img_tag = a_tag.select_one('img')
        if img_tag and 'data-original' in img_tag.attrs:
            img_url = img_tag['data-original']
            img.append(img_url)

    # 책 ID 추출
    li_tags = soup.select('li')

# data-goods-no 값 추출
    goods_ids = [li.get('data-goods-no') for li in li_tags if li.get('data-goods-no')]
    # JSON 데이터로 반환
    return {
        "title": titles,
        "img": img,
        "ids": goods_ids
    }


@app.route("/info")
def info():
    # Get the 'id' parameter from the query string
    a = request.args.get('id')
    b = request.args.get('name')
    url = f"https://www.yes24.com/Product/Goods/{a}"
    res = requests.get(url)
    
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(res.text, 'html.parser')
    
    # Select the <textarea> element that contains the information you're looking for
    textarea_element = soup.select_one("textarea")  # Update the selector if necessary

    # Extract the text inside the <textarea> element
    if textarea_element:
        textarea_text = textarea_element.get_text(strip=True)
    else:
        textarea_text = "No textarea found"

    text = """
오늘 볼 이 <이생규장전>이라는 작품은
금성, 동아, 미래엔, 비상, 지학사, 창비 등
수많은 교과서에 실려있는 작품이자
올해 수능특강에도 실린 필수 소설이 되겠습니다!

몇 가지 포인트 딱 잡아서, 살펴보도록 합시다!


1

작가 김시습

김시습은 어릴 때부터 신동, 천재로 엄청 유명했다고 해요.
별명이 '김오세'였는데
(예를 들면 "시습 'the 5 years old' KIM"약간 요런 느낌?)
세종대왕이 지어줬다구 해요.
하도 시를 잘 짓는다고 하니 세종이 한번 보자, 라고 애기를
궁궐로 불러들인거죠. 5살짜리 애를요.
근데 진짜 시를 잘 짓는거야.
그래서 비단 50필을 선물로 하사했다고....

여튼 이렇게 똘똘한 아이였으니 커서도 벼슬을 하고.. 좋았는데
계유정난이 일어나버린거 ㅠㅠ
수양대군에 의해 단종이 폐위되고, 단종을 지키려다 죽은 여섯 명의 신하들(사육신이라고 하죠?)... 김시습의 대쪽같은 성격은 이런 상황을 그냥 두고볼 수가 없었어요.
그래서 세조의 말을 거역하고 세상을 떠돌아다닙니다.

여튼.. 이렇게 계유정난이라는 큰 사건으로
김시습의 정치 이상은 완전히 박살이 나버려요.
그러니 김시습은 현실의 삶에서는 어떤 의미도 찾을 수가 없고,
그러다보니 비현실의 이야기들.
예컨대 요즘 유행하는 이세계 스토리 같은 것
(ex.. 블랙기업에 충실히 다니던 김 모씨는 결국 과로로 쓰러지고.. 눈을 떠보니 용사는 용사인데 레벨이 1에서 더이상 오르지 않는 용사가 되었다더라!! 같은..?)
에 몰두하게 되고, 그 결과물이 바로 <금오신화>입니다.

금오신화에는 만복사저포기, 취유부벽정기, 남염부주지, 용궁부연록, 그리고 이생규장전이 있죠!
(대부분이 귀신과의 러브스토리, 귀신과의 술 한 잔, 지옥/용궁 방문하기.. 뭐 그런 스토리!)


2

제목 <이생규장전>

제목의 뜻은 '이생이 담을 넘다'입니다. 여기에서 '담'의 의미를 여러가지로 생각해볼 수가 있어요.

① 현실의 담
② 가부장제 유교 윤리
③ 삶과 죽음의 경계
가 그것입니다.

먼저 ① 현실의 담은
첫번째 만남인
담 너머의 최 씨의 아름다움에 반하는 이생의 모습을 말해요.
최씨도 (스토커같지만 존잘인) 이생에게 반하고.. 이들은 사랑하게 됩니다. 하지만 이생 아빠가 반대해요 ㅠ
그래서 둘은 첫번째 이별을 겪고야 말죠.
하지만 이 첫번째 이별은 적극적이고 능동적인 최 씨에 의해 극복됩니다. 그 때 넘은 상징적 의미의 '담'이 바로
② 가부장제 유교 윤리
라고 볼 수 있는거죠. 아빠가 결혼하지 말랬는데 결혼을 하니까요.
자 이렇게 두번째 만남을 하게 됩니다만, 이 만남은 다시 두번째 이별로 이어집니다. 왜냐하면 홍건적의 난이 일어나거든요.
최 씨가 홍건적에게 죽임을 당하고, 이생은 풀밭에 숨어서 그 광경을 봅니다. 이때의 이생이 어떻게 보이시나요? 좀 찌질하지 않나요..? 일반적으로 애정전기소설에서는 남성은 좀 찐으로, 여성은 적극적이고 능동적으로 등장하는 경우가 많답니다.(아무래도 주요 독자층이 상층 여성이라 그런 게 아닐까 싶어요!)

이생은 최 씨와 헤어지고 너무너무 슬퍼해요.(아니 그럼 풀밭에 숨지말고 나와서 싸우든가하지) 그렇게 슬퍼하던 중, 최 씨가 귀신으로 변해 다시 이생 앞에 등장합니다. 즉 이들은
③ 삶과 죽음의 경계라는 '담'을 넘어 다시 세번째 만남을 하게 된거죠. 그러나 여러분도 아시다시피 삶과 죽음의 경계라는 것은 한낱 인간이 마음대로 넘을 수가 없는 거대한 담이랍니다. 결국에는 세번째 이별을 다시금 하게 되는 것으로 소설은 결말을 맺지요.

정리해보니 어떤가요? 이 작품은
세 가지 의미의 '담'과 이 '담'을 넘고 만났다가 이별하는 세 번의 만남과 이별이 주요 뼈대가 된다는 걸 알 수 있죠?
3

우의적 감상

'우의적'이란 빗대어 표현하는 것을 뜻해요.
즉,
이 작품의 '이생'은 김시습이라 볼 수 있고,
'최 씨'는 단종 또는 사육신으로 볼 수 있다는거죠.
왜냐하면 최 씨가 죽어가는 모습을 이생은 숨어서 풀밭에서 보고있잖아요. 아마 김시습은 스스로 그때 사육신들과 같이 죽지 못한 것을 평생 후회했을 거예요.
그런 마음을 담아 쓴 <이생규장전>, 오늘 정리한 것을 마음에 담고 다시 읽으면 아마 소설이 다르게 읽힐 거예요!


더 자세한 내용은 학원에서 수업 때 마무리하도록 하죠!



"""
    completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "주어진 텍스트에 포함되어 있는 시험 출제 포인트를 적어줘.",
                },
                {
                    "role":"system",
                    "content":f"{text}이렇게 정리하면 좋을거같아"

                },
                {
                    "role": "user",
                    "content": f"이 책의 제목은 {b} 이고 내용은 {textarea_text}야 알려주면 좋겠어",
                },
            ],
        )
        
    summary = completion.choices[0].message.content.strip()
    
    # Return the extracted text from the <textarea> element
    return {
        "textarea_content": textarea_text,
        'summary': summary
             }
app.run("127.0.0.1", port=8001, debug=True)