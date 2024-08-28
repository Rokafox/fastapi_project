import sqlite3

#データベースの作成（なかったら作られる）
conn = sqlite3.connect('user.db')

#カーソルオブジェクトの作成
cursor = conn.cursor()

#テーブル作成
cursor.execute('''CREATE TABLE users( id integer primary key, username TEXT, password integer, role TEXT)''')

#変更保存
conn.commit()

#接続を閉じる
conn.close()