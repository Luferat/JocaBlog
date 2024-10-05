import re


def search_articles(mysql, query):

    sql = '''
        SELECT art_id, art_title, art_resume, art_thumbnail
        FROM article
        WHERE (art_title LIKE %s
            OR art_resume LIKE %s
            OR art_content LIKE %s)
            AND art_status = 'on'
            AND art_date <= NOW()
        ORDER BY art_date DESC;
    '''
    params = (f'%{query}%', f'%{query}%', f'%{query}%')
    cur = mysql.connection.cursor()
    cur.execute(sql, params)
    articles = cur.fetchall()
    cur.close()

    return articles


def search_comments(mysql, query, length=40):
    sql = '''
        SELECT com_article, com_author_name, com_comment, art_title, art_thumbnail
        FROM comment
        INNER JOIN article ON com_article = art_id
        WHERE (com_comment LIKE %s)
            AND art_status = 'on'
            AND art_date <= NOW();
    '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (f'%{query}%',))
    comments = cur.fetchall()
    cur.close()

    # Adicionar o campo com_partial para cada comentário
    for comment in comments:
        comment['com_partial'] = comment['com_comment'][:length] + '...'

    return comments
