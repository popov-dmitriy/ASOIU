def make_query(con, query):
    link = con.cursor()
    link.execute(query)
    con.commit()
    return link.fetchall()
