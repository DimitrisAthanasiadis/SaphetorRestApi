import os

from flask import Response, jsonify, request
from flask_restful import Resource, reqparse

from resources.saphetor_schema import SaphetorPostSchema
from utils.decorators import token_required
from utils.utils import ResponseTool, VcfTool

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Saphetor(Resource):
    """
    the actual REST API implementation
    """

    def __init__(self) -> None:
        self.response_tool = ResponseTool()
        self.vcf_tool = VcfTool(
            vcf_path=os.path.join(BASE_DIR, "static", "NA12877_API_10.vcf.gz")
        )

        self.reqparse_get_args = reqparse.RequestParser()
        self.reqparse_get_args.add_argument(
            "page", type=int, required=False, default=1, help="Page number"
        )
        self.reqparse_get_args.add_argument(
            "per_page",
            type=int,
            required=False,
            default=10,
            help="Number of items per page",
        )
        self.reqparse_get_args.add_argument(
            "Response-Type",
            type=str,
            required=False,
            default="application/json",
            location="headers",
            help="Response type. Anything between [application/json, application/xml, */*] or nothing.",
        )

        self.reqparse_post_args = reqparse.RequestParser()
        self.reqparse_post_args.add_argument(
            "Content-Type",
            type=str,
            required=True,
            default="application/json",
            location="headers",
            help="Content type. Must be application/json.",
        )
        self.reqparse_post_args.add_argument(
            "X-Access-Token",
            type=str,
            required=True,
            location="headers",
            help="The predefined secret key",
        )

    def get(self, row_id=None) -> Response:
        request_args = self.reqparse_get_args.parse_args()

        if row_id:
            if row_id[:2] != "rs":
                return (
                    jsonify({"error": "Wrong ID pattern. Must start with rs[INTEGER]"}),
                    404,
                )

            response = self.response_tool.get_response(
                data=self.vcf_tool.get_dataframe_row(row_id=row_id),
                resp_type=request_args.get("Response-Type"),
            )

            return response

        response = self.response_tool.get_response(
            data=self.vcf_tool.get_results(**request_args),
            resp_type=request_args.get("Response-Type"),
        )

        return response

    @token_required
    def post(self) -> Response:
        schema = SaphetorPostSchema().load(request.get_json())
        request_args = self.reqparse_post_args.parse_args()

        response = self.response_tool.get_response(
            data=self.vcf_tool.add_row(data=schema),
            resp_type=request_args.get("Response-Type"),
        )

        return response

    @token_required
    def put(self, row_id=None) -> Response:
        if not row_id:
            return jsonify({"error": "No row id provided"}), 400

        response = self.response_tool.get_response(
            data=self.vcf_tool.update_row(row_id=row_id, data=request.get_json())
        )

        return response

    @token_required
    def delete(self, row_id=None) -> Response:
        if not row_id:
            return jsonify({"error": "No row id provided"}), 400

        response = self.response_tool.get_response(
            data=self.vcf_tool.delete_row(row_id=row_id)
        )

        return response
