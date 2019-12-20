from flask import Flask, request
import requests
import json

app = Flask(__name__)

@app.route('/allbranches/<owner>/<repository_name>')
def get_all_branches(owner, repository_name):
    repository_branches = []
    page = 1
    headers = {
        'Authorization': 'token %s' % request.args.get('token', '')
    }

    while True:
        branch_data = requests.get("https://api.github.com/repos/%s/%s/branches?page=%s&protected=false" % (owner, repository_name, page), headers=headers)
        branches = json.loads(branch_data.text)

        for each_branch in branches:
            repository_branches.append(each_branch)

        if len(branches) > 0:
            page += 1
        else:
            break

    return {
        "branches": repository_branches[0:1]
    }

@app.route("/branch-details/<owner>/<repository_name>/<branch_name>")
def get_branch_details(owner, repository_name, branch_name):
    headers = {
        'Authorization': 'token %s' % request.args.get('token', '')
    }

    branch_details = requests.get("https://api.github.com/repos/%s/%s/branches/%s" % (owner, repository_name, branch_name), headers=headers)
    return branch_details.json()