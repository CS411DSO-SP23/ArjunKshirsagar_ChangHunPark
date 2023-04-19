import pymysql

db = pymysql.connect(host='localhost',
                user='root',
                password='Hich7young',
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

def mysql_get_all_favorite_faculties():
    with db.cursor() as cursor:
        sql = 'select * from favorite_faculty order by name'
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


#widget5 using transaction tecnology
def mysql_add_favorite_faculty(input_faculty):
    with db.cursor() as cursor:
        sql1 = 'CREATE TABLE IF NOT EXISTS favorite_faculty (' + \
                'Name varchar(512) not null, ' + \
                'Position varchar(512), ' + \
                'University varchar(512),' + \
                'Email varchar(512),' + \
                'Phone varchar(512),' + \
                'primary key(Name))'
        cursor.execute(sql1)
        sql2 = 'select f.name, position, u.name as univ, email, phone ' + \
                'from faculty f join university u on f.university_id = u.id ' + \
                'where trim(f.name) = trim("{}")'.format(input_faculty)
        cursor.execute(sql2)
        result = cursor.fetchall()
        #print(sql2)
        #print(result)
        position = result[0]["position"]
        university = result[0]["univ"]
        email = result[0]["email"]
        phone = result[0]["phone"]
        sql3 = 'INSERT IGNORE INTO favorite_faculty ' + \
                'Values ("{}", "{}", "{}", "{}", "{}")'.format(input_faculty, position, university, email, phone)
        cursor.execute(sql3)
        sql4 = 'SELECT * FROM favorite_faculty order by Name'
        cursor.execute(sql4)
        result = cursor.fetchall()
        cursor.execute('commit')
        return result

#widget 6
def mysql_delete_favorite_faculty(input_faculty):
    with db.cursor() as cursor:
        sql1 = 'DELETE FROM favorite_faculty ' + \
                'WHERE trim(Name) = trim("{}")'.format(input_faculty)
        cursor.execute(sql1)
        sql2 = 'SELECT * FROM favorite_faculty order by Name'
        cursor.execute(sql2)
        result = cursor.fetchall()
        cursor.execute('commit')
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
    
