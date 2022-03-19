from api.client import AtlasAdminClient

PROJECT_ID = ""
PUBLIC_KEY = ""
PRIVATE_KEY = ""

client = AtlasAdminClient(
    project_id=PROJECT_ID, public_key=PUBLIC_KEY, private_key=PRIVATE_KEY
)

database_name = "test-db"
username = client.create_database_user(database_name=database_name)
user = client.get_database_user(username=username)
client.delete_database_user(username=username)
