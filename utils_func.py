
from utils_sql import execute_select_query, execute_commit_query

### ----- func get article and return article body

def _check_tag_and_add(tag_name, DB_NAME='database.db'):
    # check if tag is already in database
    tag_info = execute_select_query(DB_NAME, f"SELECT * FROM tags WHERE tag_name = '{tag_name}'")
    if len(tag_info) == 0: # if there is no tag, create the tag and get id
        execute_commit_query(DB_NAME, f"INSERT INTO tags (tag_name) VALUES ('{tag_name}')")
        tag_info = execute_select_query(DB_NAME, f"SELECT * FROM tags WHERE tag_name = '{tag_name}'")
    return tag_info
def _get_and_return_tag_list(slug, DB_NAME='database.db'):
    tagList = []
    tags = execute_select_query(DB_NAME, f"SELECT tag_id FROM tag_rel WHERE slug = '{slug}'")
    if len(tags) == 0:
        return tagList
    else:
        for tag_id in tags:
            tag_name = execute_select_query(
                DB_NAME, f"SELECT tag_name FROM tags WHERE tag_id = {tag_id['tag_id']}")[0]
            tagList.append(tag_name['tag_name'])
        return tagList

def _get_and_return_article_body(slug, current_user_email=None, DB_NAME='database.db'):

    # get article
    article = execute_select_query(DB_NAME, f"SELECT * FROM posts WHERE slug = '{slug}'")[0]
    author_id = article['author_id']
    author_profile = execute_select_query(
        DB_NAME,f"SELECT username, bio, image FROM users WHERE id = {author_id}")[0]
    return_dict = {
        "slug": slug,
        "title": article["title"],
        "description": article["description"],
        "body": article["body"],
        "createdAt": article["createdAt"],
        "updatedAt": article["updatedAt"],
        "favorited": article["favorited"],
        "favoritesCount": article["favoritesCount"]
    }
    # get tag list
    tagList = _get_and_return_tag_list(slug)
    return_dict["tagList"] = tagList

    return_dict["author"]= {
        "username": author_profile["username"],
        "bio": author_profile["bio"],
        "image": author_profile["image"],
        "following": False}
        
    if current_user_email is not None:
        # check if following:
        query = (
            "SELECT * FROM followers "
            f"WHERE (follower_id = (SELECT id FROM users WHERE email='{current_user_email}')) "
            f"AND (followed_id = (SELECT id FROM users WHERE id='{author_id}'));"
        )
        follow_relationship = execute_select_query(DB_NAME, query)
        if len(follow_relationship) == 0:
            following = False
        else:
            following = True

        return_dict["author"]["following"] = following
    return return_dict
    
def _match_user_author(current_user_email, slug, DB_NAME='database.db'):
    user_id = execute_select_query(
        DB_NAME, f"SELECT id FROM users WHERE email = '{current_user_email}'")[0]['id']

    author_id = execute_select_query(
        DB_NAME,f"SELECT author_id FROM posts WHERE slug = '{slug}'")[0]['author_id']
    if user_id != author_id:
        return False
    else:
        return True
