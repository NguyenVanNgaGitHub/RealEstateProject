from database.database import DataBase



def create_index_search(field_name):
    db = DataBase()
    db.create_indexes_search(field_name)



if __name__ == "__main__":
    create_index_search(['district', 'wards'])

