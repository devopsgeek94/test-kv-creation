# Show Azure subscription information
 
import os
#from azure.mgmt.resource import SubscriptionClient
from azure.identity import DefaultAzureCredential
from azure.identity import EnvironmentCredential
from azure.keyvault.secrets import SecretClient

import json

# EnvironmentCredential assumes that the following environment variables are set:
#     AZURE_TENANT_ID
#     AZURE_CLIENT_ID
#
# Plus one of the following (which are attempted in this order):
#     AZURE_CLIENT_SECRET
#  or:
#     AZURE_CLIENT_CERTIFICATE_PATH
#  or:
#     AZURE_USERNAME and AZURE_PASSWORD

# NOTE: AZURE_SUBSCRIPTION_ID isn't used directly by EnvironmentCredential and is used here
# only for convenience. You can retrieve the subscription ID from any suitable source.
subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]

credential = EnvironmentCredential()
#credential = DefaultAzureCredential()

#subscription_client = SubscriptionClient(credential)

keyVaultName = 'KVpython'
KVUri = f"https://{keyVaultName}.vault.azure.net"

client = SecretClient(vault_url=KVUri, credential=credential)

#secretName = "test3"
#secretValue = 1234567

# Opening JSON file
f = open('keys.json')
 
# returns JSON object as
# a dictionary
keys = json.load(f)
 
# Iterating through the json
# list
# keys = {"6": "Sachin Tendulkar", "7": "Dravid", "8": "Sehwag", "9": "Laxman", "10": "Kohli"}

for secretName,secretValue in keys.items():
#    print(secretName)
 print(f"Creating a secret in {keyVaultName} called '{secretName}' with the value '{secretValue}' ...") 
 client.set_secret(secretName, secretValue)

print(" done.")

print(f"Retrieving your secret from {keyVaultName}.")

for secretName in keys:
 retrieved_secret = client.get_secret(secretName) 
 print(f"Your secret is '{retrieved_secret.value}'.") 
 print(f"Deleting your secret from {keyVaultName} ...") 
 poller = client.begin_delete_secret(secretName) 
 deleted_secret = poller.result()

print(" done.")

# Closing file
f.close()
