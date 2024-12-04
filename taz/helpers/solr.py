def convert_id_to_solr_format(_id):
    return _id[:7] if _id.isdigit() else _id
