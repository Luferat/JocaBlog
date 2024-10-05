
def get_all(mysql):

    sql = '''
        SELECT art_id, art_title, art_resume, art_thumbnail
        FROM article
        WHERE art_status = 'on'
            AND art_date <= NOW()
        ORDER BY art_date DESC;
    '''
    cur = mysql.connection.cursor()
    cur.execute(sql)
    articles = cur.fetchall()
    cur.close()

    return articles


def get_one(mysql, artid):

    sql = '''
        SELECT art_id, art_date, art_title, art_content,
            DATE_FORMAT(art_date, '%%d/%%m/%%Y às %%H:%%i') AS art_datebr,
            sta_id, sta_name, sta_image, sta_description, sta_type,
            TIMESTAMPDIFF(YEAR, sta_birth, CURDATE()) - 
                (DATE_FORMAT(CURDATE(), '%%m%%d') < DATE_FORMAT(sta_birth, '%%m%%d')) AS sta_age
        FROM article
        INNER JOIN staff ON art_author = sta_id
        WHERE art_id = %s
            AND art_status = 'on'
            AND art_date <= NOW();
    '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (artid,))
    article = cur.fetchone()
    cur.close()

    return article


def update_views(mysql, artid):

    sql = '''
        UPDATE article 
            SET art_view = art_view + 1 
        WHERE art_id = %s
    '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (artid,))
    mysql.connection.commit()
    cur.close()

    return True


def get_by_author(mysql, authorid, ignore, limit):

    sql = '''
        SELECT art_id, art_title, art_thumbnail 
        FROM `article`
        WHERE art_author = %s
            AND art_status = 'on'
            AND art_date <= NOW()
            AND art_id != %s
        ORDER BY RAND()
        LIMIT %s;
    '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (authorid, ignore, limit,))
    articles = cur.fetchall()
    cur.close()

    return articles


def get_most_viewed(mysql, limit):

    sql = '''
        SELECT `art_id`, `art_title`, `art_thumbnail`
        FROM `article`
        WHERE art_status = 'on'
            AND art_date <= NOW()
        ORDER BY `art_view` DESC
        LIMIT %s;
    '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (limit,))
    articles = cur.fetchall()
    cur.close()

    return articles


def get_most_commented(mysql, limit, no_zero_comments=True):

    if no_zero_comments:
        having = ''
    else:
        having = 'HAVING total_comments > 0'

    sql = f'''
        SELECT a.art_id, a.art_title, a.art_thumbnail, COUNT(c.com_id) AS total_comments
        FROM  article a
        JOIN comment c ON a.art_id = c.com_article
        GROUP BY a.art_id, a.art_title, a.art_thumbnail
        {having}
        ORDER BY total_comments DESC
        LIMIT %s;
    '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (limit,))
    articles = cur.fetchall()
    cur.close()

    return articles
