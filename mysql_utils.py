import pymysql

db = pymysql.connect(host='localhost',
                user='root',
                password='test_root',
                database='academicworld',
                charset='utf8mb4',
                port=3306,
                cursorclass=pymysql.cursors.DictCursor)

#create indexes on "keyword name", "faculty name", and "publication title" to speed up the performance of select statement.
"""
def create_index():
     with db.cursor() as cursor:
        sql = 'CREATE INDEX idx_keyword_name ON keyword(name)'
        cursor.execute(sql)
        sql = 'CREATE INDEX idx_faculty_name ON faculty(name)'
        cursor.execute(sql)
        sql = 'CREATE INDEX idx_publication_title ON publication(title)'
        cursor.execute(sql)
        cursor.execute('commit')
"""

def mysql_get_all_keywords():
    with db.cursor() as cursor:
        sql = 'select name from keyword order by name'
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

def mysql_get_all_favorite_faculties():
    with db.cursor() as cursor:
        sql = 'show tables like "favorite_faculty"'
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) > 0:
                sql = 'select * from favorite_faculty order by name'
                cursor.execute(sql)
                result = cursor.fetchall()
        return result

def mysql_get_all_favorite_publication():
    with db.cursor() as cursor:
        sql = 'show tables like "favorite_publication"'
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) > 0:
                sql = 'select * from favorite_publication order by title'
                cursor.execute(sql)
                result = cursor.fetchall()
        return result
    
#widget2 using prepared statement
def mysql_year_publication(keyword):
        with db.cursor() as cursor:
                sql = 'select p.year as year, count(p.id) as n_pubs ' + \
                'from keyword k join publication_keyword pk on k.id = pk.keyword_id ' + \
                'join publication p on pk.publication_id = p.id ' + \
                'where k.name = %s ' + \
                'group by p.year ' + \
                'order by year'
                cursor.execute(sql,(keyword))
                result = cursor.fetchall()
                return result


#widget5 using transaction technology & prepared statement
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
                'where trim(f.name) = trim(%s)'
        cursor.execute(sql2,(input_faculty))
        result = cursor.fetchall()
        if len(result) > 0:
                position = result[0]["position"]
                university = result[0]["univ"]
                email = result[0]["email"]
                phone = result[0]["phone"]
                sql3 = 'INSERT IGNORE INTO favorite_faculty ' + \
                        'Values (%s, %s, %s, %s, %s)'
                cursor.execute(sql3, (input_faculty, position, university, email, phone))
        sql4 = 'SELECT * FROM favorite_faculty order by Name'
        cursor.execute(sql4)
        result = cursor.fetchall()
        cursor.execute('commit')
        return result


def mysql_delete_favorite_faculty(input_faculty):
    with db.cursor() as cursor:
        sql1 = 'DELETE FROM favorite_faculty ' + \
                'WHERE trim(Name) = trim(%s)'
        cursor.execute(sql1,(input_faculty))
        sql2 = 'SELECT * FROM favorite_faculty order by Name'
        cursor.execute(sql2)
        result = cursor.fetchall()
        cursor.execute('commit')
        return result

#widget 6 using transaction technology & prepared statement
def mysql_add_favorite_publication(input_publication):
    with db.cursor() as cursor:
        sql1 = 'CREATE TABLE IF NOT EXISTS favorite_publication (' + \
                'Title varchar(512) not null, ' + \
                'Author varchar(512), ' + \
                'Year varchar(512),' + \
                'Venue varchar(512),' + \
                'primary key(Title))'
        cursor.execute(sql1)
        sql2 = 'select title, f.name as name, venue, year ' + \
                'from publication p join faculty_publication fp on p.id = fp.publication_id ' + \
                'join faculty f on fp.faculty_id = f.id ' + \
                'where trim(title) = trim(%s)'
        cursor.execute(sql2,(input_publication))
        result = cursor.fetchall()
        if len(result) > 0:
                title = result[0]["title"]
                year = result[0]["year"]
                venue = result[0]["venue"]
                name = "" 
                for r in result:
                        name += r["name"] + ", "
                sql3 = 'INSERT IGNORE INTO favorite_publication ' + \
                        'Values (%s, %s, %s, %s)'
                cursor.execute(sql3,(title, name, year, venue))
        sql4 = 'SELECT * FROM favorite_publication order by title'
        cursor.execute(sql4)
        result = cursor.fetchall()
        cursor.execute('commit')
        return result


def mysql_delete_favorite_publication(input_publication):
    with db.cursor() as cursor:
        sql1 = 'DELETE FROM favorite_publication ' + \
                'WHERE trim(Title) = trim(%s)'
        cursor.execute(sql1,(input_publication))
        sql2 = 'SELECT * FROM favorite_publication order by Title'
        cursor.execute(sql2)
        result = cursor.fetchall()
        cursor.execute('commit')
        return result
