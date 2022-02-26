# this is the test file for the api

import unittest
from app import app
import json


class TestSaphetorApiResponse(unittest.TestCase):
    def test_get_row(self) -> None:
        print("RUNNING TESTS FOR FETCHING A SPECIFIC ROW ID")
        client = app.test_client(self)
        required_keys = [
            "CHROM",
            "POS",
            "ID",
            "REF",
            "ALT",
            "QUAL",
            "FILTER",
            "INFO",
            "FORMAT",
        ]

        # no headers provided, json format
        response = client.get("/saphetor/getRow/rs1232018312")
        response_status_code = response.status_code
        response_data = json.loads(response.data.decode())
        self.assertEqual(response_status_code, 200)
        self.assertTrue("result" in response_data)
        self.assertTrue(
            all(elem in list(response_data.get("result")) for elem in required_keys)
        )

        # Response-Type = application/json header provided, json format
        response = client.get(
            "/saphetor/getRow/rs1232018312",
            headers={"Response-Type": "application/json"},
        )
        response_status_code = response.status_code
        response_data = json.loads(response.data.decode())
        self.assertEqual(response_status_code, 200)
        self.assertTrue("result" in response_data)
        self.assertTrue(
            all(elem in list(response_data.get("result")) for elem in required_keys)
        )

        # Response-Type = */* header provided, json format
        response = client.get(
            "/saphetor/getRow/rs1232018312", headers={"Response-Type": "*/*"}
        )
        response_status_code = response.status_code
        response_data = json.loads(response.data.decode())
        self.assertEqual(response_status_code, 200)
        self.assertTrue("result" in response_data)
        self.assertTrue(
            all(elem in list(response_data.get("result")) for elem in required_keys)
        )

        # Response-Type = application/xml header provided, xml format
        import xml.etree.ElementTree as ET

        response = client.get(
            "/saphetor/getRow/rs1232018312",
            headers={"Response-Type": "application/xml"},
        )
        response_status_code = response.status_code

        # check if all required keys are present in the xml response
        root_element = ET.fromstring(response.data.decode()).find("result")
        for required_key in required_keys:
            self.assertTrue(root_element.find(required_key) is not None)

    def test_get_paginated(self) -> None:
        print("RUNNING TESTS FOR FETCHING PAGINATED RESULTS")
        client = app.test_client(self)
        response = client.get("/saphetor/getPaginatedData?page=1&per_page=10")
        response_status_code = response.status_code
        response_data = json.loads(response.data.decode())
        required_keys = [
            "CHROM",
            "POS",
            "ID",
            "REF",
            "ALT",
            "QUAL",
            "FILTER",
            "INFO",
            "FORMAT",
        ]

        self.assertEqual(response_status_code, 200)
        self.assertTrue("result" in response_data)
        self.assertEqual(
            len(response_data.get("result")), 9
        )  # TODO to be fixed. wrong length of results
        self.assertTrue(
            all(elem in list(response_data.get("result"))[0] for elem in required_keys)
        )

    def test_add_row(self) -> None:
        print("RUNNING TESTS FOR ADDING A ROW")
        client = app.test_client(self)
        response = client.post(
            "/saphetor/addRow",
            data=json.dumps(
                {
                    "CHROM": "chr2",
                    "POS": 1003,
                    "ALT": "A",
                    "REF": "C",
                    "ID": "rsMitsoRe",
                }
            ),
            headers={
                "Content-Type": "application/json",
                "X-Access-Token": "my-secret-key",
            },
        )
        response_status_code = response.status_code
        response_data = json.loads(response.data.decode())

        self.assertEqual(response_status_code, 201)
        self.assertTrue("result" in response_data)
        self.assertEqual(response_data.get("status"), 201)

    def test_update_row(self) -> None:
        print("RUNNING TESTS FOR UPDATING A ROW")
        client = app.test_client(self)
        response = client.put(
            "/saphetor/updateRow/rs78249347",
            data=json.dumps(
                {"CHROM": "chrXY", "POS": 11, "ALT": "ABC", "REF": "CDEffff"},
            ),
            headers={
                "Content-Type": "application/json",
                "X-Access-Token": "my-secret-key",
            }
        )
        response_status_code = response.status_code
        response_status_data = json.loads(response.data.decode())

        self.assertEqual(response_status_code, 200)
        self.assertEqual(response_status_data.get("status"), 200)
        self.assertTrue("result" in response_status_data)
        self.assertTrue("rs78249347" in response_status_data.get("result"))

    def test_delete_row(self) -> None:
        print("RUNNING TESTS FOR DELETING A ROW")
        client = app.test_client(self)
        response = client.delete(
            "/saphetor/deleteRow/rsMitsoRe",
            headers={
                "X-Access-Token": "my-secret-key",
            }
        )
        response_status_code = response.status_code

        self.assertEqual(response_status_code, 204)


if __name__ == "__main__":
    unittest.main()
