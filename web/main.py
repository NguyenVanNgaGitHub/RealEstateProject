from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for, flash
from pymongo import MongoClient
from flask_paginate import Pagination, get_page_args
from bson.objectid import ObjectId
from bson.json_util import dumps,loads
from ai.search_engine.data import get_data_by_ids
from ai.search_engine.real_estate_search_engine import RealEstateSearchEngine
from ai.search_engine.invert_index import InvertIndex
from ai.search_engine.frequence_dict import FrequenceDict
from ai.search_engine.information_retrival import InformationRetrival
from ai.search_engine.create_real_estate_invert_index import create_real_estate_invert_index

search_engine = RealEstateSearchEngine()
app = Flask(__name__)
client = MongoClient('mongodb+srv://nguyenvannga1507:nguyenvannga1507@cluster0.faxqo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
app.secret_key = 'super secret key'
db = client.RealEstate
batdongsan = db.RealEstateRaw
users = db.users
comments = db.comments
ratingPost = db.rating
historyView = db.historyView
@app.route('/')
def home():
    if 'user' in session:
        user = loads(session["user"])
        postWish = user["postWish"]
        # model goi y tin
        bds = batdongsan.find().limit(60)
        return render_template('home.html', user = loads(session['user']), bds = bds, postWish=postWish)
    else:
        bds = batdongsan.find().limit(60)
        return render_template('home.html', bds = bds, postWish=[])
@app.route('/testData', methods = ['GET'])
def test():
    items = batdongsan.find({})
    return render_template('1.html', items = items)

@app.route('/dangki', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user = {
            "name" : name,
            "email" : email,
            "password" : password,
            "postWish" : [],
            "historyView" : {}
        }
        users.insert_one(user)
        flash('Đăng kí thành công.Vui lòng đăng nhập')
        return redirect(url_for('signIn'))
    else:
        return render_template('register.html')

@app.route('/dangnhap', methods = ['POST', 'GET'])
def signIn():
    if request.method == 'POST' :
        email = request.form['email']
        password = request.form['password']
        allUsers = users.find()
        for user in allUsers:
            if (user['email'] == email and user['password'] == password):
                session['user'] = dumps(user)
                break
        if ('user' in session):
            return redirect(url_for('home'))
        else :
            flash('Email hoặc password không chính xác')
            return render_template('signin.html')
    else :
        return render_template('signin.html')

@app.route('/dangxuat', methods = ['GET'])
def logOut():
    session.pop('user')
    return redirect(url_for('home'))


@app.route('/xemTin', methods = ['GET', 'POST'])
def viewPost():
    if request.method == 'GET':
        page, per_page, offset = get_page_args(page_parameter='page',
                                               per_page_parameter='per_page')
        bds = batdongsan.find()
        bds = bds.skip(offset).limit(per_page)
        bds = list(bds)
        total = batdongsan.count()
        pagination = Pagination(page=page, per_page=per_page, total=total,
                                css_framework='bootstrap4')
        if 'user' in session:
            user = loads(session["user"])
            postWish = user["postWish"]
            return render_template('listHouse.html', user=loads(session['user']), bds=bds, postWish= postWish,
                                   page=page,
                                   per_page=per_page,
                                   pagination=pagination)
        else:
            return render_template('listHouse.html', bds=bds, postWish = [],
                                   page=page,
                                   per_page=per_page,
                                   pagination=pagination)

    else:
        sq_from = request.form['sq_from']
        sq_to = request.form['sq_to']
        pr_from = request.form['pr_from']
        pr_to = request.form['pr_to']
        category = request.form['category']
        location = request.form['location']
        page, per_page, offset = get_page_args(page_parameter='page',
                                               per_page_parameter='per_page')
        bds = batdongsan.find({"$and" : [{"type" : {"$regex": category}}, {"district" : {"$regex": location}}, {"square" : {"$lt": float(sq_to)}}, {"square" : {"$gt": float(sq_from)}}, {"price" : {"$lt": float(pr_to)}}, {"price": {"$gt" : float(pr_from)}}]})
        bds = bds.skip(offset).limit(per_page)
        bds = list(bds)
        total = batdongsan.count({"$and" : [{"type" : {"$regex": category}}, {"district" : {"$regex": location}}, {"square" : {"$lt": float(sq_to)}}, {"square" : {"$gt": float(sq_from)}}, {"price" : {"$lt": float(pr_to)}}, {"price": {"$gt" : float(pr_from)}}]})
        pagination = Pagination(page=page, per_page=per_page, total=total,
                                css_framework='bootstrap4')
        if 'user' in session:
            user = loads(session["user"])
            postWish = user["postWish"]
            return render_template('listHouse.html',user=loads(session['user']), bds=bds, postWish=postWish,
                           page=page,
                           per_page=per_page,
                           pagination=pagination)
        else:
            return render_template('listHouse.html', bds=bds, postWish=[],
                                   page=page,
                                   per_page=per_page,
                                   pagination=pagination)


@app.route('/danh-sach-yeu-thich')
def viewWishList():
    if 'user' in session :
        user = loads(session["user"])
        postWish = user["postWish"]
        listPostWish = []
        if (len(postWish) > 0):
            for id in postWish:
                post = batdongsan.find_one({"_id": ObjectId(id)})
                listPostWish.append(post)

        page, per_page, offset = get_page_args(page_parameter='page',
                                               per_page_parameter='per_page')
        total = len(listPostWish)
        listPostWish = listPostWish[offset: offset + per_page]
        pagination = Pagination(page=page, per_page=per_page, total=total,
                                    css_framework='bootstrap4')
        return render_template('wishList.html',  user=loads(session['user']), list = listPostWish, page=page,
                           per_page=per_page,
                           pagination=pagination)
    else :
        return render_template('signin.html')

@app.route('/delete-wishlist/<post_id>', methods = ['POST', 'GET'])
def delete(post_id) :
    if 'user' in session:
        users.update_one({"_id": loads(session['user'])['_id']},{"$pull": {"postWish": post_id}})
        user = loads(session["user"])
        postWish = user["postWish"]
        postWish.remove(post_id)
        user["postWish"] = postWish
        session["user"]=dumps(user)
        flash('Xoá thành công')
        return redirect(url_for('viewWishList'))
    else :
        return render_template('signin.html')

@app.route('/add-wishlist/<post_id>', methods = ['POST', 'GET'])
def addWishList(post_id) :
    if 'user' in session:
        user = loads(session["user"])
        postWish = user['postWish']
        if post_id in postWish:
            flash("Bất động sản đã có trong danh sách yêu thích")
        else:
            users.update_one({"_id": loads(session['user'])['_id']},{"$push": {"postWish": post_id}})
            postWish = user["postWish"]
            postWish.append(post_id)
            user["postWish"] = postWish
            session["user"] = dumps(user)
            flash('Đã thêm vào danh sách yêu thích')
        return redirect(url_for('viewDetail', id=post_id))
    else :
        return render_template('signin.html')

@app.route('/xem-chi-tiet/<id>')
def viewDetail(id):
    print(id)
    if 'user' in session:
        isPostWish = 0
        data = batdongsan.find_one( { '_id' : ObjectId(id)} )
        commentPost = comments.find({ "postId" : id})
        user = users.find_one({"_id": loads(session['user'])['_id']})
        if id in user['postWish']:
            isPostWish = 1
        historyView = user['historyView']
        print(historyView)
        if id in historyView:
            users.update_one({"_id": loads(session['user'])['_id']}, { "$inc": {"historyView." + id : 1 } })
        else:
            users.update_one({"_id": loads(session['user'])['_id']}, {"$set": {"historyView." + id : 1}})
        return render_template('detail.html', user=loads(session['user']), data = data, commentPost=commentPost, isPostWish=isPostWish)
    else:
        return render_template('signin.html')

# search text
@app.route('/search', methods=['GET'])
def searchPost():
    search_str = request.args.get('keyword')
    recomend_docs = search_engine.find(search_str)
    recomend_real_estates = get_data_by_ids(ids=recomend_docs.keys(), client=client)

    if "user" in session:
        user = loads(session["user"])
        postWish = user["postWish"]
        return render_template('listHouse.html', user=loads(session['user']), bds=recomend_real_estates, postWish=postWish,
                               page=1,
                               per_page=100,
                               pagination=1)
    else:
        return render_template('listHouse.html', bds=recomend_real_estates,postWish=[],
                               page=1,
                               per_page=100,
                               pagination=1)

@app.route('/postComment', methods=['POST'])
def comment():
    if request.method == 'POST' :
        contentComment = request.form['comment']
        postId = request.form['post_id']
        userId = str(loads(session['user'])['_id'])
        userName = loads(session['user'])['name']
        comment = {
            "postId" : postId,
            "userId" : userId,
            "userName" : userName,
            "contentComment" : contentComment,
            "time" : datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        }
        comments.insert_one(comment)
        flash("Gửi bình luận thành công")
        return redirect(url_for('viewDetail', id = request.form['post_id']))

#rating
@app.route('/rating', methods=['POST'])
def rating():
    if request.method == 'POST':
        value = request.form['data']
        postId = request.form['postId']
        userId = str(loads(session['user'])['_id'])
        postRating = ratingPost.find_one({
            "userId": userId,
            "postId" : postId
        })
        if(postRating) :
            ratingPost.update_one({
                "userId": userId,
                "postId": postId
            },{
                "$set": {"rating" : value}
            })
        else :
            obj = {
                "postId" : postId,
                "userId" : userId,
                "rating" : value
            }
            ratingPost.insert_one(obj)


if __name__ == '__main__':
    app.run(debug=True)
