
def generate_medias(variation):
    return [
        {
            'seller_id': variation['seller_id'],
            'sku': variation['sku'],
            'videos': ['{}'.format(variation['sku'])]
        },
        {
            'seller_id': variation['seller_id'],
            'sku': variation['sku'],
            'audios': ['{}.mp3'.format(variation['sku'])]
        },
        {
            'seller_id': variation['seller_id'],
            'sku': variation['sku'],
            'podcasts': ['{}.mp3'.format(variation['sku'])],
        },
        {
            'seller_id': variation['seller_id'],
            'sku': variation['sku'],
            'images': [
                '{}.jpg'.format(variation['sku']),
                '{}-A.jpg'.format(variation['sku'])
            ]
        }
    ]


def store_media(mongo_database, variation):
    mongo_database.medias.insert_many(generate_medias(variation))
