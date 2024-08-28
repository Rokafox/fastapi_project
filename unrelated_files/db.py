import sqlite3

# データベースの作成（なかったら作られる）
conn = sqlite3.connect('app.db')

# カーソルオブジェクトの作成
cursor = conn.cursor()

# テーブル作成
cursor.execute('''CREATE TABLE users(
                    id INTEGER PRIMARY KEY, 
                    username TEXT, 
                    password TEXT, 
                    role TEXT)''')

cursor.execute('''CREATE TABLE projects(
                    project_id INTEGER PRIMARY KEY, 
                    project_name TEXT, 
                    description TEXT, 
                    start_time TIMESTAMP, 
                    end_time TIMESTAMP, 
                    status TEXT)''')

cursor.execute('''CREATE TABLE project_members(
                    project_id INTEGER, 
                    user_id INTEGER,
                    PRIMARY KEY (project_id, user_id),
                    FOREIGN KEY (project_id) REFERENCES projects(project_id),
                    FOREIGN KEY (user_id) REFERENCES users(id))''')

cursor.execute('''CREATE TABLE attendance(
                    user_id INTEGER, 
                    project_id INTEGER, 
                    check_in TIMESTAMP, 
                    check_out TIMESTAMP,
                    PRIMARY KEY (user_id, project_id, check_in),
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (project_id) REFERENCES projects(project_id))''')

# 変更保存
conn.commit()

# 接続を閉じる
conn.close()
