def save_contact(mysql, form):

    sql = '''
        INSERT INTO contact (
            name, email, subject, message
        ) VALUES (
            %s, %s, %s, %s
        )
    '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (form['name'], form['email'],
                form['subject'], form['message'], ))
    mysql.connection.commit()
    cur.close()

    return True
