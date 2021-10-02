import os

# export MYSQL_ROOT_PASSWORD="somepasswordsomepassword"
# echo $MYSQL_ROOT_PASSWORD
MYSQL_ROOT_PASSWORD = os.environ.get("MYSQL_ROOT_PASSWORD")