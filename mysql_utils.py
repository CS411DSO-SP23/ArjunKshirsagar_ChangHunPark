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