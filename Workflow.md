This File contains our development workflow and a little introduction on how to work with git.

Initial steps:

1. Create a directory on your desktop mkdir /home/AI-for-Business
2. Move to the directory cd /home/AI-for-Business
3. Clone our development repository: git clone https://github.com/MasterDDB/product3team2
4. Go to directory AI-for-Business
5. Tell git to cache your username and pw so you don't have to type it in everytime you push smth git config --global credential.helper cache

The development team has a daily standup in the morning and developer A is assigned a story. This story is identified by a unique number (e.g. 13).
1. Developer A goes off to his computer, where A has a cloned copy of the project github repository. A creates a new BRANCH from the MAIN branch called: 'story-13-..description..', where 'description' must be replaced with a short description of the story topic.
2. A works on the story, writing the code that implements it and testing that it works. When done for the day, A commits its work to the remote branch.
3. The next day A works a bit more on the story, until it's complete. At this point A commits the new changes and pushes them to the remote branch. 
4. Then A creates a pull request to merge the remote branch into the remote MAIN branch. Once this request is reviewed by the other team members, A merges the pull request into the MAIN branch.

TO actualize your branch with the master branch
1. git pull --rebase origin main
