# SUPER IMPORTANT DISCLAIMER
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

Feels mostly minor imo

# SECOND IMPORTANT DISCLAIMER
The code in alt is technically more up to date with more refactoring, actual unit tests (which exist because complexity of info handling increased) and documentation in the classes for the functions. The visualisation is more adanced with zoom,drag and title being sideways. Also more data being displayed as well as scraped (Crucially with same Github data usage I think.) The scraper runs a lot slower due to more IO I think as a result.

# Basically if ur looking for decent unit tests I guess there are some in the alt directory 
# Also more functionality being displayed/scraped so if I get marks for that look there as well.
# If I lose marks for the result looking uglier then well...use the main visualisation

# LAST DISCLAIMER
Visualisation of alternate at [BlueSmiley.Github.io/Github_REST_requests/alt](https://bluesmiley.github.io/Github_REST_requests/alt)
Loads a bit slower but be patient!!!    
Zoom possible with mouse wheel. Drag with mouse. A bit janky. All functionality of normal visualisation applies to alt so click, coloring etc. Now basically shows a lot more in depth info about every single commit rather than just aggregate. Also note that for each user it only shows the repos and commits of some of the most recent commits of the user I believe.

Read rest of this to understand what those disclaimers are talking about. I might add a license to this later but basically I just don't take any liability for this software.


# Github_REST_requests
Repository demonstrating using the github v3 REST API to pull data

Visualtisations over at: [BlueSmiley.Github.io/Github_REST_requests](https://bluesmiley.github.io/Github_REST_requests/)

Bubbles can be clicked to get in depth info on the user.  
Reload to go back to start because I haven't bothered making a back button  

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
4. Uses local files and directly outputs files as json rather than to a database so storage space will probably be used up

python crawler.py (whatever options you want)  
Change the base repo file being read by modifying the main  
Then run the index file on firefox :-)  

# maybe eventually I'll integrate this with docker, maybe later with django for server sideness but making it all js was way simpler for now
