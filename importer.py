#!/usr/bin/env python
#
# USAGE: ./importer.py <filename>
#
# Copy the content of the Google document into a textfile. Hope that nothing changed since Uprising. Follow the instructions to create issues in the netrunner repository.

import sys
import re
import getpass
from github import Github

class Card:
    def __init__(self, name=None, faction=None, type=None, text=None):
        self.name = name
        self.faction = faction
        self.type = type
        self.text = text

    def issue_title(self):
        return "{0.faction} - {0.name}".format(self)

    def issue_body(self):
        return """### {0.name}
{0.faction} - {0.type}
> {1}

### Progress
- [ ] Implement functionality
- [ ] Write tests""".format(self, "\n".join(self.text))

def read_file(fn):
    cards = []
    with open(fn, 'r') as f:
        curr_card = Card()
        for l in f:
            match = re.match(r'^(.+?)\t(.+?)\t(.+?)\t"(.+?)$', l)
            if match:
                cards.append(curr_card)
                curr_card = Card(name=match.group(2), faction=match.group(1), type=match.group(3), text=[match.group(4)])
            else:
                l = l.strip()
                if l[-1] == '"':
                    l = l[:-1]
                curr_card.text.append(l)
        cards.append(curr_card)
    return cards[1:]

def main():
    print("Reading cards...")
    cards = read_file(sys.argv[1])
    print()

    print("Loaded cards:")
    for c in cards:
        print(c.issue_title())
    print()

    username = input("Enter Github username: ")
    password = getpass.getpass("Enter Github password: ")

    g = Github(username, password)

    print()
    reponame = input("Enter repository name (default: NoahTheDuke/netrunner-future): ")
    if not reponame:
        reponame = "NoahTheDuke/netrunner-future"
    repo = g.get_repo(reponame)

    print("Using repository: %s (%d open issues)" % (repo.name, repo.open_issues_count))

    input("Ready to create %d issues for new cards. Press ENTER to continue..." % len(cards))

    for c in cards:
        print("Creating issue for %s" % c.name, end='... ')
        repo.create_issue(title=c.issue_title(), body=c.issue_body(), labels=["New Card"])
        print("done.")

if __name__ == "__main__":
    main()
