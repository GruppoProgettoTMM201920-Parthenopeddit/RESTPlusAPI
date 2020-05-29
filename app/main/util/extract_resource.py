def extract_resource(request, name):
    try:
        value = request.json[name]
    except:
        try:
            value = request.values[name]
        except:
            raise Exception
    return value
