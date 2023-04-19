import json

'''
create a helper function to create ai-plugin.json method w the following:

FIELD	TYPE	DESCRIPTION / OPTIONS	REQUIRED
schema_version	String	Manifest schema version	✅
name_for_model	String	Name the model will used to target the plugin	✅
name_for_human	String	Human-readable name, such as the full company name	✅
description_for_model	String	Description better tailored to the model, such as token context length considerations or keyword usage for improved plugin prompting.	✅
description_for_human	String	Human-readable description of the plugin	✅
auth	ManifestAuth	Authentication schema	✅
api	Object	API specification	✅
logo_url	String	URL used to fetch the plugin's logo	✅
contact_email	String	Email contact for safety/moderation reachout, support, and deactivation	✅
legal_info_url	String	Redirect URL for users to view plugin information	✅
HttpAuthorizationType	HttpAuthorizationType	"bearer" or "basic"	✅
ManifestAuthType	ManifestAuthType	"none", "user_http", "service_http", or "oauth"	
interface BaseManifestAuth	BaseManifestAuth	type: ManifestAuthType; instructions: string;	
ManifestNoAuth	ManifestNoAuth	No authentication required: BaseManifestAuth & { type: 'none', }	
ManifestAuth	ManifestAuth	ManifestNoAuth, ManifestServiceHttpAuth, ManifestUserHttpAuth, ManifestOAuthAuth	
'''
def create_ai_plugin_json(schema_version, name_for_model, name_for_human, description_for_model, description_for_human, auth, api, logo_url, contact_email, legal_info_url):
    return {
        "schema_version": schema_version,
        "name_for_model": name_for_model,
        "name_for_human": name_for_human,
        "description_for_model": description_for_model,
        "description_for_human": description_for_human,
        "auth": auth,
        "api": api,
        "logo_url": logo_url,
        "contact_email": contact_email,
        "legal_info_url": legal_info_url
    }

def write_ai_plugin_json_to_file(ai_plugin_json, file_path):
    print ("Writing ai-plugin.json to file: " + file_path)
    print(ai_plugin_json)

    # if file doesn't exist, create it
    with open(file_path, 'w+') as outfile:
        json.dump(ai_plugin_json, outfile, indent=4)

def cli_create_ai_plugin_json():
    schema_version = input("schema_version: ") or "1.0.0"
    name_for_model = input("name_for_model: ") or "my_model"
    name_for_human = input("name_for_human: ") or "My Model"
    description_for_model = input("description_for_model: ") or "My model is a model that models things."
    description_for_human = input("description_for_human: ") or "My model is a model that models things."
    
    auth = {}
    auth["type"] = input("auth_type: ") or "none"
    auth["instructions"] = input("auth_instructions: ") or "No authentication required."
    if auth["type"] == "user_http":
        auth["http_authorization_type"] = input("auth_http_authorization_type: ") or "bearer"
    elif auth["type"] == "service_http":
        auth["http_authorization_type"] = input("auth_http_authorization_type: ") or "bearer"
    elif auth["type"] == "oauth":
        auth["oauth_authorization_url"] = input("auth_oauth_authorization_url: ") or "https://example.com/oauth/authorize"
        auth["oauth_token_url"] = input("auth_oauth_token_url: ") or "https://example.com/oauth/token"
        auth["oauth_scopes"] = input("auth_oauth_scopes: ") or "read"
        auth["oauth_client_id"] = input("auth_oauth_client_id: ") or "1234567890"
        auth["oauth_client_secret"] = input("auth_oauth_client_secret: ") or "1234567890"


    '''
    "api": {
        "type": "openapi",
        "url": "http://localhost:3333/openapi.yaml",
        "is_user_authenticated": false
    },
    '''
    api = {}
    api["type"] = input("api_type: ") or "openapi"
    api["url"] = input("api_url: ") or "http://localhost:3333/openapi.yaml"
    api["is_user_authenticated"] = input("api_is_user_authenticated: ") or False


    logo_url = input("logo_url: ") or "https://example.com/logo.png"
    contact_email = input("contact_email: ") or "test@mail.com"
    legal_info_url = input("legal_info_url: ") or "https://example.com/legal.html"
    ai_plugin_json = create_ai_plugin_json(schema_version, name_for_model, name_for_human, description_for_model, description_for_human, auth, api, logo_url, contact_email, legal_info_url)
    file_path = input("file_path: ") or "./.well-known/ai-plugin.json"
    write_ai_plugin_json_to_file(ai_plugin_json, file_path)

if __name__ == "__main__":
    cli_create_ai_plugin_json()