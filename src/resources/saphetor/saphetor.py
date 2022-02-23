from flask_restful import Resource, reqparse
from flask import jsonify, Response
from utils.utils import VcfTool, ResponseTool
from flask import request
from utils.decorators import token_required
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
saphetor_data = reqparse.RequestParser()
saphetor_data.add_argument("page", type=int, required=False, default=1, help="Page number")
saphetor_data.add_argument("per_page", type=int, required=False, default=10, help="Number of items per page")


class Saphetor(Resource):
    """
    the actual REST API implementation
    """

    def __init__(self) -> None:
        self.response_tool = ResponseTool()
        self.vcf_tool = VcfTool(vcf_path=os.path.join(BASE_DIR, "static", "NA12877_API_10.vcf.gz"))

    def get(self, row_id=None) -> Response:
        data = saphetor_data.parse_args()

        if row_id:
            if row_id[:2] != "rs":
                return jsonify({"error": "Wrong ID pattern. Must start with rs[INTEGER]"}), 404

            response = self.response_tool.get_response(data=self.vcf_tool.get_dataframe_row(row_id=row_id), resp_type=request.headers.get("Response-Type"))

            return response

        response = self.response_tool.get_response(data=self.vcf_tool.get_results(**data), resp_type=request.headers.get("Response-Type"))

        return response

    @token_required
    def post(self, **kwargs) -> Response:
        response = self.response_tool.get_response(data=self.vcf_tool.add_row(data=request.get_json()), resp_type=request.headers.get("Response-Type"))

        return response

    @token_required
    def put(self, row_id=None) -> Response:
        if not row_id:
            return jsonify({"error": "No row id provided"}), 400

        response = self.response_tool.get_response(data=self.vcf_tool.update_row(row_id=row_id, data=request.get_json()))

        return response
