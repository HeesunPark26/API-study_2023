### ------ import modules
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from utils_sql import execute_select_query, execute_commit_query
from utils_func import _check_tag_and_add, _get_and_return_tag_list, _get_and_return_article_body, _match_user_author
import datetime
import hashlib

### ------ parameters
DB_NAME = 'database.db'

### ------ make flask instance
app = Flask(__name__)

### ------ JWT authentification
app.config['JWT_SECRET_KEY'] = 'SECRET_KEY'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
jwt = JWTManager(app)

### ----- Authentication header
# read the Authentication header from the headers of the request
@app.route('/')
def read_auth_header():
    headers = request.headers
    auth = headers.get("Authorization")
    if auth:
        return jsonify({"Authorization": auth})
    else:
        return jsonify({"message": "ERROR: Unauthorized"}), 401

### ----- Authentication: login
@app.route('/api/users/login', methods = ['POST'])
def login():
    request_user = request.get_json()['user']
    # check if required fields are filled
    required_fields = ['email', 'password']
    for info in required_fields:
        if info not in request_user:
            return jsonify({"message": f"ERROR: Please enter your {info}"})
    
    # check if the user exists in DB
    query = f"SELECT * FROM users WHERE email = '{request_user['email']}'"
    user_db = execute_select_query(DB_NAME, query)
    if len(user_db)==0:
        return jsonify({'message': 'Please check your email address'}), 401
    else:
        user_db = user_db[0]
        hashed_password = hashlib.sha256(request_user['password'].encode("utf-8")).hexdigest()
        if hashed_password == user_db['password']:
            # give access token
            access_token = create_access_token(identity=user_db['email']) # create jwt token
            return jsonify({
                'user': {
                    'email': user_db['email'],
                    'token': access_token,
                    'username': user_db['username'],
                    'bio': user_db['bio'],
                    'image': user_db['image']}
                }), 200

### ----- Registration
@app.route('/api/users', methods = ['POST'])
def registration():
    new_user = request.get_json()['user']
    # check if requried fields are filled
    required_fields = ['email', 'password', 'username']
    for info in required_fields:
        if info not in new_user:
            return jsonify({'message': f'ERROR: Please enter your {info}'})

    # check if username or email already exists
    query_check_email = f"SELECT * FROM users WHERE email = '{new_user['email']}'"
    query_check_username = f"SELECT * FROM users WHERE username = '{new_user['username']}'"
    if len(execute_select_query(DB_NAME, query_check_email)) != 0:
        return jsonify({'message': 'Email already in use'})
    if len(execute_select_query(DB_NAME, query_check_username)) != 0:
        return jsonify({'message': 'Username already in use'})

    # register - save user info to DB
    hashed_password = hashlib.sha256(new_user['password'].encode("utf-8")).hexdigest()
    try:
        execute_commit_query(DB_NAME,
        ("INSERT INTO users (email, password, username) "
        f"VALUES ('{new_user['email']}', '{hashed_password}', '{new_user['username']}')"   
        ))
    except:
        return jsonify({"message": "Registration failed. Please try again"})

    # give response
    registered_user = execute_select_query(
        DB_NAME,f"SELECT * FROM users WHERE email='{new_user['email']}'")[0]

    return jsonify({'user':{
        'email': registered_user['email'],
        'username': registered_user['username']
    }}), 201
    
### ---- Get current user
# reference: https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/
@app.route("/api/user", methods = ["GET"])
@jwt_required()
def get_current_user():
    # Access the identity of the current user with get_jwt_identity
    current_user_email = get_jwt_identity()

    # retrieve user data from DB
    query = f"SELECT * FROM users WHERE email = '{current_user_email}'"
    user_db = execute_select_query(DB_NAME, query)[0]
    access_token = request.headers.get("Authorization")
    return jsonify({
    'user': {
        'email': user_db['email'],
        'token': access_token,
        'username': user_db['username'],
        'bio': user_db['bio'],
        'image': user_db['image']}
    })

### ----- Update user
@app.route('/api/user', methods = ['PUT'])
@jwt_required()
def update_user():
    # Access the identity of the current user with get_jwt_identity
    current_user_email = get_jwt_identity()
    
    fields = request.get_json()['user']
    
    # hash password before updating password
    if 'password' in fields:
        hashed_password = hashlib.sha256(fields['password'].encode("utf-8")).hexdigest()
        fields['password'] = hashed_password

    # to make query including to-be-updated parameters
    # e.g., query_set_l is ["username = xxxx"]
    query_set_l = [f"{f} = '{fields[f]}'" for f in fields.keys()]
    query_set   = ', '.join(query_set_l)
    query = f"UPDATE users SET {query_set} WHERE email = '{current_user_email}'"
    try:
        execute_commit_query(DB_NAME, query)
    except:
        return jsnonify({"message": "Update user failed. Please try again."})

    # retrieve user data from DB
    query = f"SELECT * FROM users WHERE email = '{current_user_email}'"
    user_db = execute_select_query(DB_NAME, query)[0]
    access_token = request.headers.get("Authorization")
    return jsonify({
    'user': {
        'email': user_db['email'],
        'token': access_token,
        'username': user_db['username'],
        'bio': user_db['bio'],
        'image': user_db['image']}
    })

### ----- Get profile
@app.route('/api/profiles/<string:username>', methods = ['GET'])
@jwt_required(optional=True)
def get_profile(username):
    current_user_email = get_jwt_identity()
    
    # check if the user exists
    user_profile = execute_select_query(DB_NAME, f"SELECT bio, image FROM users WHERE username = '{username}'")
    if len(user_profile)==0:
        return jsonify({'message': f"No user with username '{username}'"})
    else: user_profile = user_profile[0]
    
    # if authorized user
    if current_user_email:
        ### check if already following
        query = (
            "SELECT * FROM followers "
            f"WHERE (follower_id = (SELECT id FROM users WHERE email='{current_user_email}')) "
            f"AND (followed_id = (SELECT id FROM users WHERE username='{username}'));"
        )
        follow_relationship = execute_select_query(DB_NAME, query)
        following = False if len(follow_relationship)==0 else True
    else:
        following=False
    
    return jsonify({'profile': {
        'username': username,
        'bio': user_profile['bio'],
        'image': user_profile['image'],
        'following': following
    }})

### ----- Follow & Unfollow user
@app.route('/api/profiles/<string:username>/follow', methods = ['POST', 'DELETE'])
@jwt_required()
def follow_and_unfollow_user(username):
    # Follow user 
    if request.method == 'POST':
        # Access the identity of the current user with get_jwt_identity
        current_user_email = get_jwt_identity()

        # check if the user exists
        user_profile = execute_select_query(DB_NAME, f"SELECT bio, image FROM users WHERE username = '{username}'")
        if len(user_profile)==0:
            return jsonify({'message': f"No user with username '{username}'"})
        else: user_profile = user_profile[0]
        
        # check if already following -> if not, follow!
        query = (
            "SELECT * FROM followers "
            f"WHERE (follower_id = (SELECT id FROM users WHERE email='{current_user_email}')) "
            f"AND (followed_id = (SELECT id FROM users WHERE username='{username}'));"
        )
        follow_relationshp = execute_select_query(DB_NAME, query)
        # if not following now:
        if len(follow_relationshp) == 0:
            query = (
                "INSERT INTO followers (follower_id, followed_id) "
                f"VALUES ((SELECT id FROM users WHERE email='{current_user_email}'),(SELECT id FROM users WHERE username='{username}'))"
                )
            execute_commit_query(DB_NAME, query)
        # if already following now:
        else:
            return jsonify({'message': f"You are already following '{username}'"})
        
        return jsonify({'profile': {
            'username': username,
            'bio': user_profile['bio'],
            'image': user_profile['image'],
            'following': True
        }})

    # Unfollow user
    elif request.method == 'DELETE':
        # Access the identity of the current user with get_jwt_identity
        current_user_email = get_jwt_identity()
        
        # check if the user exists
        user_profile = execute_select_query(DB_NAME, f"SELECT bio, image FROM users WHERE username = '{username}'")
        if len(user_profile)==0:
            return jsonify({'message': f"No user with username '{username}'"})
        else: user_profile = user_profile[0]
        
        ## check if already following
        query = (
            "SELECT * FROM followers "
            f"WHERE (follower_id = (SELECT id FROM users WHERE email='{current_user_email}')) "
            f"AND (followed_id = (SELECT id FROM users WHERE username='{username}'));"
        )
        follow_relationship = execute_select_query(DB_NAME, query)
        # if not following now:
        if len(follow_relationship) == 0:
            return jsonify({'message': f"Cannot unfollow: you are not following '{username}'"})
        # if already following now:
        else:
            query = (
                "DELETE FROM followers "
                f"WHERE (follower_id = (SELECT id FROM users WHERE email='{current_user_email}')) "
                f"AND (followed_id = (SELECT id FROM users WHERE username='{username}'));"            
            )
            execute_commit_query(DB_NAME, query) 
            return jsonify({'profile': {
                'username': username,
                'bio': user_profile['bio'],
                'image': user_profile['image'],
                'following': False
            }})


### ----- Get article
@app.route('/api/articles/<string:slug>', methods = ['GET'])
def get_article(slug):
    try:
        article_body = _get_and_return_article_body(slug)
    except:
        return jsonify({"message": "No article with this name"})
    return jsonify({"article": article_body})

### ----- Create article
@app.route('/api/articles', methods = ['POST'])
@jwt_required()
def create_article():
    # Access the identity of the current user with get_jwt_identity
    current_user_email = get_jwt_identity()
    # get user info
    user_profile = execute_select_query(
        DB_NAME, f"SELECT * FROM users WHERE email = '{current_user_email}'")[0]
    
    new_article = request.get_json()['article']
    
    # check if required fields are filled
    required_fields = ['title', 'description', 'body']
    for info in required_fields:
        if info not in new_article:
            return jsonify({"message": f"ERROR: Please enter your {info}"})

    title = new_article['title']
    description = new_article['description']
    body = new_article['body']

    # make slug with title
    from slugify import slugify
    slug = slugify(title)

    # create article
    query = (
        "INSERT INTO posts "
        "(slug, title, description, body, favorited, favoritesCount, author_id) "
        f"VALUES ('{slug}', '{title}', '{description}', '{body}', 'False', 0, {user_profile['id']})")
    try:
        execute_commit_query(DB_NAME, query)
    except:
        return jsonify({"message": "Error during generating post. Please check your title."})
    # if there is tag
    if "tagList" not in new_article:
        article_body = _get_and_return_article_body(slug)
        return jsonify({"article": article_body})
    else:
        tagList = new_article['tagList']
        for tag in tagList:
            tag_info = _check_tag_and_add(tag)
            # with tag id, make tag relationship
            tag_id = tag_info[0]['tag_id']
            execute_commit_query(
                DB_NAME, f"INSERT INTO tag_rel (tag_id, slug) VALUES ({tag_id},'{slug}')")
        article_body = _get_and_return_article_body(slug)
        return jsonify({"article": article_body})

### ----- Update article
@app.route('/api/articles/<string:slug>', methods = ['PUT'])
@jwt_required()
def update_article(slug):
    # check the slug is correct
    try:
        article_body = _get_and_return_article_body(slug)
    except:
        return jsonify({"message": "No article with this name"})

    # Access the identity of the current user with get_jwt_identity
    current_user_email = get_jwt_identity()

    # check if this user is the author of the post
    match = _match_user_author(current_user_email, slug)
    if match == False:
        return jsonify({"message": "You don't have permission to edit this article. You are not the author."})

    update_info = request.get_json()['article']

    # if taglist is changed
    if "tagList" in update_info:
        tagList = update_info['tagList']
        old_tag_info = execute_select_query(
            DB_NAME, f"SELECT tag_name FROM tags WHERE tag_id in (SELECT tag_id FROM tag_rel WHERE slug='{slug}')")
        old_tagList = [tags['tag_name'] for tags in old_tag_info]

        # delete and add tags 
        del_tags = list(set(old_tagList).difference(set(tagList)))
        add_tags = list(set(tagList).difference(set(old_tagList)))

        for del_t in del_tags:
            execute_commit_query(
                DB_NAME, f"DELETE FROM tag_rel WHERE tag_id = (SELECT tag_id FROM tags WHERE tag_name = '{del_t}')")
        for add_t in add_tags:
            tag_info = _check_tag_and_add(add_t)
            execute_commit_query(
                DB_NAME, f"INSERT INTO tag_rel (tag_id, slug) VALUES ({tag_info[0]['tag_id']},'{slug}')")

    # to make query including to-be-updated parameters except for taglist
    query_set_l = [f"{p} = '{update_info[p]}'" for p in update_info.keys() if p != 'tagList']
    # e.g., query_set_l is ["title = 'how to train dog'"]

    # change slug if title is changed
    new_slug = None
    if "title" in update_info:
        from slugify import slugify
        new_slug = slugify(update_info["title"])
        query_set_l.append(f"slug = '{new_slug}'")

        # update tag relationship with new slug
        execute_commit_query(DB_NAME, f"UPDATE tag_rel SET slug = '{new_slug}' WHERE slug is '{slug}'")
    
    if len(query_set_l) > 0:
        query_set = ", ".join(query_set_l)
        try:
            execute_commit_query(DB_NAME, f"UPDATE posts SET {query_set} WHERE slug is '{slug}'")
        except:
            return jsonify({"message": "Error during generating post. Please check your title."})
    
    # return article
    slug = slug if new_slug is None else new_slug
    new_article_body = _get_and_return_article_body(slug)
    return new_article_body

### ----- Delete article
@app.route('/api/articles/<string:slug>', methods = ['DELETE'])
@jwt_required()
def delete_article(slug):
    # check the slug is correct
    try:
        article_body = _get_and_return_article_body(slug)
    except:
        return jsonify({"message": "No article with this name"})

    # Access the identity of the current user with get_jwt_identity
    current_user_email = get_jwt_identity()
    match = _match_user_author(current_user_email, slug)
    if match == False:
        jsonify({"message": "You don't have permission to delete this article. You are not the author."})

    # delete 
    execute_commit_query(DB_NAME, f"DELETE FROM posts WHERE slug = '{slug}'")
    execute_commit_query(DB_NAME, f"DELETE FROM tag_rel WHERE slug= '{slug}'")
    return jsonify({"message": "Article deleted"})

if __name__ == '__main__':
    app.run(debug=True) # debug=True: I don't have to restart server.