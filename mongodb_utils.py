import pymongo

conn = pymongo.MongoClient() #MongoClient('mongodb://localhost:27017')

db = conn.academicworld

def mongodb_get_all_keywords():
    results = db.publications.aggregate([{"$unwind": "$keywords"}, 
                                         {"$project": {"_id": 0, "name": "$keywords.name"}}, 
                                         {"$group": {"_id": "$name"}},
                                         {"$sort": {"_id": 1}}])
    return results

#widget 3
def mongodb_topn_publications(input_keyword, n):
    response = db.publications.aggregate([{"$unwind": "$keywords"}, 
                                         {"$match": {"keywords.name": input_keyword}}, 
                                         {"$sort": {"numCitations": -1}}, 
                                         {"$limit": n}, 
                                         {"$project": {"_id": 0, "title": 1, "venue": 1, "year": 1, "numCitations": 1}}])
    result = []
    for r in response:
        new_r = {}
        new_r["title"] = r["title"]
        if r["venue"] is None:
            new_r["venue"] = 'None'
        else:
            new_r["venue"] = r["venue"]
        if r["year"] is None:
            new_r["year"] = 'None'
        else:
            new_r["year"] = r["year"] 
        if r["numCitations"] is None:
            new_r["numCitations"] = 'None'
        else:
            new_r["numCitations"] = r["numCitations"]   
        result.append(new_r)
    return result


# unused
# #widget5
# def mongodb_update_favorites(input_name, action, collection):
#     if collection == 'faculty':
#         db.faculty.update_one({"name":input_name}, [{"$set":{"favorite":{"$eq":[action,"Add"]}}}])
#         result = db.faculty.find({'favorite':true})
#     else:
#         db.faculty.updateMany({"affiliation.name":input_name}, [{"$set":{"affiliation.favorite":{"$eq":[action,"Add"]}}}])
#         result = db.faculty.find({'favorite':true})
#     return result

# def mongodb_reset_favorites():
#     query1 = db.faculty.update({}, {"$unset": {"favorite":1}} , {"multi": "true"})



#unused
def mongodb_get_university(input_value):
    results = db.faculty.aggregate([{"$match": {"affiliation.name": { "$regex": input_value, "$options": 'i' }}}, 
                                    {"$project": { "affiliation.name": 1,"_id": 0}},
                                    {"$group": {"_id": "$affiliation.name", "name": {"$addToSet": "$affiliation.name"}}}, 
                                    {"$project": {"_id": 0, "name":1}}])

    return results
