from neo4j import GraphDatabase

db = GraphDatabase.driver("bolt://localhost:7687", auth = ("neo4j", "Hi!ch7young"))

session = db.session(database="academicworld")

def neo4j_get_university(input_value):
    q = 'MATCH (a:INSTITUTE) WHERE a.name contains "{}" RETURN a'.format(input_value)
    #q = 'MATCH (a:INSTITUTE) WHERE a.name contains "illinois" RETURN a'
    response = list(session.run(q))
    return response

def neo4j_get_all_keywords():
    q = 'Match (k: KEYWORD) Return k.name as name'
    response = list(session.run(q))
    return response

#widget1
def neo4j_get_professor_university(input_keyword, n):
    q = 'MATCH (k: KEYWORD)<-[: LABEL_BY]-(p: PUBLICATION)<-[: PUBLISH]-(f: FACULTY)-[: AFFILIATION_WITH]->(u: INSTITUTE) ' + \
        'WHERE k.name = "{}" '.format(input_keyword) + \
        'MATCH (f)-[i: INTERESTED_IN]->(k) ' + \
        'WITH f.name as fname, u.name as uname, i.score as score, count(p.id) as n_pubs ' + \
        'ORDER BY n_pubs desc limit {} '.format(n) + \
        'RETURN fname, uname, n_pubs, score'
    records = session.run(q)
    result = [r.data() for r in records]
    return result

#session.close()
