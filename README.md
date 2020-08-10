Visualtisations over at: [BlueSmiley.Github.io/Github_REST_requests](https://bluesmiley.github.io/Github_REST_requests/)
# DISCLAIMER
More detailed scraping and visualisation available in the alt directory.    
However I think it looks uglier despite being technically more impressive in terms of amount of data being pulled and displayed.      
Hence why the main visualisation uses different json and shows less data.    

I don't have time to fix some of the bugs with the visualisation at alt.       
Bugs include : 
1. Zoom and dragging being janky
2. Names overflowing small bubbles
3. Bubble names being displayed in wrong order/prominence
4. The color ranges messing up due to extremes of churn ratios from small bubbles all the way to parent repo bubbles
5. Child bubbles block clickability and hover over their parent bubbles even though child should be unclickable

The code in alt is technically more up to date with more refactoring, actual unit tests (which exist because complexity of info handling increased) and documentation in the classes for the functions. The visualisation is more adanced with zoom,drag and title being sideways. Also more data being displayed as well as scraped (Crucially with same Github data usage I think.) The scraper runs a lot slower due to more IO I think as a result.

# Detailed Visuals
Visualisation of alternate at [BlueSmiley.Github.io/Github_REST_requests/alt](https://bluesmiley.github.io/Github_REST_requests/alt)
Loads a bit slower but be patient!!!    
Zoom possible with mouse wheel. Drag with mouse. A bit janky. All functionality of normal visualisation applies to alt so click, coloring etc. Now basically shows a lot more in depth info about every single commit rather than just aggregate. Also note that for each user it only shows the repos and commits of some of the most recent commits of the user I believe.

# Technical info
There's an extra feature that came for free with fixing some naming standards. Now the repos and users are connected so from a user u can click on repo to get more info on repo if the repo data had been scraped and it automatically displays. This is really cool if u scrape a smaller repo and u make the scraping more recursive and smarter/scrape some more repos anyway you get a web like traversal behaviour. You can't see this in my example very well because it's a gigantic repo with so many users with so many repos they contribute to and make that the chances of having most of these repos are non-existent. If you ever clikc on an user and one of their repos is the kubernetes one you will see that happening though( eg. Caerxuchou). I didn't make the crawler recursive by default due to "rate limits issues" for DFS and "extra complexity + memory + probably going to get rate limited anyway so why bother" for BFS. But should be easy enough to implement/modify if u want since scraping users and scraping repo functions are already built.

Name clashes if two users have repo with same name, but this always existed as filenames can't have / characters but fully qualified names on github are basically name/reponame. Low chances of collision in my opinion.

# Github_REST_requests
Repository demonstrating using the github v3 REST API to pull data

Visualtisations over at: [BlueSmiley.Github.io/Github_REST_requests](https://bluesmiley.github.io/Github_REST_requests/)

Bubbles can be clicked to get in depth info on the user.  
Reload to go back to start because I haven't made a back button  

# Data being pulled:
Pick a repository and the scraper gets all the users and their total additions and deletions in the project.  
It also tries to get the contributions of the user to different repositories. unfortunately u will probably get rate limited before you are done so only a sample of the bubbles are clickable.

**The color correspond to the ratio of deletions/additions. Which is used as a proxy for churn. The higher the ratio the greater the percent of estimated churn. I think colors currently go from cadetblue to darkseagreen.**

**The size of the bubbles correspond to the number of additions.**

**Click on user bubbles for in depth info on user - Note: Some users don't have any scraped data**

**Current displayed repo = Kubernetes/Kubernetes**

# Using scraper.py
It does some basic authentication, the help function should show how to use it.  
Repository needs to be fully qualified name.  
**Scapes first every user commit stat in repo chosen.**
**Then tries scraping all commit stats of every user across all repositories to compare performance.***

Dependencies:
1. PyGithub
2. Python 2 preferably
3. d3.js (linked to in js script so okay)

Uses local files and directly outputs files as json rather than to a database so storage space will probably be used up

python crawler.py (whatever options you want)  
Change the base repo file being read by modifying the main  
Then run the index file on firefox :-)  

# Making it all js was way simpler for now rather than designing an actual django app or hosting a server
