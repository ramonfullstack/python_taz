import pytest

from taz.api.common.utils import parse_base64_to_dict


class TestUtils:

    @pytest.fixture
    def base64_content(self):
        return (
            'eyJpZCI6ICJtbGVudHJlZ2FzIiwgImFjY291bnRfbmFtZSI6ICJyZV9jazEyaWI'
            '3NXQwMWRpc2Q2ZWpvMXdpZ2x0IiwgImNvbnRhY3RzIjogW10sICJhZGRyZXNzI'
            'jogeyJhZGRyZXNzIjogIlJ1YSBWb2x1bnRcdTAwZTFyaW9zIGRhIEZyYW5jYSI'
            'sICJudW1iZXIiOiAiMTQ2NSIsICJjb21wbGVtZW50IjogIiIsICJkaXN0cmljd'
            'CI6ICJDZW50cm8iLCAiY2l0eSI6ICJGcmFuY2EiLCAic3RhdGUiOiAiU1AiLCAi'
            'Y291bnRyeSI6ICJCcmFzaWwiLCAiemlwY29kZSI6ICIxNDQwMDQ5MCJ9LCAibGV'
            'nYWxfbmFtZSI6ICJNYWdhemluZSBMdWl6YSIsICJ0cmFkaW5nX25hbWUiOiAibW'
            'dsdTMiLCAiZG9jdW1lbnRfbnVtYmVyIjogIjQ3OTYwOTUwMDAwMTIxIiwgInRyY'
            'W5zZmVyX2RheSI6IDEsICJiYW5rX2NvZGUiOiAiMjM3IiwgImJhbmtfY29kZV9k'
            'aWdpdCI6ICIiLCAiYmFua19hZ2VuY3kiOiAiMjA0MiIsICJiYW5rX2FnZW5jeV9'
            'kaWdpdCI6ICI3IiwgImJhbmtfYWNjb3VudCI6ICI5MzAwMSIsICJiYW5rX2FjY2'
            '91bnRfZGlnaXQiOiAiNiIsICJmaW5hbmNpYWxfZW1haWwiOiAic2FjQG1hZ2F6aW'
            '5lbHVpemEuY29tLmJyIiwgImNhbl9hbnRpY2lwYXRlIjogdHJ1ZSwgImRpc3RyaW'
            'J1dGlvbl9jZW50ZXJfemlwY29kZSI6IG51bGwsICJpbnRlZ3JhdGlvbl9pbmZvIj'
            'ogbnVsbCwgInNlcnZpY2VzIjogW3sic2VydmljZSI6ICJtYWdhbHUtcGFnYW1lbn'
            'RvcyIsICJpc19hY3RpdmUiOiB0cnVlfV0sICJpc19hY3RpdmUiOiB0cnVlLCAibmF'
            'tZSI6ICJNYWdhbHUgRW50cmVnYXMiLCAiZGVmYXVsdF9mZWVfcGVyY2VudGFnZSI6'
            'ICIxMC4wMCIsICJhY2NvdW50X2dyb3VwIjogIm1sZW50cmVnYXMiLCAicGxhdGZvc'
            'm0iOiAib3BlbmFwaSIsICJ0cmFuc2Zlcl9pbnRlcnZhbCI6ICJ3ZWVrbHkiLCAibG'
            'VhZF9jcmVhdGVkX2F0IjogbnVsbCwgImFwaV9zaWduYXR1cmVfc2VjcmV0IjogIi'
            'IsICJzaGlwcGluZ19mYWxsYmFja191cmwiOiAiIiwgInNoaXBwaW5nX2NhbGxiYW'
            'NrX3VybCI6ICIiLCAicmVzZXJ2YXRpb25fY2FsbGJhY2tfdXJsIjogIiIsICJmdW'
            'xmaWxsbWVudF9jYWxsYmFja191cmwiOiAiIiwgIm9yZGVyX3N0YXR1c19jYWxsYm'
            'Fja191cmwiOiAiIiwgIm9yZGVyX2l0ZW1fY2FuY2VsX2NhbGxiYWNrX3VybCI6IC'
            'IiLCAic2VsbHNfdG9fY29tcGFueSI6IHRydWUsICJwaG9uZSI6IG51bGwsICJzdG'
            'F0ZV9pbnNjcmlwdGlvbiI6IG51bGwsICJpdF9lbWFpbCI6IG51bGwsICJidXNpbm'
            'Vzc19jb25kaXRpb24iOiAiIiwgInNpdGVfdXJsIjogbnVsbCwgIm1lcmNoYW50X2'
            'NvZGUiOiAiODYwNiIsICJibG9ja19yZWNlaXZhYmxlcyI6IHRydWUsICJhbnRpY2'
            'lwYXRpb25fZmVlIjogIjEuNDkiLCAibWF4X2FudGljaXBhdGlvbl9wZXJjZW50YW'
            'dlIjogIjEwMC4wMCIsICJzZWxsZXJfZXh0ZXJuYWxfaWQiOiAiIiwgIm1kciI6IC'
            'IwLjAwIn0='
        )

    def test_should_parse_base64_to_dict(self, base64_content):
        data = parse_base64_to_dict(base64_content)
        assert data == {
            'id': 'mlentregas',
            'account_name': 're_ck12ib75t01disd6ejo1wiglt',
            'contacts': [],
            'address': {
                'address': 'Rua Voluntários da Franca',
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
            'distribution_center_zipcode': None,
            'integration_info': None,
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
            'lead_created_at': None,
            'api_signature_secret': '',
            'shipping_fallback_url': '',
            'shipping_callback_url': '',
            'reservation_callback_url': '',
            'fulfillment_callback_url': '',
            'order_status_callback_url': '',
            'order_item_cancel_callback_url': '',
            'sells_to_company': True,
            'phone': None,
            'state_inscription': None,
            'it_email': None,
            'business_condition': '',
            'site_url': None,
            'merchant_code': '8606',
            'block_receivables': True,
            'anticipation_fee': '1.49',
            'max_anticipation_percentage': '100.00',
            'seller_external_id': '',
            'mdr': '0.00'
        }
