# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import json

import requests
import os
from datetime import datetime

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", None)
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

GITHUB_GRAPHQL_ALL_REPO_QUERY = """
{
  organization(login: "eon-com") {
    repositories(last: 100, orderBy: {direction: DESC, field: PUSHED_AT}) {
      totalCount
      allRepos: edges {
        repo: node {
          isFork
          isPrivate
          isArchived
          name
          description
          createdAt
          pushedAt
          updatedAt
          refs(refPrefix: "refs/heads/", orderBy: {direction: DESC, field: TAG_COMMIT_DATE}, first: 100) {
            __typename
            edges {
              node {
                __typename
                branchname: name
                target {
                  ... on Commit {
                    pushedDate
                    authoredDate
                    committedDate
                    author {
                      name
                      email
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
"""

GITHUB_GRAPHQL_STATS_QUERY = """
query {
  repository(owner: \"{{user}}\", name: \"{{repo}}\") {
    openIssues: issues(states: OPEN) {
      totalCount
    },
    closedIssues: issues(states: CLOSED) {
      totalCount
    },
    releasesCount: releases(last: 100){
      totalCount
    },
    lastRelease: releases(last:1){
       nodes {
        name,
        publishedAt,
        url
      }
    },
    lastPush: defaultBranchRef {
      target {
        ... on Commit {
          history(first: 1){
            edges{
              node {
                committedDate
              }
            }
          }
        }
      }
    },
    watchers(last:100){
      totalCount
    },
    stargazers(last:100){
      totalCount
    }
  }
}"""

def to_date(date_str):
	return date_str
	#return datetime.fromisoformat(date_str.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M:%S %z")


def main():
    graph_ql_query = GITHUB_GRAPHQL_ALL_REPO_QUERY
    auth = "token "  + GITHUB_TOKEN
    response = requests.post(GITHUB_GRAPHQL_URL,
                             headers={"Content-Type": "application/json; charset=utf-8",
                                      "Authorization": auth},
                             json={'query': graph_ql_query})

    if response.status_code != 200:
        print("!! Error while querying Github API")
        print("!!   Status: {}".format(response.status_code))
        print("!!   Body: {}".format(response.text))
        return dict()

    data = response.json()
    if not data:
        print("!! No data available from Github API")
        return dict()

    totalCount = data["data"]["organization"]["repositories"]["totalCount"]
    allReposList = data["data"]["organization"]["repositories"]["allRepos"]

    allStats = list()

    # created, Repo-Name, isPrivate, lastcomit, commitby, branch
    for repoDataDict in allReposList:
        statsResult = dict()
        repo = repoDataDict['repo']
        repoName = repo["name"]
        print(repoName)

        graph_ql_query = GITHUB_GRAPHQL_STATS_QUERY \
            .replace("{{user}}", "eon-com") \
            .replace("{{repo}}", repoName)

        response = requests.post(GITHUB_GRAPHQL_URL,
                                 headers={"Content-Type": "application/json; charset=utf-8",
                                          "Authorization": auth},
                                 json={'query': graph_ql_query})

        if response.status_code != 200:
            print("!! Error while querying Github API")
            print("!!   Status: {}".format(response.status_code))
            print("!!   Body: {}".format(response.text))
            return dict()


        data = response.json()
        if not data:
            print("!! No data available from Github API")
            return dict()


        repository_values = data["data"]["repository"]
        release_count = repository_values["releasesCount"]["totalCount"]
        statsResult.update(repo="{}/{}".format("eon-com", repoName),
                      open_issues=repository_values["openIssues"]["totalCount"],
                      closed_issues=repository_values["closedIssues"]["totalCount"],
                      releases=release_count,
                      watchers=repository_values["watchers"]["totalCount"],
                      stars=repository_values["stargazers"]["totalCount"],
                      last_push=to_date(
                          repository_values["lastPush"]["target"]["history"]["edges"][0]["node"]["committedDate"]))


        if release_count:
            latest_release = repository_values["lastRelease"]["nodes"][0]
            statsResult.update(latest_release=latest_release["name"],
                          latest_release_date=to_date(latest_release["publishedAt"]),
                          latest_release_url=latest_release["url"])

        allStats.append(statsResult)
        print(statsResult)

    with open("meta.json", 'w+') as jsonStats:
        jsonStats.write("[")

        for stat in allStats:
            jsonStats.write(json.dumps(stat))
            jsonStats.write(",")
        jsonStats.write("]")

if __name__ == "__main__":
    main()

