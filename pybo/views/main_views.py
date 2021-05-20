from flask import Blueprint, render_template, url_for, request, jsonify
from werkzeug.utils import redirect

from pybo.models import Question,Answer
from datetime import datetime
from pybo import db
from pybo.movieapi import Mrank
from pybo.naverapi import navermovie


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


def movie_info(imgurl, title,link,subtitle):
    response_json = jsonify(
        fulfillment_text='영화정보',
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