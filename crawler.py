import sys
import cmd
import getpass
from github import Github
from github import enable_console_debug_logging

def main():
    if(len(sys.argv)<2):
        print("Error too few arguments\n")
        help()
        return
    else:
        if(sys.argv[1]=="None"): 
            g = Github()
            reponame = raw_input("Repository:")
            crawl(g,reponame)
        elif(sys.argv[1]=="Login"):
            username = raw_input("Username:")
            password = getpass.getpass("Password:")
            g = Github(username,password)
            reponame = raw_input("Repository:")
            crawl(g,reponame)
        elif(sys.argv[1]=="Token"):
            token = getpass.getpass("Github Token:")
            g = Github(token)
            reponame = raw_input("Repository:")
            crawl(g,reponame)
        else:
            print("Unknown parameters\n")
            help()

def crawl(g, reponame):
    #enable_console_debug_logging()
    repo = g.get_repo(reponame)
    #contributors = repo.get_contributors()
    contributors = repo.get_stats_contributors()
    for c in contributors:
        total_additions = 0
        total_deletions = 0
        for week in c.weeks: 
            total_additions += week.a
            total_deletions += week.d
        print("Contributor:" + str(c.author.login) + "\n"
            "Additions:" + str(total_additions) + "\n" + 
            "Deletions:" + str(total_deletions) + "\n")
    
def help():
    print("crawler.py option_name \n")
    print("option_name = \n None: For using limited rate access.\n" + 
        "Login: For login using github username and password.\n" +
        "Token: For login using github access token.\n")
    print("Then enter in the appropriate values for any fields that pop up\n")
    print("Repository = name of repo this script should crawl")
    


if __name__ == "__main__":
    main()