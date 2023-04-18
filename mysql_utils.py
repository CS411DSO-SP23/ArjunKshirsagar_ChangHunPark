import pymysql

db = pymysql.connect(host='localhost',
                user='root',
                password='Hich7young',
                # password='test_root'
                database='academicworld',
                charset='utf8mb4',
                port=3306,
                cursorclass=pymysql.cursors.DictCursor)

def mysql_get_all_keywords():
    with db.cursor() as cursor:
        sql = 'select name from keyword order by name'
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

#widget2
def mysql_year_publication(keyword):
    with db.cursor() as cursor:
        sql = 'select p.year as year, count(p.id) as n_pubs ' + \
              'from keyword k join publication_keyword pk on k.id = pk.keyword_id ' + \
            'join publication p on pk.publication_id = p.id ' + \
            'where k.name = "{}" '.format(keyword) + \
            'group by p.year ' + \
            'order by year'
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

#widget5
def mysql_create_favorite_faculty(input_faculty, action):
    with db.cursor() as cursor:
        sql1 = 'DROP TABLE IF EXISTS favorite_faculty;'
        sql2 = 'CREATE TABLE favorite_faculty AS SELECT faculty.name as fname, position, university.name as uname, email, phone' + \
            'FROM faculty, university WHERE faculty.university_id = university.id AND faculty.name = {}'.format(input_faculty)
        sql3 = 'SELECT * FROM favorite_faculty;'
        cursor.execute(sql1)
        cursor.execute(sql2)
        cursor.execute(sql3)
        result = cursor.fetchall()
        return result

def mysql_update_favorite_faculty(input_faculty, action):
    with db.cursor() as cursor:
        if action=='Add':
            sql1 = 'INSERT INTO favorite_faculty(fname, position, uname, email, phone)' + \
                'SELECT faculty.name as fname, position, university.name as uname, email, phone' + \
                'FROM faculty, university WHERE faculty.university_id = university.id AND faculty.name = {}'.format(input_faculty)
        elif action=='Remove':
            sql1 = 'DELETE FROM favorite_faculty WHERE name = {}'.format(input_faculty)
        cursor.execute(sql1)
        sql2 = 'SELECT * FROM favorite_faculty;'
        cursor.execute(sql2)
        result = cursor.fetchall()
        return result

#widget6
def mysql_create_favorite_universities(input_university, action):
    with db.cursor() as cursor:
        sql1 = 'DROP TABLE IF EXISTS favorite_university;'
        sql2 = 'CREATE TABLE favorite_university AS SELECT name FROM university WHERE faculty.name = {}'.format(input_university)
        sql3 = 'SELECT * FROM favorite_university;'
        cursor.execute(sql1)
        cursor.execute(sql2)
        cursor.execute(sql3)
        result = cursor.fetchall()
        return result

def mysql_update_favorite_universities(input_university, action):
    with db.cursor() as cursor:
        if action=='Add':
            sql1 = 'INSERT INTO favorite_university(name)' + \
                'SELECT name' + \
                'FROM university WHERE name = {}'.format(input_university)
        elif action=='Remove':
            sql1 = 'DELETE FROM favorite_university WHERE name = {}'.format(input_university)
        cursor.execute(sql1)
        sql2 = 'SELECT * FROM favorite_university;'
        cursor.execute(sql2)
        result = cursor.fetchall()
        return result


#unused
def mysql_get_professor_university(input_keyword, n):
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