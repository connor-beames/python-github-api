import requests
import pandas
import pyodbc
from github import Github
from dotenv import load_dotenv
load_dotenv()
import os

#from repos_class import Repos as rc

#set connection variables
access_token = os.getenv("access_token")
owner = os.getenv("owner")
server = os.getenv("server")
database = os.getenv("database")
user_name = os.getenv("user_name")
password = os.getenv("password")

'''get repositories from github'''
#make an api call and store the response
url = f'https://api.github.com/user/repos?affiliation=owner'
headers = {'Authorization': "Token "+access_token
    , 'Accept': 'application/vnd.github.v3+json'
    }
repos = requests.get(url, headers=headers)
print(f"Status code: {repos.status_code}")

#store api response in a variable
response_dict = repos.json()

#create a list to store classes
repositories = []

#create a class of repo
class Repo:
    """attempt to model a repo"""

    def __init__(self, name, owner, stars, repository, description):
        """initializes a repo"""
        self.name = name
        self.owner = owner
        self.stars = stars
        self.repository = repository
        self.description = description

#create instance of class of repo and store in list
for r in response_dict:
    repo = Repo(
        r['name'],
        r['owner']['login'],
        r['stargazers_count'],
        r['html_url'],
        r['description'],
    )
    repositories.append([repo.name,repo.owner,repo.stars,repo.repository,
        repo.description])

'''insert repositories to database'''
#create connection
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+user_name+';PWD='+password)
cursor = cnxn.cursor()

#create sql query
insert_records = '''
    INSERT INTO raphaelSystem.githubRepos(
        repoName
        ,owner
        ,stars
        ,repository
        ,description
    ) 
    VALUES(
        ?
        ,?
        ,?
        ,?
        ,?)
'''
cursor.executemany(insert_records,repositories)
cnxn.commit()
cursor.close()
cnxn.close()