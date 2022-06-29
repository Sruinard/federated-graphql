# federated-graphql

az ad sp create-for-rbac --name "graphql-azure" --role contributor \
    --scopes /subscriptions/<subscription-id>/resourceGroups/<group-name>/ \
    --sdk-auth