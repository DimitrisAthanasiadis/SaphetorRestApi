import gzip
import pandas as pd
import io
from flask import make_response
import json
from dicttoxml import dicttoxml


class VcfTool:
    """
    a class that mimcks the database operations.
    i tried ti implement methods that look like
    a select, insert, update, delete methods so that
    they could be used by the API
    """

    def __init__(self, **kwargs) -> None:
        self.vcf_path = kwargs.get("vcf_path")

    def get_dataframe(self, **kwargs) -> pd.DataFrame:
        """
        it opens the vcf file path given and returns
        the file as a dataframe

        Returns:
            pd.DataFrame: the vcf file as a dataframe
        """

        with gzip.open(self.vcf_path, 'rt') as f:
            lines = [l for l in f if not l.startswith('##')]
        return pd.read_csv(
            io.StringIO(''.join(lines)),
            # dtype={'#CHROM': str, 'POS': int, 'ID': str, 'REF': str, 'ALT': str,
            #     'QUAL': str, 'FILTER': str, 'INFO': str},
            sep='\t'
        ).rename(columns={'#CHROM': 'CHROM'})

    def get_dataframe_row(self, **kwargs) -> dict:
        """
        method that returns a single record from the
        given dataset. it either accepts a dataframe
        or it opens the specified vcf file as the dataframe

        Returns:
            dict: vcf file row with the given row_id
        """

        if kwargs.get("df"):
            df = kwargs.get("df")
        else:
            df = self.get_dataframe()

        row = df[df["ID"] == kwargs.get("row_id")]
        final_dict = row.to_dict("records")[0] # gets the row as a pure dict without index (records orientation)

        if not final_dict.get("ID"):
            return {"result": "No record found", "status": 404}

        return {"result": final_dict, "status": 200}

    def get_results(self, **kwargs) -> dict:
        """
        a method that returns the desired results paginated,
        either by the default or the desired pagination.

        Returns:
            dict: dict that contains the results. the keyword 'result'
                contains a list of dicts with the results fetched from
                the dataset
        """

        if kwargs.get("df"):
            df = kwargs.get("df")
        else:
            df = self.get_dataframe()

        page = kwargs.get("page") or 1
        per_page = kwargs.get("per_page") or 10
        start_index = (page * per_page) - per_page
        end_index = (start_index + per_page) - 1
        df_res = df[start_index:end_index+1]

        final_res = []
        for index, row in df_res.iterrows():
            final_res.append(row.to_dict())

        return {"result": final_res, "status": 200}

    def add_row(self, **kwargs) -> dict:
        """
        accepts the dataframe or opens it from
        the default specified file path. it appends
        the given dict to the vcf file and returns
        the data that user provided as well as the
        status code.

        Returns:
            dict: it contains the user provided data
                and the status code
        """

        if kwargs.get("df"):
            df = kwargs.get("df")
        else:
            df = self.get_dataframe()

        try:
            df = df.append(kwargs.get("data"), ignore_index=True)
            df.to_csv(self.vcf_path, sep='\t', index=False, compression='gzip')
        except Exception as e:
            return {
                "result": {
                    "error": "Something went wrong adding the row into the file",
                    "exception": str(e)
                },
                "status": 500
            }

        return {
            "result": kwargs.get("data"),
            "status": 201
        }

    def update_row(self, **kwargs) -> dict:
        """
        accepts the dataframe or opens it from
        the default specified file path.
        it updates the given row_id with the
        provided dict data.

        Returns:
            dict: it contains the notification
                about the update and the status code
        """

        if kwargs.get("df"):
            df = kwargs.get("df")
        else:
            df = self.get_dataframe()

        row = df[df["ID"] == kwargs.get("row_id")]

        if row.empty:
            return {"result": "No record found", "status": 404}

        try:
            index = df.index[df['ID'] == kwargs.get("row_id")].tolist()[0]
            for key, value in kwargs.get("data").items():
                df.at[index, key] = value

            df.to_csv(self.vcf_path, sep='\t', index=False, compression='gzip')
        except Exception as e:
            return {
                "result": {
                    "error": "Something went wrong updating the row into the file",
                    "exception": str(e)
                },
                "status": 500
            }

        return {
            "result": f"Row with id {kwargs.get('row_id')} updated",
            "status": 200
        }

    def delete_row(self, **kwargs) -> dict:
        """
        accepts the dataframe or opens it from
        specified file path. it deletes the given
        row_id from the vcf file.

        Returns:
            dict: it contains the notification
                about the deletion and the status code
        """

        if kwargs.get("df"):
            df = kwargs.get("df")
        else:
            df = self.get_dataframe()

        row = df[df["ID"] == kwargs.get("row_id")]

        if row.empty:
            return {"result": "No record found", "status": 404}

        try:
            index_to_delete = df.index[df['ID'] == kwargs.get("row_id")].tolist()[0]
            df = df.drop(index_to_delete)
            df.to_csv(self.vcf_path, sep='\t', index=False, compression='gzip')
        except Exception as e:
            return {
                "result": {
                    "error": "Something went wrong deleting the row into the file",
                    "exception": str(e)
                },
                "status": 500
            }

        return {
            "result": f"Row with id {kwargs.get('row_id')} deleted",
            "status": 204
        }


class ResponseTool:
    """
    a class that has the purpose of returning the response
    according to the desired response type.

    i wanted a kind of abstract way of getting the response
    by providing the data and the response type only.
    """

    def __init__(self, **kwargs) -> None:
        self.representations = {
            'application/xml': self.output_xml,
            'application/json': self.output_json,
            "*/*": self.output_json
        }

    def output_json(self, data, code, headers=None) -> make_response:
        """Makes a Flask response with a JSON encoded body"""
        resp = make_response(json.dumps(data), code)
        resp.headers.extend(headers or {})

        return resp

    def output_xml(self, data, code, headers=None) -> make_response:
        """Makes a Flask response with an XML body"""
        from xml.dom.minidom import parseString

        resp = make_response(parseString(dicttoxml(data, attr_type=False)).toprettyxml(), code)
        resp.headers.extend(headers or {})

        return resp

    def get_response(self, **kwargs) -> make_response:
        """
        receives the response type and the data and
        returns the corresponding response according to
        the representation type

        Returns:
            make_response: response object
        """

        if kwargs.get("resp_type"):
            if kwargs.get("resp_type") not in self.representations:
                return {"error": "Response-Type not acceptable"}, 406

        if not kwargs.get("data"):
                return {"error": "No record found"}, 404

        resp = make_response(self.representations[kwargs.get("resp_type") or "application/json"](data=kwargs.get("data"), code=kwargs.get("data").get("status")))
        return resp
