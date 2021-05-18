import datetime
import database.database as DB


def findCandidate(new_bds):
    """
    FIND CANDIDATES WHICH IS USE FOR CHECKING DUPLICATE NEW REAL ESTATE
    :param new_bds: A DOCUMENT THAT IS A NEW REAL ESTATE - JSON
    :return: CANDIDATES - ARRAY
    """
    FACTOR_LOWER_PRICE = 0.6
    FACTOR_HIGHER_PRICE = 2.35
    FACTOR_LOWER_SQUARE = 0.6
    FACTOR_HIGHER_SQUARE = 1.5
    db = DB.connect_to_database()
    bds_collection = db[DB.COLLECTION_NAME]
    year_ago = datetime.datetime.strptime(new_bds['time'], "%d/%m/%Y") - datetime.timedelta(days=365)
    print(year_ago)
    resultFind = bds_collection.find(
        filter={
            "$expr": {"$gt": [{"$dateFromString": {"dateString": "$time", "format": "%d/%m/%Y"}}, year_ago]},
            # Insert filter type in here,
            "district": {"$regex": new_bds['district'], "$options": "i"},
            "wards": {"$regex": new_bds['wards'], "$options": "i"},
            "price": {"$gte": float(new_bds['price']) * FACTOR_LOWER_PRICE, "$lte": float(new_bds['price']) * FACTOR_HIGHER_PRICE},
            "square": {"$gte": float(new_bds['square']) * FACTOR_LOWER_SQUARE, "$lte": float(new_bds['square']) * FACTOR_HIGHER_SQUARE}
        },
        # ADD FIELDS WHICH YOU WANT TO RETURN IN FUNCTION
        projection=[
            "_id"
        ]
    )

    result = []
    i = 1
    num_of_candidate = resultFind.count()
    while i <= num_of_candidate:
        result.append(resultFind.next())
        i += 1

    return result




