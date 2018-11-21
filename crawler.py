import sys
import cmd
import getpass
import json
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
            if sys.version_info[0] < 3:
                reponame = raw_input("Repository:")
            else:
                reponame = input("Repository:")
            crawl(g,reponame)
        elif(sys.argv[1]=="Login"):
            if sys.version_info[0] < 3:
                username = raw_input("Username:")
            else:
                username = input("Username:")
            password = getpass.getpass("Password:")
            g = Github(username,password)
            if sys.version_info[0] < 3:
                reponame = raw_input("Repository:")
            else:
                reponame = input("Repository:")
            crawl(g,reponame)
        elif(sys.argv[1]=="Token"):
            token = getpass.getpass("Github Token:")
            g = Github(token)
            if sys.version_info[0] < 3:
                reponame = raw_input("Repository:")
            else:
                reponame = input("Repository:")
            crawl(g,reponame)
        else:
            print("Unknown parameters\n")
            help()

def crawl(g, reponame):
    #enable_console_debug_logging()
    repo = g.get_repo(reponame)
    #contributors = repo.get_contributors()
    contributors = repo.get_stats_contributors()
    data = {}
    data.update({
        "Name" : (reponame.split("/"))[1],
        "Add" : 0,
        "Del" : 0,
        "children" : []
    }) 
    data["children"] = []
    repo_adds = 0
    repo_dels = 0
    for c in contributors:
        total_additions = 0
        total_deletions = 0
        for week in c.weeks: 
            total_additions += week.a
            total_deletions += week.d
        repo_adds += total_additions
        repo_dels += total_deletions
        data["children"].append({
            "Name": c.author.login,
            "Add" : total_additions,
            "Del" : total_deletions
        })
        data["Add"] = repo_adds
        data["Del"] = repo_dels
    #This here kills ur rate limit :)
    crawl_users(g,  repo.get_contributors())
    with open((reponame.split("/"))[1] + '.json', 'w') as outfile:  
        json.dump(data, outfile)
        
# This is probably a bit unsuitable due to the amount of data requests fired
# Also midway through making this the documentation became sparse/non-existent
# I got this all working as far as I can tell
# But relucatant to throw away good possibly working code
# Also I have a feeling the pygithub abstraction leaks so a lot more requests
# Than even I imagine probably happen
def crawl_users(g, contributors):
    #Or why you should use an ORM rather than work with raw data and json
    for author in contributors:
        data = {}
        data.update({
             "Name" : author.login,
             "Add" : 0,
             "Del" : 0,
             "children" : []
        })
        rinfo = {}
        tAdd = 0
        tDel = 0
        for event in author.get_events():
            if event.type == "PushEvent":
                # Some wierd interaction is going on with python dict keys
                # it keeps not using whole string as key
                #ignore deleted repos since github wont let you acess them
                # Says file not found so maybe they dont even store them haha
                try:
                    repo = rinfo.get(event.repo.full_name,{
                    "Add":0,
                    "Del":0,
                    })
                    commits = event.payload["commits"]
                    actualrepo = g.get_repo(event.repo.full_name)
                    for commit in commits:
                        commitdata = actualrepo.get_commit(sha=commit["sha"])
                        repo["Add"] += commitdata.stats.additions
                        repo["Del"] += commitdata.stats.deletions
                    rinfo[event.repo.full_name] = repo
                except:
                    print "repo deleted?"
                    pass
        
        for reponame in rinfo.keys():
            usr_info = rinfo[reponame]
            tAdd += usr_info["Add"]
            tDel += usr_info["Del"]
            #This format is for visualisation...maybe ORM would have helped here
            data["children"].append({
                "Name": reponame,
                "Add" : usr_info["Add"],
                "Del" : usr_info["Del"]
             })
        data["Add"] = tAdd
        data["Del"] = tDel
        with open(author.login + '.json', 'w') as outfile:  
            json.dump(data, outfile)
            
    
def help():
    print("crawler.py option_name \n")
    print("option_name = \n None: For using limited rate access.\n" + 
        "Login: For login using github username and password.\n" +
        "Token: For login using github access token.\n")
    print("Then enter in the appropriate values for any fields that pop up\n")
    print("Repository = name of repo this script should crawl")
    


if __name__ == "__main__":
    main()