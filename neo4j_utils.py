from neo4j import GraphDatabase

db = GraphDatabase.driver("bolt://localhost:7687", auth = ("neo4j", "Hi!ch7young"))
# db = GraphDatabase.driver("bolt://localhost:7687", auth = ("neo4j", "test_root"))

def neo4j_get_all_keywords():
    session = db.session(database="academicworld")
    q = 'MATCH (k: KEYWORD) RETURN k.name as name'
    response = list(session.run(q))
    session.close()
    return response

def neo4j_get_all_universties():
    session = db.session(database="academicworld")
    q = 'MATCH (u: INSTITUTE) RETURN u.name as name order by name'
    response = list(session.run(q))
    session.close()
    return response

def neo4j_get_all_faculty():
    session = db.session(database="academicworld")
    q = 'MATCH (f: FACULTY) RETURN f.name as name order by name'
    response = list(session.run(q))
    session.close()
    return response

#widget1
def neo4j_get_professor_university(input_keyword, n):
    session = db.session(database="academicworld")
    q = 'MATCH (k: KEYWORD)<-[: LABEL_BY]-(p: PUBLICATION)<-[: PUBLISH]-(f: FACULTY)-[: AFFILIATION_WITH]->(u: INSTITUTE) ' + \
        'WHERE k.name = "{}" '.format(input_keyword) + \
        'MATCH (f)-[i: INTERESTED_IN]->(k) ' + \
        'WITH f.name as fname, u.name as uname, i.score as score, count(p.id) as n_pubs ' + \
        'ORDER BY n_pubs desc limit {} '.format(n) + \
        'RETURN fname, uname, n_pubs, score'
    records = session.run(q)
    result = [r.data() for r in records]
    session.close()
    return result

#widget 4
def neo4j_get_university_keywords(input_university, n):
    session = db.session(database="academicworld")
    q = 'MATCH (u: INSTITUTE)<-[:AFFILIATION_WITH]-(f: FACULTY)-[:PUBLISH]->(p: PUBLICATION)-[l: LABEL_BY]->(k: KEYWORD) ' + \
        'WHERE u.name = "{}" '.format(input_university) + \
        'RETURN k.name as name, round(sum(l.score)) as total_score ' + \
        'ORDER BY total_score desc ' + \
        'LIMIT {}'.format(n)
    records = session.run(q)
    result = [r.data() for r in records]
    session.close()
    return result