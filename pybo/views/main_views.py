from flask import Blueprint, render_template, url_for, request, jsonify
from werkzeug.utils import redirect

from pybo.models import Question,Answer
from datetime import datetime
from pybo import db
from pybo.movieapi import Mrank
from pybo.naverapi import navermovie, navershop
from pybo.weatherapi import get_wdata
import json
from collections import OrderedDict

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/test')
def test():
    for i in range(100):
        q = Question(subject='테스트 데이터 [%03d]'%i, content='내용무',create_date=datetime.now())
        db.session.add(q)
    db.session.commit()



    return redirect(url_for('main.index'))

@bp.route('/hello')
def hello_pybo():
    #result = Question.query.filter(Question.id==1).all()
    #result = Question.query.get(1) #id(primary key)가 1번데이터를 가져옴
    #result = Question.query.filter(Question.subject.like('%무엇%')).all()
    #result = Question.query.filter(Question.username.like('%김%')).all()
    #print(result)
    #result = Question.query.get(1)
    #print(result.subject)
    #result.subject = '파이보 재밌어요'
    #db.session.commit()
    #result = Question.query.get(1)
    #db.session.delete(result)
    #db.session.commit()

    #q = Question.query.get(2)
    #print(q)
    #a = Answer(question = q, content='답변 3번',create_date=datetime.now())
    #db.session.add(a)
    #db.session.commit()

    #q = Question.query.get(2)
    #result = q.answer_set
    #print(result)

    #q = Question.query.get(2)
    #db.session.delete(q)
    #db.session.commit()

    #q = Question.query.get(5)

    #db.session.delete(q)
    #db.session.commit()


    #2번 질문에 대한 답변 데이터를 가져오세요.


    return 'Hello, Pybo!'

@bp.route('/')
def index():
    return redirect(url_for('question._list'))


@bp.route('/webhook',methods=['GET','POST'])
def webhook():
    req = request.get_json()
    if req['queryResult']['intent']['displayName'] =='movie ranking':
        rankdata = Mrank()

        result = ''
        count = 1
        for temp in rankdata:
            result = result + str(count) + '위 : '+temp['title']
            if count==3:
                break
            count += 1
    elif req['queryResult']['intent']['displayName'] =='movie info - custom':
        movieresult = navermovie(req['queryResult']['queryText'])
        moviedata = movieresult['items'][0]


        return movie_info(moviedata['image'],moviedata['title'],moviedata['link'],
                          '감독:'+moviedata['director']+' 출연자'+moviedata['actor'])
    elif req['queryResult']['intent']['displayName'] == 'weather - custom':
        wdata = get_wdata(req['queryResult']['queryText'])
        print(wdata)
        return weather_info(wdata)
    elif req['queryResult']['intent']['displayName'] == 'product - custom':
        sdata = navershop(req['queryResult']['queryText'])
        return shop_infos(sdata['items'])



def movie_info(imgurl, title,link,subtitle):
    response_json = jsonify(
        fulfillment_text=title,
        fulfillment_messages=[
            {
                "payload": {
                    "richContent": [[
                        {
                            "type": "image",
                            "rawUrl": imgurl
                        },
                        {
                            "type": "info",
                            "title": title,
                            "actionLink": link,
                            "subtitle": subtitle
                        }
                    ]]
                }
            }
        ]
    )

    return response_json
def weather_info(wdata):
    strdata = ''

    if '지역' in wdata:
        strdata += wdata['지역']+'의 '
    if '현재일기' in wdata and len(wdata['현재일기'])>1:
        strdata += '현재일기는' + wdata['현재일기']
    if '현재기온' in wdata and len(wdata['현재기온'])>1:
        strdata += '현재기온은' + wdata['현재기온']
    if '일강수' in wdata and len(wdata['일강수'])>1:
        strdata += '일강수는' + wdata['일강수']

    strdata += '입니다.'


    response_json = jsonify(
        fulfillment_text=strdata
    )

    return response_json

def shop_info(items):

    sdata = OrderedDict()
    sdata['fulfillment_text'] = 'title'
    sdata['fulfillment_messages'] = []
    scarddata = OrderedDict()

    cardimg = OrderedDict()
    cardimg['type'] = 'image'
    cardimg['rawUrl'] = 'rawUrl'

    cardinfo = OrderedDict()
    cardinfo['type'] = 'info'
    cardinfo['title'] = 'title'
    cardinfo['actionLink'] = 'actionLink'
    cardinfo['subtitle'] = 'subtitle'

    slist = []
    slist.append(cardimg)
    slist.append(cardinfo)

    rich = OrderedDict()
    rich['richContent'] = []
    rich['richContent'].append(slist)

    scarddata['payload'] = rich
    sdata['fulfillment_messages'].append(scarddata)

    print(json.dumps(sdata))

def shop_infos(items):

    plist = []
    for temp in items:
        imgurl = temp['image']
        title = temp['title']
        link = temp['link']
        subtitle = '최저가 :' + temp['lprice']
        listdata = [
            {
                "type": "image",
                "rawUrl": imgurl
            },
            {
                "type": "info",
                "title": title,
                "actionLink": link,
                "subtitle": subtitle
            }
        ]

        plist.append(listdata)

    response_json = jsonify(
        fulfillment_text=title,
        fulfillment_messages=[
            {
                "payload": {
                    "richContent": plist
                }
            }
        ]
    )

    return response_json



