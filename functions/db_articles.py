from flask_mysqldb import MySQLdb


def get_all(mysql, limit=0):  # Obtém todos os artigos na página inicial

    if limit == 0:
        subsql = ''
    else:
        subsql = f'LIMIT {limit}'

    sql = f'''
        -- Seleciona os campos abaixo
        SELECT art_id, art_title, art_resume, art_thumbnail
        -- desta tabela
        FROM article
        -- art_status é 'on'
        WHERE art_status = 'on'
            -- E art_date é menor ou igual à data atual
            -- Não obtém artigos com data futura (agendados)
            AND art_date <= NOW()
        -- Ordena pela data mais recente
        ORDER BY art_date DESC
        {subsql}
    '''
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql)
    articles = cur.fetchall()
    cur.close()

    return articles


def get_one(mysql, artid):  # Obtém um artigo pelo id

    sql = '''
        SELECT 
            -- Campos do artigo
            art_id, art_date, art_title, art_content,
            -- Campos do autor
            sta_id, sta_name, sta_image, sta_description, sta_type,
            -- Campos especiais
            -- Obtém a data em PT-BR pelo pseudo-campo `art_datebr`
            DATE_FORMAT(art_date, '%%d/%%m/%%Y às %%H:%%i') AS art_datebr,            
            -- Calcula a idade para `sta_age` considerando ano, mês e dia de nascimento
            TIMESTAMPDIFF(YEAR, sta_birth, CURDATE()) - (DATE_FORMAT(CURDATE(), '%%m%%d') < DATE_FORMAT(sta_birth, '%%m%%d')) AS sta_age
        FROM article
        INNER JOIN staff ON art_author = sta_id
        WHERE art_id = %s
            AND art_status = 'on'
            AND art_date <= NOW();
    '''
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql, (artid,))
    article = cur.fetchone()
    cur.close()

    return article


def update_views(mysql, artid):  # Atualiza as visualizações do artigo

    sql = 'UPDATE article SET art_view = art_view + 1 WHERE art_id = %s'
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql, (artid,))
    mysql.connection.commit()
    cur.close()

    return True


def get_author(mysql, staid, artid, limit):  # Obtém artigos do autor

    sql = '''
        -- Obtém (id, title, thumbnail)
        SELECT art_id, art_title, art_thumbnail
        -- da table `article`
        FROM article
        -- Do author com o id `art_author`
        WHERE art_author = %s
        -- Cujo status é 'on'
            AND art_status = 'on'
            -- Cuja data de publicação está no passado
            AND art_date <= NOW()
            -- Não obtém o artigo atual
            AND art_id != %s
        -- Em ordem aleatória
        ORDER BY RAND()
        -- Até 4 artigos
        LIMIT %s;
    '''
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql, (staid, artid, limit, ))
    articles = cur.fetchall()
    cur.close()

    return articles


def articles_search(mysql, query, limit=0):

    if limit == 0:
        subsql = ''
    else:
        subsql = f'LIMIT {limit}'

    sql = f'''
        SELECT art_id, art_title, art_resume, art_thumbnail
        FROM article
        WHERE (
                art_title LIKE %s
                OR art_resume LIKE %s
                OR art_content  LIKE %s
            )
            AND art_status = 'on'
            AND art_date <= NOW()
        ORDER BY art_date DESC
        {subsql}
    '''
    like_term = f'%{query}%'
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql, (like_term, like_term, like_term, ))
    articles = cur.fetchall()
    cur.close()

    return articles


def most_commented(mysql, limit=4):
    sql = '''
        -- Seleciona os campos e a contagem de comentários
        SELECT 
            a.art_id, 
            a.art_title,
            a.art_thumbnail, 
            COUNT(c.com_id) AS comment_count
        FROM 
            article a
        -- Faz um LEFT JOIN com a tabela comment, contando apenas os comentários cujo com_status é 'on'
        LEFT JOIN 
            comment c ON a.art_id = c.com_article AND c.com_status = 'on'
        -- Filtra os artigos para incluir apenas aqueles cujo art_status é 'on' e art_date é menor ou igual a NOW()
        WHERE 
            a.art_status = 'on' 
            AND a.art_date <= NOW()
        -- Agrupa os resultados por art_id, art_title
        GROUP BY 
            a.art_id, a.art_title
        -- Filtra os grupos para incluir apenas aqueles com contagem de comentários maior que zero
        HAVING 
            comment_count > 0
        -- Ordena os resultados pela contagem de comentários em ordem decrescente
        ORDER BY 
            comment_count DESC
        -- Limita os resultados a # registros
        LIMIT %s;
    '''
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql, (limit,))
    articles = cur.fetchall()
    cur.close()

    return articles


def most_viewed(mysql, limit=4):
    sql = '''
        SELECT art_id, art_title, art_thumbnail
        FROM article
        WHERE art_status = 'on'
            AND art_date <= NOW()
        ORDER BY art_view DESC, art_date DESC
        LIMIT %s
    '''
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql, (limit,))
    articles = cur.fetchall()
    cur.close()

    return articles


def get_random(mysql, limit=4):  # Obtém artigos aleatórios

    sql = '''
        SELECT art_id, art_title, art_thumbnail
        FROM article
        WHERE art_status = 'on'
            AND art_date <= NOW()
        ORDER BY RAND()
        LIMIT %s
    '''
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql, (limit,))
    articles = cur.fetchall()
    cur.close()

    return articles
