import pymysql

db = pymysql.connect(host='localhost',
                user='root',
                password='Hich7young',
                database='academicworld',
                charset='utf8mb4',
                port=3306,
                cursorclass=pymysql.cursors.DictCursor)

#ignore this
def mysql_get_university(input_value):
    with db.cursor() as cursor:
        sql = 'select id, name from university where name like "%' + input_value + '%";'
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

def mysql_get_all_keywords():
    with db.cursor() as cursor:
        sql = 'select name from keyword order by name'
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

#ignore this
def mysql_get_professor_university2(input_keyword, n):
    with db.cursor() as cursor:
        sql = 'select f.name, u.name, n_pubs, fk.score\
               from keyword k, faculty_keyword fk, faculty f, university u, publication_keyword pk, keyword_faculty_publication_summary kfps\
               where k.name = "{}" and \
                     k.id = fk.keyword_id and fk.faculty_id = f.id and f.university_id = u.id and k.id = kfps.keyword_id and f.id = kfps.faculty_id\
               order by n_pubs desc, fk.score desc\
               limit {}'.format(input_keyword, n)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    

def mysql_get_professor_university(input_keyword, n):
    with db.cursor() as cursor:
        sql = 'select f.name, u.name, fk.score as n_pubs\
               from keyword k, faculty_keyword fk, faculty f, university u, publication_keyword pk \
               where k.name = "{}" and \
                     k.id = fk.keyword_id and fk.faculty_id = f.id and f.university_id = u.id \
               order by n_pubs desc\
               limit {}'.format(input_keyword, n)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result