from flask_mysqldb import MySQLdb


def save_comment(mysql, form):  # Salva comentário

    sql = '''
        INSERT INTO comment (com_article, com_author_name, com_author_email, com_comment)
        VALUE (%s, %s, %s, %s)
    '''
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql, (form['artid'], form['name'],
                form['email'], form['comment'], ))
    mysql.connection.commit()
    cur.close()

    return 'Enviado'


def get_comments(mysql, artid):  # Obtém todos os comentarios do artigo

    sql = '''
        SELECT
            com_id, com_author_name, com_comment,
            DATE_FORMAT(com_date, '%%d/%%m/%%Y às %%H:%%i') AS com_datebr
        FROM comment 
        WHERE com_article = %s
            AND com_status = 'on'
        ORDER BY com_date DESC;
    '''
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql, (artid, ))
    comments = cur.fetchall()
    cur.close()

    return comments


def user_coments(mysql, useremail, limit=4):
    sql = '''
        SELECT com_article, com_comment, art_title
        FROM comment
        INNER JOIN article ON art_id = com_article
        WHERE com_author_email = %s 
            AND com_status = 'on'
        ORDER BY com_date DESC
        LIMIT %s
    '''
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql, (useremail, limit, ))
    comments = cur.fetchall()
    cur.close()

    return comments
