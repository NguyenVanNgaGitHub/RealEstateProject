from flask import Blueprint, request, flash
from ai.recommend.simple_model import SimpleRecommendSystem
from ai.search_engine.real_estate_search_engine import RealEstateSearchEngine
from serverai.config_const import MessageCode
from ai.search_engine.data import get_data_by_ids
import logging
import json
import config as CONFIG
import os
import time
import pickle
bp = Blueprint('ai', __name__, url_prefix='/ai')


@bp.route('/debug', methods=('GET', 'POST'))
def debug():
    return 'Debug in here'


@bp.route('get_recommend_posts', methods=['GET', 'POST'])
def get_recommend_posts():
    if request.method == 'POST':
        data = request.json
        if data is None:
            flash("Missing parameter")
            return {
                "code": MessageCode.CODE_MISSING_PARAMETER
            }
        post = data['post']
        number_post = int(data['num_post'])
        if post is None or number_post is None:
            flash('Null Data')
            return {
                'code': MessageCode.CODE_ERROR_DATA
            }

        start = time.time()
        recommend_sys = SimpleRecommendSystem(post=post, num_of_recommend_post=number_post)
        posts = recommend_sys.find_recommend_posts(online=True)
        end = time.time()
        print('Find recommend time:', end-start)

        return {
            'codeMess': MessageCode.CODE_OK,
            'data': posts
        }


search_engine = RealEstateSearchEngine()
@bp.route('search', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        find_str = request.form['keyword']

        if find_str is None:
            flash('Missing parameter')
            return {
                'code': MessageCode.CODE_MISSING_PARAMETER,
                'data': [

                ]
            }
        start = time.time()
        posts_id = search_engine.find(find_str)
        recommend_posts = get_data_by_ids(ids=posts_id.keys())
        for index, post in enumerate(recommend_posts):
            recommend_posts[index]['_id'] = str(post['_id'])
        end = time.time()
        print('Search Time:', end-start)
        return {
            'code': MessageCode.CODE_OK,
            'data': recommend_posts
        }