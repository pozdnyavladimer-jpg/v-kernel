def process(data):
    if not data:
        return None

    result = []
    for item in data:
        result.append(item * 2)

    return result
