import base64
import json

import pytest

from taz.api.common.utils import parse_base64_to_dict


@pytest.fixture
def seller_payload():
    return {
        'message': {
            'data': 'eyJpZCI6ICJtbGVudHJlZ2FzIiwgImFjY291bnRfbmFtZSI6ICJyZV9jazEyaWI3NXQwMWRpc2Q2ZWpvMXdpZ2x0IiwgImNvbnRhY3RzIjogW10sICJhZGRyZXNzIjogeyJhZGRyZXNzIjogIlJ1YSBWb2x1bnRcdTAwZTFyaW9zIGRhIEZyYW5jYSIsICJudW1iZXIiOiAiMTQ2NSIsICJjb21wbGVtZW50IjogIiIsICJkaXN0cmljdCI6ICJDZW50cm8iLCAiY2l0eSI6ICJGcmFuY2EiLCAic3RhdGUiOiAiU1AiLCAiY291bnRyeSI6ICJCcmFzaWwiLCAiemlwY29kZSI6ICIxNDQwMDQ5MCJ9LCAibGVnYWxfbmFtZSI6ICJNYWdhemluZSBMdWl6YSIsICJ0cmFkaW5nX25hbWUiOiAibWdsdTMiLCAiZG9jdW1lbnRfbnVtYmVyIjogIjQ3OTYwOTUwMDAwMTIxIiwgInRyYW5zZmVyX2RheSI6IDEsICJiYW5rX2NvZGUiOiAiMjM3IiwgImJhbmtfY29kZV9kaWdpdCI6ICIiLCAiYmFua19hZ2VuY3kiOiAiMjA0MiIsICJiYW5rX2FnZW5jeV9kaWdpdCI6ICI3IiwgImJhbmtfYWNjb3VudCI6ICI5MzAwMSIsICJiYW5rX2FjY291bnRfZGlnaXQiOiAiNiIsICJmaW5hbmNpYWxfZW1haWwiOiAic2FjQG1hZ2F6aW5lbHVpemEuY29tLmJyIiwgImNhbl9hbnRpY2lwYXRlIjogdHJ1ZSwgImRpc3RyaWJ1dGlvbl9jZW50ZXJfemlwY29kZSI6IG51bGwsICJpbnRlZ3JhdGlvbl9pbmZvIjogbnVsbCwgInNlcnZpY2VzIjogW3sic2VydmljZSI6ICJtYWdhbHUtcGFnYW1lbnRvcyIsICJpc19hY3RpdmUiOiB0cnVlfV0sICJpc19hY3RpdmUiOiB0cnVlLCAibmFtZSI6ICJNYWdhbHUgRW50cmVnYXMiLCAiZGVmYXVsdF9mZWVfcGVyY2VudGFnZSI6ICIxMC4wMCIsICJhY2NvdW50X2dyb3VwIjogIm1sZW50cmVnYXMiLCAicGxhdGZvcm0iOiAib3BlbmFwaSIsICJ0cmFuc2Zlcl9pbnRlcnZhbCI6ICJ3ZWVrbHkiLCAibGVhZF9jcmVhdGVkX2F0IjogbnVsbCwgImFwaV9zaWduYXR1cmVfc2VjcmV0IjogIiIsICJzaGlwcGluZ19mYWxsYmFja191cmwiOiAiIiwgInNoaXBwaW5nX2NhbGxiYWNrX3VybCI6ICIiLCAicmVzZXJ2YXRpb25fY2FsbGJhY2tfdXJsIjogIiIsICJmdWxmaWxsbWVudF9jYWxsYmFja191cmwiOiAiIiwgIm9yZGVyX3N0YXR1c19jYWxsYmFja191cmwiOiAiIiwgIm9yZGVyX2l0ZW1fY2FuY2VsX2NhbGxiYWNrX3VybCI6ICIiLCAic2VsbHNfdG9fY29tcGFueSI6IHRydWUsICJwaG9uZSI6IG51bGwsICJzdGF0ZV9pbnNjcmlwdGlvbiI6IG51bGwsICJpdF9lbWFpbCI6IG51bGwsICJidXNpbmVzc19jb25kaXRpb24iOiAiIiwgInNpdGVfdXJsIjogbnVsbCwgIm1lcmNoYW50X2NvZGUiOiAiODYwNiIsICJibG9ja19yZWNlaXZhYmxlcyI6IHRydWUsICJhbnRpY2lwYXRpb25fZmVlIjogIjEuNDkiLCAibWF4X2FudGljaXBhdGlvbl9wZXJjZW50YWdlIjogIjEwMC4wMCIsICJzZWxsZXJfZXh0ZXJuYWxfaWQiOiAiIiwgIm1kciI6ICIwLjAwIn0=',  # noqa
            'messageId': '766983098991499',
            'message_id': '766983098991499',
            'publishTime': '2019-10-02T20:45:08.802Z',
            'publish_time': '2019-10-02T20:45:08.802Z'
        },
            'subscription': 'projects/maga-homolog/subscriptions/acme-helena-sellers'  # noqa
    }


@pytest.fixture
def inactive_seller_payload():
    payload = {
        'message': {
            'data': 'eyJpZCI6ICJtbGVudHJlZ2FzIiwgImFjY291bnRfbmFtZSI6ICJyZV9jazEyaWI3NXQwMWRpc2Q2ZWpvMXdpZ2x0IiwgImNvbnRhY3RzIjogW10sICJhZGRyZXNzIjogeyJhZGRyZXNzIjogIlJ1YSBWb2x1bnRcdTAwZTFyaW9zIGRhIEZyYW5jYSIsICJudW1iZXIiOiAiMTQ2NSIsICJjb21wbGVtZW50IjogIiIsICJkaXN0cmljdCI6ICJDZW50cm8iLCAiY2l0eSI6ICJGcmFuY2EiLCAic3RhdGUiOiAiU1AiLCAiY291bnRyeSI6ICJCcmFzaWwiLCAiemlwY29kZSI6ICIxNDQwMDQ5MCJ9LCAibGVnYWxfbmFtZSI6ICJNYWdhemluZSBMdWl6YSIsICJ0cmFkaW5nX25hbWUiOiAibWdsdTMiLCAiZG9jdW1lbnRfbnVtYmVyIjogIjQ3OTYwOTUwMDAwMTIxIiwgInRyYW5zZmVyX2RheSI6IDEsICJiYW5rX2NvZGUiOiAiMjM3IiwgImJhbmtfY29kZV9kaWdpdCI6ICIiLCAiYmFua19hZ2VuY3kiOiAiMjA0MiIsICJiYW5rX2FnZW5jeV9kaWdpdCI6ICI3IiwgImJhbmtfYWNjb3VudCI6ICI5MzAwMSIsICJiYW5rX2FjY291bnRfZGlnaXQiOiAiNiIsICJmaW5hbmNpYWxfZW1haWwiOiAic2FjQG1hZ2F6aW5lbHVpemEuY29tLmJyIiwgImNhbl9hbnRpY2lwYXRlIjogdHJ1ZSwgImRpc3RyaWJ1dGlvbl9jZW50ZXJfemlwY29kZSI6IG51bGwsICJpbnRlZ3JhdGlvbl9pbmZvIjogbnVsbCwgInNlcnZpY2VzIjogW3sic2VydmljZSI6ICJtYWdhbHUtcGFnYW1lbnRvcyIsICJpc19hY3RpdmUiOiB0cnVlfV0sICJpc19hY3RpdmUiOiB0cnVlLCAibmFtZSI6ICJNYWdhbHUgRW50cmVnYXMiLCAiZGVmYXVsdF9mZWVfcGVyY2VudGFnZSI6ICIxMC4wMCIsICJhY2NvdW50X2dyb3VwIjogIm1sZW50cmVnYXMiLCAicGxhdGZvcm0iOiAib3BlbmFwaSIsICJ0cmFuc2Zlcl9pbnRlcnZhbCI6ICJ3ZWVrbHkiLCAibGVhZF9jcmVhdGVkX2F0IjogbnVsbCwgImFwaV9zaWduYXR1cmVfc2VjcmV0IjogIiIsICJzaGlwcGluZ19mYWxsYmFja191cmwiOiAiIiwgInNoaXBwaW5nX2NhbGxiYWNrX3VybCI6ICIiLCAicmVzZXJ2YXRpb25fY2FsbGJhY2tfdXJsIjogIiIsICJmdWxmaWxsbWVudF9jYWxsYmFja191cmwiOiAiIiwgIm9yZGVyX3N0YXR1c19jYWxsYmFja191cmwiOiAiIiwgIm9yZGVyX2l0ZW1fY2FuY2VsX2NhbGxiYWNrX3VybCI6ICIiLCAic2VsbHNfdG9fY29tcGFueSI6IHRydWUsICJwaG9uZSI6IG51bGwsICJzdGF0ZV9pbnNjcmlwdGlvbiI6IG51bGwsICJpdF9lbWFpbCI6IG51bGwsICJidXNpbmVzc19jb25kaXRpb24iOiAiIiwgInNpdGVfdXJsIjogbnVsbCwgIm1lcmNoYW50X2NvZGUiOiAiODYwNiIsICJibG9ja19yZWNlaXZhYmxlcyI6IHRydWUsICJhbnRpY2lwYXRpb25fZmVlIjogIjEuNDkiLCAibWF4X2FudGljaXBhdGlvbl9wZXJjZW50YWdlIjogIjEwMC4wMCIsICJzZWxsZXJfZXh0ZXJuYWxfaWQiOiAiIiwgIm1kciI6ICIwLjAwIn0=',  # noqa
            'messageId': '766983098991499',
            'message_id': '766983098991499',
            'publishTime': '2019-10-02T20:45:08.802Z',
            'publish_time': '2019-10-02T20:45:08.802Z'
        },
            'subscription': 'projects/maga-homolog/subscriptions/acme-helena-sellers'  # noqa
    }

    seller = parse_base64_to_dict(payload['message']['data'])
    seller['is_active'] = False

    payload['message']['data'] = base64.b64encode(
        json.dumps(seller).encode('utf-8')
    ).decode('utf-8')

    return payload


@pytest.fixture
def seller_sells_to_company_false_payload():
    payload = {
        'message': {
            'data': 'eyJpZCI6ICJtbGVudHJlZ2FzIiwgImFjY291bnRfbmFtZSI6ICJyZV9jazEyaWI3NXQwMWRpc2Q2ZWpvMXdpZ2x0IiwgImNvbnRhY3RzIjogW10sICJhZGRyZXNzIjogeyJhZGRyZXNzIjogIlJ1YSBWb2x1bnRcdTAwZTFyaW9zIGRhIEZyYW5jYSIsICJudW1iZXIiOiAiMTQ2NSIsICJjb21wbGVtZW50IjogIiIsICJkaXN0cmljdCI6ICJDZW50cm8iLCAiY2l0eSI6ICJGcmFuY2EiLCAic3RhdGUiOiAiU1AiLCAiY291bnRyeSI6ICJCcmFzaWwiLCAiemlwY29kZSI6ICIxNDQwMDQ5MCJ9LCAibGVnYWxfbmFtZSI6ICJNYWdhemluZSBMdWl6YSIsICJ0cmFkaW5nX25hbWUiOiAibWdsdTMiLCAiZG9jdW1lbnRfbnVtYmVyIjogIjQ3OTYwOTUwMDAwMTIxIiwgInRyYW5zZmVyX2RheSI6IDEsICJiYW5rX2NvZGUiOiAiMjM3IiwgImJhbmtfY29kZV9kaWdpdCI6ICIiLCAiYmFua19hZ2VuY3kiOiAiMjA0MiIsICJiYW5rX2FnZW5jeV9kaWdpdCI6ICI3IiwgImJhbmtfYWNjb3VudCI6ICI5MzAwMSIsICJiYW5rX2FjY291bnRfZGlnaXQiOiAiNiIsICJmaW5hbmNpYWxfZW1haWwiOiAic2FjQG1hZ2F6aW5lbHVpemEuY29tLmJyIiwgImNhbl9hbnRpY2lwYXRlIjogdHJ1ZSwgImRpc3RyaWJ1dGlvbl9jZW50ZXJfemlwY29kZSI6IG51bGwsICJpbnRlZ3JhdGlvbl9pbmZvIjogbnVsbCwgInNlcnZpY2VzIjogW3sic2VydmljZSI6ICJtYWdhbHUtcGFnYW1lbnRvcyIsICJpc19hY3RpdmUiOiB0cnVlfV0sICJpc19hY3RpdmUiOiB0cnVlLCAibmFtZSI6ICJNYWdhbHUgRW50cmVnYXMiLCAiZGVmYXVsdF9mZWVfcGVyY2VudGFnZSI6ICIxMC4wMCIsICJhY2NvdW50X2dyb3VwIjogIm1sZW50cmVnYXMiLCAicGxhdGZvcm0iOiAib3BlbmFwaSIsICJ0cmFuc2Zlcl9pbnRlcnZhbCI6ICJ3ZWVrbHkiLCAibGVhZF9jcmVhdGVkX2F0IjogbnVsbCwgImFwaV9zaWduYXR1cmVfc2VjcmV0IjogIiIsICJzaGlwcGluZ19mYWxsYmFja191cmwiOiAiIiwgInNoaXBwaW5nX2NhbGxiYWNrX3VybCI6ICIiLCAicmVzZXJ2YXRpb25fY2FsbGJhY2tfdXJsIjogIiIsICJmdWxmaWxsbWVudF9jYWxsYmFja191cmwiOiAiIiwgIm9yZGVyX3N0YXR1c19jYWxsYmFja191cmwiOiAiIiwgIm9yZGVyX2l0ZW1fY2FuY2VsX2NhbGxiYWNrX3VybCI6ICIiLCAic2VsbHNfdG9fY29tcGFueSI6IHRydWUsICJwaG9uZSI6IG51bGwsICJzdGF0ZV9pbnNjcmlwdGlvbiI6IG51bGwsICJpdF9lbWFpbCI6IG51bGwsICJidXNpbmVzc19jb25kaXRpb24iOiAiIiwgInNpdGVfdXJsIjogbnVsbCwgIm1lcmNoYW50X2NvZGUiOiAiODYwNiIsICJibG9ja19yZWNlaXZhYmxlcyI6IHRydWUsICJhbnRpY2lwYXRpb25fZmVlIjogIjEuNDkiLCAibWF4X2FudGljaXBhdGlvbl9wZXJjZW50YWdlIjogIjEwMC4wMCIsICJzZWxsZXJfZXh0ZXJuYWxfaWQiOiAiIiwgIm1kciI6ICIwLjAwIn0=',  # noqa
            'messageId': '766983098991499',
            'message_id': '766983098991499',
            'publishTime': '2019-10-02T20:45:08.802Z',
            'publish_time': '2019-10-02T20:45:08.802Z'
        },
            'subscription': 'projects/maga-homolog/subscriptions/acme-helena-sellers'  # noqa
    }

    seller = parse_base64_to_dict(payload['message']['data'])
    seller['sells_to_company'] = False

    payload['message']['data'] = base64.b64encode(
        json.dumps(seller).encode('utf-8')
    ).decode('utf-8')

    return payload


@pytest.fixture
def seller():
    return {
        'id': 'mlentregas',
        'account_name': 're_ck12ib75t01disd6ejo1wiglt',
        'contacts': [],
        'address': {
            'address': 'Rua Volunt\u00e1rios da Franca',
            'number': '1465',
            'complement': '',
            'district': 'Centro',
            'city': 'Franca',
            'state': 'SP',
            'country': 'Brasil',
            'zipcode': '14400490'
        },
        'legal_name': 'Magazine Luiza',
        'trading_name': 'mglu3',
        'document_number': '47960950000121',
        'transfer_day': 1,
        'bank_code': '237',
        'bank_code_digit': '',
        'bank_agency': '2042',
        'bank_agency_digit': '7',
        'bank_account': '93001',
        'bank_account_digit': '6',
        'financial_email': 'sac@magazineluiza.com.br',
        'can_anticipate': True,
        'distribution_center_zipcode': 'null',
        'integration_info': 'null',
        'services': [
            {
                'service': 'magalu-pagamentos',
                'is_active': True
            }
        ],
        'is_active': True,
        'name': 'Magalu Entregas',
        'default_fee_percentage': '10.00',
        'account_group': 'mlentregas',
        'platform': 'openapi',
        'transfer_interval': 'weekly',
        'lead_created_at': 'null',
        'api_signature_secret': '',
        'shipping_fallback_url': '',
        'shipping_callback_url': '',
        'reservation_callback_url': '',
        'fulfillment_callback_url': '',
        'order_status_callback_url': '',
        'order_item_cancel_callback_url': '',
        'sells_to_company': True,
        'phone': 'null',
        'state_inscription': 'null',
        'it_email': 'null',
        'business_condition': '',
        'site_url': 'null',
        'merchant_code': '8606',
        'block_receivables': True,
        'anticipation_fee': '1.49',
        'max_anticipation_percentage': '100.00',
        'seller_external_id': '',
        'mdr': '0.00'
    }


@pytest.fixture
def create_seller(mongo_database, seller):
    mongo_database.sellers.save(seller)
