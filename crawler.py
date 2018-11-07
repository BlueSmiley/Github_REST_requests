import sys
from github import Github
from github import enable_console_debug_logging

def main():
    if(len(sys.argv)<2):
        print("Error too few arguments\n")
        help()
        return
    else:
        if(sys.argv[1]=="None"):
            if(len(sys.argv)<3):
                help()
            else:
                g = Github()
                crawl(g,sys.argv[2])
        elif(sys.argv[1]=="Login"):
            if(len(sys.argv)<5):
                help()
            else:
                g = Github(sys.argv[2],sys.argv[3])
                crawl(g,sys.argv[4])
        elif(sys.argv[1]=="Token"):
            if(len(sys.argv)<4):
                help()
            else:
                g = Github(sys.argv[2])
                crawl(g,sys.argv[3])
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
    print("crawler.py option_name option_params.. github_repo_name \n")
    print("option_name = \n None: For using limited rate access.\n" + 
        "Login: For login using github username and password.\n" +
        "Token: For login using github access token.\n")
    print("option_params = \n Don't enter anything if option=None\n" +
        "github_username password if option=Login\n" +
        "github_acess_token if option=Token\n")
    print("github_repo_name = name of repo this script should crawl")
    


if __name__ == "__main__":
    main()