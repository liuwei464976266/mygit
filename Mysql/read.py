import mysql_connect

ms = mysql_connect.MySQL(host='localhost', user='root', pwd='lw1212', db='sql_tutorial', port=3306)

data = ms.ExecQuery('select * from `student`where student_id = 2;')
print(data)