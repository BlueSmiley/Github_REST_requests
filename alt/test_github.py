import unittest
import sys
from github import Github
import crawler
# Since simple test script of library
# Testing out output functions rather than writing any code

class GithubTest(unittest.TestCase):

    # Test the github samples and pygithub samples work
    # Only testable ones are tested here 
    # I dont like this test because I don't think it's legitimate really
    #def test_main(self):
    #    g = Github()
    #    repo = g.get_repo("PyGithub/PyGithub")
    #    org = g.get_organization("PyGithub")
    #    self.assertEqual(repo.name,"PyGithub")
    #    self.assertEqual(org.login,"PyGithub")
    #    self.assertEqual(repo.get_topics(),
    #        [u'pygithub', u'python', u'github', u'github-api'])
    
    def test_sumList(self):
        testList = [
        {
            "Name": "Blue",
            "Add" : 100,
            "Del" : 10
        },
        {
            "Name": "Smiley",
            "Add" : 300,
            "Del" : 30
        },
        {
            "Name": "Monster",
            "Add" : 500,
            "Del" : 50
        }]
        name = "guest"
        expect = {
            "Name": name,
            "Add" : 900,
            "Del" : 90,
            "children": testList
        }
        res = crawler.sumList(testList,name)
        for key in res.keys():
            self.assertEqual(res[key],expect[key])
    
    def test_updateDict(self):
        testDict = {
            "Add" : 500,
            "Del" : 50,
            "children": [ {
                "Name": "Monster",
                "Add" : 500,
                "Del" : 50
                }]
        }

        testList = [
        {
            "Name": "Blue",
            "Add" : 100,
            "Del" : 10
        },
        {
            "Name": "Smiley",
            "Add" : 300,
            "Del" : 30
        }
        ]

        expect = {
            "Add" : 900,
            "Del" : 90,
            "children": [
                {
                    "Name": "Monster",
                    "Add" : 500,
                    "Del" : 50
                },
                {
                    "Name": "Blue",
                    "Add" : 100,
                    "Del" : 10
                },
                {
                    "Name": "Smiley",
                    "Add" : 300,
                    "Del" : 30
                }]
        }

        res = crawler.updateDict(testDict,testList)
        for key in res.keys():
            self.assertEqual(res[key],expect[key])


# Can't test these ones since mutable IO and results vary over time
# However can print them out
# Can technically test by getting results another way( ie. curl) and then
# extracting out the relevant info and checking if same but not worth effort
# for a simple sample showing basic competence of using a library
def main():
    if(len(sys.argv)<3):
        g = Github()
    else:
        g = Github(sys.argv[1],sys.argv[2])
    user = g.get_user("BlueSmiley")
    for repo in user.get_repos():
        print(repo.name)
        try:
            contents = repo.get_contents("README.md")
            print contents.decoded_content.split("\n")[0] + "\n"
        except:
            pass
        
    repositories = g.search_repositories(query='language:python')
    for index in range(0,10):
       print(repositories[index])
    repo =  g.get_repo("BlueSmiley/Github_REST_requests")
    contributors = repo.get_contributors()
    for contributor in contributors:
        print contributor.login
    


if __name__ == "__main__":
    unittest.main()
