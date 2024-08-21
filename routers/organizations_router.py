import json
from uuid import uuid4

from flask import Blueprint, Response, request, Request, jsonify
from flask_cors import CORS, cross_origin

from auth.token_manager import check_correct_token, get_token_info
from database.organizations_database import OrganizationsDatabase
from database.organizations_members_database import OrganizationsMembersDatabase
from modules.organization import Organization
from responses import response_not_correct_data, response_not_correct_token
from utils import check_request


class OrganizationRouter:
    def __init__(self, org_db: OrganizationsDatabase, org_members_db: OrganizationsMembersDatabase):
        self.database = org_db
        self.database_members = org_members_db
        self.blueprint = Blueprint("organizations", __name__)


        @self.blueprint.route("/organizations", methods=["POST"])
        @cross_origin()
        def organizations_create() -> tuple[Response, int]:
            return self.__organizations_create(request)

        @self.blueprint.route("/organizations", methods=["GET"])
        @cross_origin()
        def organizations_get() -> tuple[Response, int]:
            return self.__organizations_get(request)

        @self.blueprint.route("/organizations", methods=["DELETE"])
        @cross_origin()
        def organizations_remove() -> tuple[Response, int]:
            return self.__organizations_remove(request)

        @self.blueprint.route("/organizations/members", methods=["POST"])
        @cross_origin()
        def organizations_addmember() -> tuple[Response, int]:
            return self.__organizations_members_add(request)

        @self.blueprint.route("/organizations/members", methods=["GET"])
        @cross_origin()
        def organizations_getmembers() -> tuple[Response, int]:
            return self.__organizations_members_get(request)

        @self.blueprint.route("/organizations/members", methods=["DELETE"])
        @cross_origin()
        def organizations_deletemember() -> tuple[Response, int]:
            return self.__organizations_members_delete(request)

    def __organizations_create(self, request: Request):
        if not check_request(request):
            return response_not_correct_data()

        data: dict = json.loads(request.data.decode())
        token = request.headers.get("Authorization")

        if not check_correct_token(token):
            return response_not_correct_token()

        login = get_token_info(token)["login"]
        org_id = str(uuid4())
        try:
            self.database.create_organization(Organization(org_id, data['title'], data['description'], login))
        except Exception as e:
            print(e)
            return jsonify({"response": {"error": "Organizations not create"}}), 400
        return jsonify({"response": org_id}), 200

    def __organizations_get(self, request: Request):

        data: dict = json.loads(request.data.decode())
        token = request.headers.get("Authorization")

        if not check_correct_token(token):
            return response_not_correct_token()

        try:
            organization_info = self.database.get_organization(request.args.get('org_id'))
        except Exception as e:
            print(e)
            return jsonify({"response": {"error": "Organization not found"}}), 400
        return jsonify({"response": organization_info.get_dict()}), 200

    def __organizations_remove(self, request: Request):
        if not check_request(request):
            return response_not_correct_data()

        data: dict = json.loads(request.data.decode())
        token = request.headers.get("Authorization")

        if not check_correct_token(token):
            return response_not_correct_token()

        try:
            self.database.remove_organization(data['org_id'])
        except Exception as e:
            print(e)
            return jsonify({"response": {"error": "Organization not deleted"}}), 400
        return jsonify({"response": "good"}), 200

    def __organizations_members_add(self, request: Request):
        if not check_request(request):
            return response_not_correct_data()

        data: dict = json.loads(request.data.decode())
        token = request.headers.get("Authorization")

        if not check_correct_token(token):
            return response_not_correct_token()

        try:
            self.database_members.add_member(data['org_id'], data['member_login'])
        except Exception as e:
            print(e)
            return jsonify({"response": {"error": "Not added member to org"}}), 400
        return jsonify({"response": "good"}), 200

    def __organizations_members_get(self, request: Request):
        if not check_request(request):
            return response_not_correct_data()

        data: dict = json.loads(request.data.decode())
        token = request.headers.get("Authorization")

        if not check_correct_token(token):
            return response_not_correct_token()

        try:
            users = self.database_members.get_members(request.args.get('org_id'))
        except Exception as e:
            print(e)
            return jsonify({"response": {"error": "Not can get users"}}), 400
        return jsonify({"response": users}), 200

    def __organizations_members_delete(self, request: Request):
        if not check_request(request):
            return response_not_correct_data()

        data: dict = json.loads(request.data.decode())
        token = request.headers.get("Authorization")

        if not check_correct_token(token):
            return response_not_correct_token()

        try:
            self.database_members.remove_member(data['org_id'], data['member_login'])
        except Exception as e:
            print(e)
            return jsonify({"response": {"error": "User not can been remove"}}), 400
        return jsonify({"response": "good"}), 200
