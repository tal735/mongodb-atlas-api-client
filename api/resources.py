API_BASE_URL = "https://cloud.mongodb.com/api/atlas/v1.0"

ROLES_URL = API_BASE_URL + "/groups/{group_id}/customDBRoles/roles"
ROLE_URL = ROLES_URL + "/{role_name}"

DATABASE_USERS_URL = API_BASE_URL + "/groups/{group_id}/databaseUsers"
DATABASE_USER_URL = DATABASE_USERS_URL + "/{database_name}/{username}"
