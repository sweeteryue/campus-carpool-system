from flask import Flask, render_template_string, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "campus_carpool_2026_secret"

# 模拟存储：常用路线、用户信息（后面B、C同学写后端接口再替换成数据库）
user_info = {
    "nickname": "测试用户",
    "avatar": "",
    "phone": ""
}
saved_routes = [
    {"start": "图书馆", "end": "北门宿舍区"},
    {"start": "教学楼A栋", "end": "食堂三楼"}
]


HTML_TPL = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>校园拼车系统</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: "PingFang SC", "Microsoft YaHei", system-ui, sans-serif;
        }
        :root {
            --deep-blue: #0f3460;
            --mid-blue: #16537e;
            --light-blue: #1a759f;
            --white: #ffffff;
            --gray: #e8edf2;
        }
        body {
            background-color: var(--deep-blue);
            color: white;
            min-height: 100vh;
            animation: fadeIn 0.8s ease-out;
        }
        @keyframes fadeIn {
            from {opacity: 0; transform: translateY(12px);}
            to {opacity:1; transform: translateY(0);}
        }
        @keyframes pulse-btn {
            0% {transform: scale(1);}
            50% {transform: scale(1.03);}
            100% {transform: scale(1);}
        }
        .container {
            max-width: 480px;
            margin: 0 auto;
            padding: 24px 20px;
        }
        .header-title {
            text-align: center;
            margin: 30px 0 40px;
        }
        .header-title h1 {
            font-size: 38px;
            font-weight: 700;
            letter-spacing: 2px;
            text-shadow: 0 2px 10px rgba(0,0,0,0.25);
        }
        .header-title p {
            margin-top: 8px;
            opacity: 0.8;
            font-size: 15px;
        }
        .card {
            background: rgba(255,255,255,0.09);
            border-radius: 18px;
            padding: 22px;
            margin-bottom: 20px;
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255,255,255,0.12);
        }
        .card h3 {
            margin-bottom:16px;
            font-size:18px;
        }
        .form-item {
            margin-bottom:16px;
        }
        label {
            display:block;
            margin-bottom:6px;
            font-size:14px;
            opacity:0.9;
        }
        input {
            width:100%;
            padding:14px 16px;
            border-radius:12px;
            border:none;
            font-size:16px;
            outline:none;
            background: rgba(255,255,255,0.95);
            color:#222;
        }
        .btn {
            width:100%;
            padding:15px;
            border-radius:14px;
            border:none;
            font-size:17px;
            font-weight:600;
            cursor:pointer;
            transition: all 0.3s ease;
        }
        .btn-primary {
            background-color: var(--light-blue);
            color:white;
        }
        .btn-primary:hover {
            animation: pulse-btn 1.2s infinite ease-in-out;
            background-color:#2088b8;
        }
        .btn-wechat {
            background-color:#07c160;
            color:white;
        }
        .route-item {
            padding:12px 14px;
            background:rgba(255,255,255,0.08);
            border-radius:12px;
            margin-bottom:10px;
            font-size:15px;
        }
        .tab-bar {
            position:fixed;
            bottom:0;
            left:0;
            right:0;
            max-width:480px;
            margin:0 auto;
            background-color:#0b284a;
            display:flex;
        }
        .tab-item {
            flex:1;
            text-align:center;
            padding:12px 0;
            font-size:14px;
            cursor:pointer;
        }
        .tab-item.active {
            color:#4ecdc4;
            font-weight:600;
        }
        .page {
            display:none;
        }
        .page.active {
            display:block;
            animation: fadeIn 0.4s ease;
        }
        .tip-text {
            font-size:13px;
            opacity:0.75;
            margin-top:8px;
        }
    </style>
</head>
<body>
<div class="container">
    <div class="header-title">
        <h1>校园拼车系统</h1>
        <p>便捷同行 · 安全拼车</p>
    </div>

    <!-- 登录页 -->
    <div id="page-login" class="page active">
        <div class="card">
            <h3>微信授权登录</h3>
            <p class="tip-text">点击下方按钮，模拟微信一键登录</p>
            <br>
            <button class="btn btn-wechat" onclick="switchPage('page-home')">微信一键授权登录</button>
        </div>
    </div>

    <!-- 首页：发布行程、寻找伙伴 -->
    <div id="page-home" class="page">
        <div class="card">
            <h3>📌 发布出行行程</h3>
            <div class="form-item">
                <label>起点</label>
                <input type="text" id="start-pos" placeholder="例如：图书馆">
            </div>
            <div class="form-item">
                <label>终点</label>
                <input type="text" id="end-pos" placeholder="例如：学校北门">
            </div>
            <div class="form-item">
                <label>出发时间</label>
                <input type="datetime-local" id="go-time">
            </div>
            <div class="form-item">
                <label>备注（可选）</label>
                <input type="text" id="note" placeholder="人数、携带物品等">
            </div>
            <button class="btn btn-primary" onclick="publishTrip()">【寻找拼车伙伴】</button>
            <p class="tip-text" style="text-align:center;margin-top:10px;">点击后跳转到匹配等待页（后续B同学做匹配逻辑）</p>
        </div>

        <div class="card">
            <h3>⭐ 常用路线</h3>
            {% for r in saved_routes %}
            <div class="route-item">
                {{ r.start }} → {{ r.end }}
            </div>
            {% endfor %}
            <button class="btn btn-primary" style="margin-top:10px;padding:10px;font-size:15px" onclick="saveRoute()">保存当前路线</button>
        </div>
    </div>

    <!-- 个人中心页 -->
    <div id="page-mine" class="page">
        <div class="card">
            <h3>👤 个人资料</h3>
            <div class="form-item">
                <label>昵称</label>
                <input type="text" id="nick" value="{{ user_info.nickname }}">
            </div>
            <div class="form-item">
                <label>联系电话</label>
                <input type="text" id="phone" value="{{ user_info.phone }}">
            </div>
            <button class="btn btn-primary" onclick="saveProfile()">保存资料</button>
        </div>
        <div class="card">
            <h3>我的行程</h3>
            <p class="tip-text">待匹配、已确认、已完成行程列表（后续扩展）</p>
        </div>
    </div>

</div>

<!-- 底部Tab导航 -->
<div class="tab-bar">
    <div class="tab-item active" onclick="switchPage('page-home'); setTabActive(this)">首页</div>
    <div class="tab-item" onclick="switchPage('page-mine'); setTabActive(this)">我的</div>
</div>

<script>
    let currentPage = "page-login";
    function switchPage(pageId) {
        document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
        document.getElementById(pageId).classList.add('active');
        currentPage = pageId;
    }
    function setTabActive(el) {
        document.querySelectorAll('.tab-item').forEach(t=>t.classList.remove('active'));
        el.classList.add('active');
    }
    function publishTrip() {
        alert("✅ 行程提交成功！正在寻找同路人（匹配等待页，交给B同学开发匹配逻辑）");
    }
    function saveRoute() {
        const s = document.getElementById('start-pos').value;
        const e = document.getElementById('end-pos').value;
        if(!s || !e) {alert("请填写起点终点");return;}
        alert(`✅ 路线【${s} → ${e}】保存成功！`);
    }
    function saveProfile() {
        alert("✅ 个人资料保存成功！");
    }
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TPL, user_info=user_info, saved_routes=saved_routes)

if __name__ == "__main__":
    app.run(debug=True)
