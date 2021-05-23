import pymongo
from typing import Dict

def update_score():
    client = pymongo.MongoClient("mongodb+srv://nguyenvannga1507:nguyenvannga1507@cluster0.faxqo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.get_database("RealEstate")

    user_collection = pymongo.collection.Collection(db, "users")
    list_users = user_collection.find({}, projection=["_id","postWish","historyView"])
    list_users = list(list_users)

    score : Dict[str,Dict[str,int]] = {}

    for user in list_users:
        user_id = str(user["_id"])
        if user_id not in score:
            score[user_id] = {}
        for post_id in user["postWish"]:
            if post_id not in score[user_id]:
                score[user_id][post_id] = 5.0
            else:
                score[user_id][post_id] += 5.0
        for post_id in user["historyView"]:
            if post_id not in score[user_id]:
                score[user_id][post_id] = 1.0
            else:
                score[user_id][post_id] += 1.0

    user_rate_collection = pymongo.collection.Collection(db, "rating")
    list_rates = user_rate_collection.find({}, projection=["postId", "userId", "rating"])
    list_rates = list(list_rates)

    for rate in list_rates:
        user_id = rate["userId"]
        if user_id not in score:
            score[user_id] = {}

        post_id = rate["postId"]
        rating = float(rate["rating"])

        if rating >= 4:
            if post_id in score[user_id]:
                score[user_id][post_id] += rating
            else:
                score[user_id][post_id] = rating
        elif rating <=2:
            if post_id not in score[user_id] or score[user_id][post_id]<5:
                score[user_id][post_id] = rating-3
            else:
                score[user_id][post_id] /= 4-rating

    score_collection = pymongo.collection.Collection(db, "scores")
    for user_id in score:
        score_collection.find_one_and_update(filter={"user_id": user_id},update={"$set": {"score": score[user_id]}}, upsert=True)

    client.close()


update_score()