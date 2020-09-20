#!/bin/bash


if test $# != 1
then
    echo "Error: Please provide your credentials csv as an argument in the command line."
    exit 1
fi

if [ ! -f "$1" ]
then
    echo "Error: The file you have provided does not exist.\n\tPlease make sure your credentials are in the current working directory."
    exit 1
fi

if [[ $1 =~ accessKeys.*\.csv$ ]]
then
    access_key=`sed -n 2p $1|cut -d',' -f1`
    secret_access_key=`sed -n 2p $1|cut -d',' -f2`
elif [[ $1 =~ credentials.*\.csv$ ]]
then
    access_key=`sed -n 2p $1|cut -d',' -f3`
    secret_access_key=`sed -n 2p $1|cut -d',' -f4`
else
    echo "Error: Please provide your credentials csv as an argument in the command line.\n\tPerhaps you have renamed your credentials file?\n\tYour file name should end in 'accessKeys.csv' or 'credentials.csv'"
    exit 1
fi

aws configure set aws_access_key_id $access_key
aws configure set aws_secret_access_key $secret_access_key
aws configure set default.region ap-southeast-2
echo "Your AWS CLI has been successfully configured"
