#!/bin/bash

# This script is dependent on jq. On macos use `brew install jq` or on linux use `apt-get install jq`
SECURITY_GROUP_ID="$1"
REGION="eu-west-2"
PROFILE="$2"

IP_RANGES=$(curl -s https://api.github.com/meta | jq -r '.actions[]')

for IP in $IP_RANGES
do
  aws ec2 authorize-security-group-ingress --region $REGION --group-id $SECURITY_GROUP_ID --protocol tcp --port 22 --cidr $IP --profile $PROFILE
done
