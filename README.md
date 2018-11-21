# Github_REST_requests
Repository demonstrating using the github v3 REST API to pull data

Visualtisations over at: BlueSmiley/Github.io/Github_REST_requests

Bubbles can be clicked to get in depth info on the user. 
Reload to go back to start because I haven't bothered making a back button

# Data being pulled:
Pick a repository and the scraper gets all the users and their total additions and deletions in the project 
It also tries to get the contributions of the user to different repositories. unfortunately u will probably get rate limited before you are done so only a sample of the bubb;es are clickable.

**The color correspond to the ratio of deletions/additions. Which is used as a proxy for churn. The higher the ratio the greater the percent of estimated churn. I think colors currently go from cadetblue to darkseagreen.**

**The size of the bubbles correspond to the number of additions.**

**Click on user bubbles for in depth info on user - Note: Some users don't have any scraped data**

**Current displayed repo = Kubernetes/Kubernetes**

# Using scraper.py
It does some basic authentication, the help function should show how to use it.
Repository needs to be fully qualified name
**Scapes first every user commit stat in repo chosen.**
**Then tries scraping all commit stats of every user across all repositories to compare performance.***

Dependencies:
1. PyGithub
2. Python 2 preferably
3. d3.js (linked to in js script so okay)
4. Uses local files and directly outputs files as json rather than to a database so storage space will probably be used up

python crawler.py (whatever options you want)
Change the base repo file being read by modifying the main
Then run the index file on firefox :-)

# maybe eventually I'll integrate this with docker, maybe later with django for server sideness but making it all js was way simpler for now
