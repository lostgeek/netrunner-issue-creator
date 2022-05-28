#!/usr/bin/env python
#
# USAGE: ./importer.py <filename>
#
# Copy the content of the Google document into a textfile. Hope that nothing changed since Uprising. Follow the instructions to create issues in the netrunner repository.

import sys
import re
import getpass
from github import Github
import time

def issue_title(c):
    return "{0[Faction]} - {0[Card Name]}".format(c)

def issue_body(c, hs):
    headers = hs[:] # pass by value
    out = []
    out.append("### {0[Card Name]}")
    out.append("{0[Faction]} - {0[Type]}")

    headers.remove('Card Name')
    headers.remove('Faction')
    headers.remove('Type')
    headers.remove('Card Text')

    for h in headers:
        if h in c.keys() and c[h]:
            out.append(h+': {0['+h+']}')

    out.append("")
    out.append("> {0[Card Text]}")
    out.append("")

    out.append("### Progress")
    out.append("- [ ] Implement functionality")
    out.append("- [ ] Write tests")

    return '\n'.join(out).format(c);

def get_headers(fn):
    cards = []
    with open(fn, 'r') as f:
        curr_card = {}
        lines = [line.rstrip() for line in f]
        return lines[0].split('\t')

def read_file(fn, headers):
    cards = []
    with open(fn, 'r') as f:
        curr_card = {}
        lines = [line.rstrip() for line in f]
        for l in lines[1:]:
            if l.count('\t') < 12: # this must be another line of card text instead of a new card
                curr_card['Card Text'] += '\n' + l
            else:
                cards.append(curr_card)
                values = l.split('\t');
                curr_card = dict(zip(headers, values))
    cards.append(curr_card)
    return cards[1:]

def main():
    print("Determining headers...")
    headers = get_headers(sys.argv[1])
    print()

    print("Reading cards...")
    cards = read_file(sys.argv[1], headers)
    print()

    print("Loaded %d cards:"%len(cards))
    for c in cards:
        print(issue_title(c))
    print()

    #  username = input("Enter Github username: ")
    #  password = getpass.getpass("Enter Github password: ")
    #  g = Github(username, password)

    access_token = "INSERT_TOKEN_HERE" # TODO: change this
    g = Github(access_token)

    print(g)
    reponame = input("Enter repository name (default: NoahTheDuke/netrunner-future): ")
    if not reponame:
        reponame = "NoahTheDuke/netrunner-future"
        print("Chosing %s"%reponame)

    repo = g.get_repo(reponame)

    print("Using repository: %s (%d open issues)" % (repo.name, repo.open_issues_count))

    input("Ready to create %d issues for new cards. Press ENTER to continue..." % len(cards))

    for c in cards[40:]:
        print("Creating issue for {0[Card Name]}".format(c), end='... ')
        repo.create_issue(title=issue_title(c), body=issue_body(c, headers), labels=["New Card"])
        print("done.")
        time.sleep(5) # get around ratelimiting

if __name__ == "__main__":
    main()
