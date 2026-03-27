import argparse
import os
from typing import Iterable

import requests
from azure.identity import ClientSecretCredential
from fabric_cicd import (
    FabricWorkspace,
    append_feature_flag,
    change_log_level,
    publish_all_items,
    unpublish_all_orphan_items,
)


def get_workspace_id(workspace_name: str, credential: ClientSecretCredential) -> str:
    token = credential.get_token("https://api.fabric.microsoft.com/.default")
    response = requests.get(
        "https://api.fabric.microsoft.com/v1/workspaces",
        headers={
            "Authorization": f"Bearer {token.token}",
            "Content-Type": "application/json",
        },
        timeout=30,
    )

    if response.status_code != 200:
        raise ValueError(f"Error retrieving workspaces: {response.status_code}, {response.text}")

    for workspace in response.json()["value"]:
        if workspace["displayName"] == workspace_name:
            return workspace["id"]

    raise ValueError(f"Workspace {workspace_name} was not found.")


def first_env_value(names: Iterable[str]) -> str:
    for name in names:
        value = os.getenv(name)
        if value:
            return value

    joined_names = ", ".join(names)
    raise KeyError(f"Expected one of these environment variables to be set: {joined_names}")


def parse_item_types(raw_value: str) -> list[str]:
    items = []
    for item in raw_value.strip().strip("[]").split(","):
        cleaned = item.strip().strip('"').strip("'")
        if cleaned:
            items.append(cleaned)

    if not items:
        raise ValueError("items_in_scope must contain at least one Fabric item type.")

    return items


append_feature_flag("enable_shortcut_publish")
append_feature_flag("enable_lakehouse_unpublish")
change_log_level("DEBUG")

parser = argparse.ArgumentParser(description="Deploy Fabric items from the repository.")
parser.add_argument("--aztenantid", type=str, required=True, help="Tenant ID")
parser.add_argument("--azclientid", type=str, required=True, help="Service principal client ID")
parser.add_argument("--azspsecret", type=str, required=True, help="Service principal secret")
parser.add_argument("--target_env", type=str, required=True, help="Target environment")
parser.add_argument("--items_in_scope", type=str, required=True, help="Fabric item types to deploy")
args = parser.parse_args()

target_env = args.target_env
workspace_var_name = f"{target_env}WorkspaceName"
workspace_name = first_env_value([workspace_var_name, workspace_var_name.upper()])
repository_directory = first_env_value(["GITDIRECTORY", "gitDirectory"])
item_types = parse_item_types(args.items_in_scope)

print(f"Target environment set to {target_env}")
print(f"Using workspace name from {workspace_var_name}: {workspace_name}")
print(f"Deploying from repository directory: {repository_directory}")

credential = ClientSecretCredential(
    tenant_id=args.aztenantid,
    client_id=args.azclientid,
    client_secret=args.azspsecret,
)
workspace_id = get_workspace_id(workspace_name, credential)
print(f"Resolved workspace ID for {workspace_name}: {workspace_id}")

target_workspace = FabricWorkspace(
    workspace_id=workspace_id,
    environment=target_env,
    repository_directory=repository_directory,
    item_type_in_scope=item_types,
    token_credential=credential,
)

publish_all_items(target_workspace)
unpublish_all_orphan_items(target_workspace)
