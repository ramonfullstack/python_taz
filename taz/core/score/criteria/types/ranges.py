
def get(element, value):
    for criteria in element['criteria']:
        count = len(value) if isinstance(value, str) else value

        if criteria.get('equals'):
            if count == criteria['equals']:
                return criteria.get('points') or 0, criteria['name']
        else:
            if not criteria.get('max'):
                if count >= criteria['min']:
                    return criteria.get('points') or 0, criteria['name']

            if not criteria.get('min'):
                if count <= criteria['max']:
                    return criteria.get('points') or 0, criteria['name']

            if (
                    criteria['min'] <= count <= criteria['max']
            ):
                return criteria.get('points') or 0, criteria['name']

    return 0, None
