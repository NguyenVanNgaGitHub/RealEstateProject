from ai.data.data import get_user_by_id, get_item_by_id, get_data
import numpy as np
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
from sklearn.ensemble import RandomForestRegressor


def get_recommend_list(userId):
    user = get_user_by_id(userId)
    wishlist = user.get('postWish')
    view_history = user.get('historyView')

    data = []
    columns_get = {'type': 1, 'wards': 1, 'district': 1, 'province': 1, 'square': 1, 'price': 1}
    for id in wishlist:
        estate = get_item_by_id(id)
        data.append({'id': id,
                     'type': estate.get('type'),
                     'wards': estate.get('wards'),
                     'district': estate.get('district'),
                     'province': estate.get('province'),
                     'square': estate.get('square'),
                     'price': estate.get('price'),
                     'score': 100
                     })
    view_history_estates = [get_item_by_id(id) for id in view_history.keys()]
    max_times = max(view_history.values())
    for i, (id, times) in enumerate(view_history.items()):
        estate = view_history_estates[i]
        data.append({'id': id,
                     'type': estate.get('type'),
                     'wards': estate.get('wards'),
                     'district': estate.get('district'),
                     'province': estate.get('province'),
                     'square': estate.get('square'),
                     'price': estate.get('price'),
                     'score': 50 / max_times * times
                     })
    data = pd.DataFrame(data)
    data.set_index('id', inplace=True)

    y = data.score
    X = data.drop(['score'], axis=1)

    candidate = []
    for column in ['type', 'province']:
        for value in data[column].unique():
            for estate in get_data({column: value}, columns_get, limit=5):
                candidate.append({'id': str(estate.get('_id')),
                                  'type': estate.get('type'),
                                  'wards': estate.get('wards'),
                                  'district': estate.get('district'),
                                  'province': estate.get('province'),
                                  'square': estate.get('square'),
                                  'price': estate.get('price'),
                                  })
    candidate = pd.DataFrame(candidate)
    candidate.set_index('id', inplace=True)
    candidate.drop_duplicates(inplace=True)
    candidate.drop(data.index,inplace=True)

    oh_cols = ['type', 'wards', 'district', 'province']
    oh_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
    oh_cols_train = pd.DataFrame(oh_encoder.fit_transform(X[oh_cols]))
    oh_cols_candidate = pd.DataFrame(oh_encoder.transform(candidate[oh_cols]))
    oh_cols_train.index = X.index
    oh_cols_candidate.index = candidate.index
    num_X_train = X.drop(oh_cols, axis=1)
    num_X_candidate = candidate.drop(oh_cols, axis=1)
    oh_X_train = pd.concat([num_X_train, oh_cols_train], axis=1)
    oh_X_candidate = pd.concat([num_X_candidate, oh_cols_candidate], axis=1)
    model = RandomForestRegressor(n_estimators=100, random_state=20173448)
    model.fit(oh_X_train, y)
    predicts = model.predict(oh_X_candidate)
    best_index = np.flip(np.argsort(predicts))
    result = [oh_X_candidate.index[i] for i in best_index[:5]]
    print(result)
    return result


get_recommend_list('60967e6e26eabee1ecc5b4e1')
