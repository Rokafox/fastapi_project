import sqlite3

#データベースの作成（なかったら作られる）
conn = sqlite3.connect('users.db')
conn2 = sqlite3.connect('projects.db')
conn3 = sqlite3.connect('project_members.db')
conn4 = sqlite3.connect('attendance.db')

#カーソルオブジェクトの作成
cursor = conn.cursor()
cursor2 = conn2.cursor()
cursor3 = conn3.cursor()
cursor4 = conn4.cursor()


#テーブル作成
cursor.execute('''CREATE TABLE users( id integer primary key, username TEXT, password integer, role TEXT)''')
cursor2.execute('''CREATE TABLE projects(project_id integer primary key, project_name TEXT, description TEXT, start_time timestamp, end_time timestamp, status TEXT ))''')
cursor3.execute('''CREATE TABLE project_members(project_id integer, user_id integer)''')
cursor4.execute('''CREATE TABLE users(user_id integer, project_id integer, check_in timestamp, check_out timestamp)''')

#変更保存
conn.commit()
conn2.commit()
conn3.commit()
conn4.commit()

#接続を閉じる
conn.close()
conn2.close()
conn3.close()
conn4.close()