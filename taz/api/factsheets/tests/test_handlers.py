class TestFactsheetHandler:

    def test_should_get_factsheet(
        self,
        client,
        mock_factsheet_sku,
        mock_factsheet_seller_id,
        mock_factsheet_payload,
        patch_storage_manager_get_json
    ):
        with patch_storage_manager_get_json as mock_get_json:
            mock_get_json.return_value = mock_factsheet_payload
            response = client.get(
                '/factsheet/seller/{seller_id}/sku/{sku}'.format(
                    seller_id=mock_factsheet_seller_id,
                    sku=mock_factsheet_sku
                )
            )

        assert response.json == mock_factsheet_payload

    def test_should_get_factsheet_returns_not_found(
        self,
        client
    ):
        response = client.get(
            '/factsheet/seller/{seller_id}/sku/{sku}'.format(
                seller_id='murcho',
                sku='000000000'
            )
        )

        assert response.status_code == 404
