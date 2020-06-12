def get_paginated_result(query, page, per_page, field, timestamp):
    new_query = query
    if page != 1 and timestamp != None:
        new_query = query.filter(
            field < timestamp
        )

    try:
        return new_query.paginate(
            per_page=per_page,
            page=page
        ).items, 200
    except:
        response_object = {
            'status': 'error',
            'message': 'end of content',
        }
        return response_object, 470
