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

def sumList(jsonList, name):
    """
    Sums additions and deletions inside list of dicts representing json objects

    Args:
        jsonList =  A list containing json objects with Add and Del key value
        pairs
        name =  The name for the json object represented by the dict returned

    Effects:
        Probably bubbles back a key not found exception if any of the json
        objects don't contain a Del or Add field.

        Possibly references same objects as in the list since I don't explicitly
        deep copy each dict in the list.

    Returns:
        A python dict representing a Json object with a Name, Add, Del and
        children key value pairs. The name pair corresponds to the name passed
        as the argument to this function and the children embeds each element
        of the list passed as the argument to this function in a new list.
    """
    adds = 0
    dels = 0
    jsonDict = {}
    embedList = []
    for elem in jsonList:
        adds += elem["Add"]
        dels += elem["Del"]
        embedList.append(elem)
    jsonDict.update({
        "Name": name,
        "Add" : adds,
        "Del" : dels,
        "children" : embedList
    })
    return jsonDict

def updateDict(jsonDict, jsonList):
    """
    Updates a dictionary with the new list values

    Args:
        jsonDict = The target dictionary representing a json object
        jsonList = the source list to be appended to the children of the 
            dictionary

    Effects:
        Probably key error if dict does not have expected key values of 
        children, Add and Del
        Appends same elements to the children as in list (no deep copy)
    
    Return:
        The modified jsonDict with the list appended to the children list and
        the add and del of the dict modified to account for new children values.
    """
    adds = jsonDict["Add"]
    dels = jsonDict["Del"]
    childrenList = jsonDict["children"]
    for elem in jsonList:
        adds += elem["Add"]
        dels += elem["Del"]
        childrenList.append(elem)
    jsonDict["Add"] = adds
    jsonDict["Del"] = dels 
    jsonDict["children"] = childrenList
    return jsonDict
    

# I processed data in a very specific way in the index file and
# its easier to make this match the format than fix the index file
def crawl(g, reponame):
    """ 
    Crawls a given repo to fetch commit information about all users who
    contributed to the repo and stores info into json files

    Args:
       g = Github instance
       reponame = Name of repo to be crawled
    
    Effects:
        Writes multiple json files to local file storage encoding the scraped
        data.

        Sends GET requests to Github API

        Prints to stdout if errors

    Returns: void
    """
    #enable_console_debug_logging() -- debugging command for pyGithub apparently
    repo = g.get_repo(reponame)
    contributors = repo.get_stats_contributors()
    repoData = []
    for c in contributors:
        userData = []
        for week in c.weeks: 
            userData.append({
                "Name": week.w.strftime("%x"),
                "Add" : week.a,
                "Del" : week.d
            })
        totalUserData = sumList(userData,c.author.login)
        repoData.append(totalUserData)
    data = sumList(repoData,(reponame.split("/"))[1])

    with open((reponame.split("/"))[1] + '.json', 'w') as outfile:  
        json.dump(data, outfile)
    #This here kills ur rate limit :)
    crawl_users(g,  repo.get_contributors())
        
# This is probably a bit unsuitable due to the amount of data requests fired
# The quality of info for this stuff was pretty low but thats's the price you
# pay for third party libraries employig multiple abstractions to make it easier
def crawl_users(g, contributors):
    """
    Crawls all contributors in given contributor list for recent commit history 
    of the contributor and stores info into json files

    Args:
       g = Github instance
       contributors = PyGithub representation (Paginated list I believe) of 
            contributors to a project
    
    Effects:
        Writes multiple json files to local file storage encoding the scraped
        data.
        Sends GET requests to Github API
        Prints to stdout if errors

    Returns: void
    """
    for author in contributors:
        repoStore = {}
        for event in author.get_events():
            if event.type == "PushEvent":
                # Some wierd interaction is going on with python dict keys and names
                # ignore deleted repos since github wont let you acess them
                try:
                    repoName = (event.repo.full_name.split("/"))[1]
                    repoInfo = repoStore.get(repoName,{
                    "Name":repoName,
                    "Add":0,
                    "Del":0,
                    "children":[]
                    })
                    repoCommits = []
                    commits = event.payload["commits"]
                    actualrepo = g.get_repo(event.repo.full_name)
                    for commit in commits:
                        commitdata = actualrepo.get_commit(sha=commit["sha"])
                        repoCommits.append({
                            "Name": commitdata.commit.message,
                            "Add" : commitdata.stats.additions,
                            "Del" : commitdata.stats.deletions
                        })
                        updateDict(repoInfo,repoCommits)
                        #repo["Add"] += commitdata.stats.additions
                        #repo["Del"] += commitdata.stats.deletions
                    
                    repoStore[repoName] = repoInfo
                except KeyboardInterrupt:
                    raise
                except:
                    print "repo deleted/private?"
                    pass
        
        repoList = []
        for repo in repoStore.keys():
            repoList.append(repoStore[repo])
        data = sumList(repoList,author.login)
        with open(author.login + '.json', 'w') as outfile:  
            json.dump(data, outfile)
            
    
def help():
    """Helper function that prints to stdout how to use this file"""

    print("crawler.py option_name \n")
    print("option_name = \n None: For using limited rate access.\n" + 
        "Login: For login using github username and password.\n" +
        "Token: For login using github access token.\n")
    print("Then enter in the appropriate values for any fields that pop up\n")
    print("Repository = name of repo this script should crawl")
    


if __name__ == "__main__":
    main()