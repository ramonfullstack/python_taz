import datetime
import hashlib


def generate_task_id_with_seller_id_and_scope(seller_id, scope):
    return hashlib.md5(
        '{seller_id}{scope}'.format(seller_id=seller_id, scope=scope).encode(
            'utf-8'
        )
    ).hexdigest()


def create_message(scope, data, task_id):
    return {
        'scope': scope,
        'action': 'update',
        'data': data,
        'task_id': task_id
    }


def parse_seller(seller):
    return {
        'id': seller['id'],
        'legal_name': seller['legal_name'],
        'trading_name': seller.get('trading_name'),
        'name': seller['name'],
        'document_number': seller['document_number'],
        'address': seller['address'],
        'updated_at': datetime.datetime.now().isoformat()
    }
