从烧瓶导入烧瓶，请求，jsonify，render_template，中止
从flask_sqlalchemy导入SQLAlchemy
从flask_cors导入CORS
从日期时间导入日期时间
导入日志记录

应用程序 = Flask ( __name__, static_folder= '静态' , template_folder= '模板' )
CORS ( app )   # 允许跨域请求

# 配置SQLite数据库
应用程序。config [ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///treasurehunt.db'
应用程序。配置[ 'SQLALCHEMY_TRACK_MODIFICATIONS' ] = False

数据库= SQLAlchemy （应用程序）

#记录日志
basicConfig  ( level=logging.INFO ) 记录。
记录器=记录。获取记录器（ __name__ ）

# 定义玩家模型
玩家类别（数据库模型）：
    id = 数据库。列（ db.整数， Primary_key= True）
    昵称=db.列（ db. String（80 ），唯一= True，可空= False）
    分数历史记录 = db.关系（'分数'，backref= '玩家'，lazy= True）

# 共享模型
样本分数（数据库模型）：
    id = 数据库。列（ db.整数， Primary_key= True）
    分数 = 分贝.列( db.Integer , nullable = False   )
    时间 = 数据库.列（ db. DateTime， nullable= False，默认= datetime.乌特克诺）
    玩家 ID = 数据库. Column ( db.Integer , db.ForeignKey ( ' player.id' ) , nullable = False )

# 初始化数据库（建议移至单独的脚本中）
与应用程序。应用程序上下文（）：
    数据库。创建全部（）

# API接口：创建或更新玩家信息
@ app.route ( '/api/player' ,methods= [ 'POST' ] )
def  update_player ( ) :
    尝试：
        数据=请求。获取_json ( )
        昵称=数据。获取（'昵称'）
        如果不是昵称：
            return   jsonify  (  {  "error" : "昵称必填项"  }  ) , 400
        
        玩家=玩家。询问。filter_by （昵称=昵称）。第一个的（）
        如果玩家为无：
            玩家=玩家（昵称=昵称）
            数据库。会议。添加（玩家）
            数据库。会议。犯罪（）
            记录器。info  (  f"创建了新玩家，昵称：{昵称} "  )
        
        return   jsonify  (  {  "id" : 玩家.id , "昵称" : 玩家.昵称}  ) , 201
    另外异常e：
        记录器。error  (  f" 更新播放器失败: {  str  ( e )  } " )
        return  jsonify  (  {  "error" : "更新播放器时发生错误"  }  ) , 500

# API接口：添加游戏积分
@ app.route (  '/api/score' ,methods= [  'POST'  ]  )
def   add_score  (  ) :
    尝试：
        数据=请求。获取_json  (  )
        玩家ID =数据。获取(  '玩家ID'  )
        分数=数据。得到（'分数'）

        如果不是player_id或没有得分：
            return  jsonify  (  {  "error" : "需要玩家 ID 和分数"  }  ) , 400
        
        new_score = 分数（分数=分数，player_id=玩家id ）
        数据库。会议。添加（新股票）
        数据库。会议。犯罪（）
        记录器。info  (  f"为玩家{ player_id }添加了分数{ score } " )
        
        return  jsonify  (   {   "message" : "积分添加成功"   }   ) , 201
    另外异常e：
        记录器。error   f" 添加分数失败: { str () } (   )f" 添加分数失败: {  str  ( e )  } "  
        return    jsonify   (   {   "error" : "添加股票时发生错误"   }  ) , 500

# API接口：获取玩家信息和游戏得分历史记录
@app.route (  '/api/player/<int:player_id>' ,methods= [  'GET'  ]  )
def   get_player  ( player_id ) :
    尝试：
get_or_404          (玩家ID )
        分数 = [  {  "分数" : s.分数，“计时器”：s。计时器。isoformat  (  )  }用于播放器中的s。得分_历史]
        返回jsonify  ( {
            “id”：玩家。ID，
            “昵称”：玩家。昵称,
            “股数”：股数
        }   ) , 200
    另外异常e：
        记录器。error   (   f"获取玩家信息失败：{   str   ( e )   } "   )
        return    jsonify   (   {   "error" : "获取玩家信息时发生错误"   }   ) , 500

# 路由：主页，返回HTML页面
@应用程序.route (  '/' )
定义指数(   ) :
    返回渲染模板（'index.html'）

如果__name__ == '__main__'：
    应用程序。运行（调试=真）
