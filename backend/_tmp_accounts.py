import json, urllib.request, urllib.error, pymysql

def call(url, payload):
    req = urllib.request.Request(url, data=json.dumps(payload, ensure_ascii=False).encode(),
                                 headers={'Content-Type': 'application/json'}, method='POST')
    try:
        r = urllib.request.urlopen(req); return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()

B='http://127.0.0.1:5000/api'
# 学生
print('student:', call(B+'/register/normal', {'username':'stu_t1','password':'123456','confirmPassword':'123456','name':'学生一','role':'student','school':'a校','studentId':'stu_t1'}))
# 教师
print('teacher:', call(B+'/register/normal', {'username':'tea_t1','password':'123456','confirmPassword':'123456','name':'教师一','role':'teacher','school':'a校','teacherId':'tea_t1'}))

# 库中将教师置为已通过
c = pymysql.connect(host='localhost', user='root', password='cyc13729243361', database='achievement_db', charset='utf8mb4')
cur = c.cursor()
cur.execute("UPDATE teachers t JOIN users u ON u.id=t.user_id SET t.status='approved' WHERE u.username='tea_t1'")
c.commit()
cur.execute("""
SELECT u.username, u.role, u.name, t.status st
FROM users u LEFT JOIN teachers t ON t.user_id=u.id
WHERE u.username IN ('admin','stu_t1','tea_t1')""")
for r in cur.fetchall(): print('ACCT:', r)
c.close()