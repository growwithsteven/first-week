from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta

# 필요한 기능
# 1. 동영상 및 온갖 정보 불러오기
# 제목, 썸네일 주소, 영상 주소, 좋아요 숫자, 싫어요 숫자

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/video', methods=['GET'])
def randomVideo():
    videoInfo = list(db.videos.find({},{'_id':False}))
    return jsonify({'videoInfo': videoInfo})

    # 좋아요, 싫어요 데이터베이스 구축

@app.route('/api/like', methods=['POST'])
def like_star():
    name_receive = request.form['name_give']
    target_star = db.mystar.find_one({'name':name_receive})
    current_like = target_star['like']
    new_like = current_like + 1
    db.update_one({'name':name_receive}, {'$set':{'like':new_like}})

# 2. 동영상 좋아요
@app.route('/api/video/like', methods=['POST'])
def video_like():
    name_receive = request.form['name_give']
    target_video = db.mystar.find_one({'name':name_receive})
    current_like = target_video['like']
    new_like = current_like + 1
    db.mystar.update_one({'name':name_receive}, {'$set':{'like':new_like}})

# 3. 동영상 싫어요
@app.route('/api/video/dislike', methods=['POST'])
def video_dislike():
    name_receive = request.form['name_give']
    target_video = db.mystar.find_one({'name':name_receive})
    current_dislike = target_video['like']
    new_like = current_dislike + 1
    db.mystar.update_one({'name':name_receive}, {'$set':{'like':new_like}})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5556, debug=True)