import requests
from password_generator import PasswordGenerator
from requests.auth import HTTPDigestAuth

from api.resources import DATABASE_USER_URL, DATABASE_USERS_URL, ROLES_URL, ROLE_URL


class AtlasAdminClient:
    def __init__(self, project_id, public_key, private_key):
        self.project_id = project_id
        self.public_key = public_key
        self.private_key = private_key

    # Users
    def get_database_user(self, username):
        url = DATABASE_USER_URL.format(group_id=self.project_id, database_name="admin", username=username)
        response = self._submit_request(requests.get, url)
        user = response.json()
        return user

    def create_database_user(self, database_name):
        url = DATABASE_USERS_URL.format(group_id=self.project_id)

        username = f"port-user-{database_name}"
        password = PasswordGenerator().generate()
        data = {
            "databaseName": "admin",
            "password": password,
            "roles": [{
                "databaseName": database_name,
                "roleName": "dbAdmin"
            }],
            "scopes": [{
                "name": "Cluster0",
                "type": "CLUSTER"
            }],
            "username": username
        }

        response = self._submit_request(requests.post, url, data)

        username = response.json()["username"]
        return username

    def update_database_user(self):
        pass

    def delete_database_user(self, username):
        url = DATABASE_USER_URL.format(group_id=self.project_id, database_name="admin", username=username)
        self._submit_request(requests.delete, url)

    # Roles
    def create_drop_database_role(self, database_name):
        url = ROLES_URL.format(group_id=self.project_id)

        data = {
            "actions": [{
                "action": "DROP_DATABASE",
                "resources": [{
                    "collection": "",
                    "db": database_name
                }]
            }],
            "inheritedRoles": [{
                "db": database_name,
                "role": "dbAdmin"
            }],
            "roleName": f"DropDbRole-{database_name}"
        }

        response = self._submit_request(requests.post, url, data=data)

        role_name = response.json()["roleName"]
        return role_name

    def delete_role(self, role_name):
        url = ROLE_URL.format(group_id=self.project_id, role_name=role_name)
        self._submit_request(requests.delete, url)

    def _submit_request(self, method, url, data=None):
        auth = HTTPDigestAuth(self.public_key, self.private_key)
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        response = method(url=url, json=data, auth=auth, headers=headers)
        assert response.ok
        return response
