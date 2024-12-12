from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 配置SQLite数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///treasurehunt.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 定义玩家模型
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(80), unique=True, nullable=False)
    score_history = db.relationship('Score', backref='player', lazy=True)

# 定义分数模型
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)

# 初始化数据库
with app.app_context():
    db.create_all()

# API接口：创建或更新玩家信息
@app.route('/api/player', methods=['POST'])
def update_player():
    data = request.get_json()
    nickname = data.get('nickname')
    if not nickname:
        return jsonify({"error": "Nickname is required"}), 400
    
    player = Player.query.filter_by(nickname=nickname).first()
    if player is None:
        player = Player(nickname=nickname)
        db.session.add(player)
        db.session.commit()
    
    return jsonify({"id": player.id, "nickname": player.nickname}), 201

# API接口：添加游戏分数
@app.route('/api/score', methods=['POST'])
def add_score():
    data = request.get_json()
    player_id = data.get('player_id')
    score = data.get('score')

    if not player_id or not score:
        return jsonify({"error": "Player ID and score are required"}), 400
    
    new_score = Score(score=score, player_id=player_id)
    db.session.add(new_score)
    db.session.commit()

    return jsonify({"message": "Score added successfully"}), 201

# API接口：获取玩家信息和游戏得分历史记录
@app.route('/api/player/<int:player_id>', methods=['GET'])
def get_player(player_id):
    player = Player.query.get_or_404(player_id)
    scores = [{"score": s.score, "timestamp": s.timestamp.isoformat()} for s in player.score_history]
    return jsonify({
        "id": player.id,
        "nickname": player.nickname,
        "scores": scores
    }), 200

# 路由：主页，返回HTML页面
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)