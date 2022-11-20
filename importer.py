#!/usr/bin/env python
#
# USAGE: ./importer.py <filename>
#
# Copy the content of the Google document into a textfile. Hope that nothing changed since Uprising. Follow the instructions to create issues in the netrunner repository.

import sys
import csv
import re
import getpass
from github import Github
import time

def issue_title(c):
    return "{0[Set Number]} - {0[Faction]} - {0[Card Name (English - For Translation)]}".format(c)

def issue_body(c):
    out = []
    out.append("### {0[Card Name (English - For Translation)]}")
    out.append("{0[Faction]} - {0[Type]}")

    out.append("")
    out.append("> {0[Card Text]}")
    out.append("")

    out.append("### Progress")
    out.append("- [ ] Implement functionality")
    out.append("- [ ] Write tests")

    return '\n'.join(out).format(c);

def read_file(fn):
    cards = []
    with open(fn, 'r') as f:
        r = csv.DictReader(f, delimiter=',')
        cards = list(r)
    return cards

def main():
    print("Reading cards...")
    cards = read_file(sys.argv[1])
    print()

    print("Loaded %d cards:"%len(cards))
    for c in cards:
        print(issue_title(c))
    print()

    access_token = "INSERT_TOKEN_HERE" # TODO: change this
    g = Github(access_token)

    reponame = input("Enter repository name (default: NoahTheDuke/netrunner-future): ")
    if not reponame:
        reponame = "NoahTheDuke/netrunner-future"
        print("Choosing %s"%reponame)

    repo = g.get_repo(reponame)

    print("Using repository: %s (%d open issues)" % (repo.name, repo.open_issues_count))

    input("Ready to create %d issues for new cards. Press ENTER to continue..." % len(cards))

    for c in cards:
        print("Creating issue for {0[Card Name (English - For Translation)]}".format(c), end='... ')
        repo.create_issue(title=issue_title(c), body=issue_body(c), labels=["New Card"])
        #  print("Would create: {0}".format(issue_title(c)))
        print(issue_body(c))
        print("done.")
        time.sleep(3) # get around ratelimiting

if __name__ == "__main__":
    main()
