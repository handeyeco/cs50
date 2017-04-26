query = []

    if l.city:
        query.append("place_name=:place_name")
    if l.state:
        query.append("admin_name1=:admin_name1")
    if l.zipcode:
        query.append("postal_code=:postal_code")

    if len(query) < 1:
        result = []
    else:
        result = db.execute("SELECT * FROM places WHERE " + " AND ".join(query), place_name=l.city, admin_name1=l.state, postal_code=l.zipcode)
