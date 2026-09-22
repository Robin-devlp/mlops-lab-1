***Robin Ghassibeh (231463)***

### Question 1: Observe the files created, what do you think they contain.

uv init created pyproject.toml, .python-version, README.md and a src folder. pyproject.toml holds the project settings like the name, the Python version and the list of dependencies. .python-version says which Python version the project uses. README.md is an empty description of the project and the src folder has a small starter package with a main function that prints a hello message.

### Question 2: What are the created files. What do you think they are used for? And which ones should be pushed to git?

dvc init created the .dvc folder and the .dvcignore file. Inside .dvc there is a config file for the DVC settings like the remote, a .gitignore that keeps the local DVC files out of git and a tmp folder for temporary files. .dvcignore lists the files DVC should ignore. The ones to push to git are .dvc/config, .dvc/.gitignore and .dvcignore.

### Question 3: Where are the credentials stored? and what are the options other than --global? Should the credentials be pushed to github?

With --global the credentials are saved in a DVC config file in the user folder, outside the project. With --local they go in .dvc/config.local and only apply to this project on this computer. With --project they go in .dvc/config which is pushed to git. With --system they apply to every user on the computer. The credentials should not be pushed to GitHub because the repo is public and anyone could use them to access the data. That's why I put the URL in the project config and the username and token with --local, since config.local is ignored by git.

### Question 4: Take a look at the .gitignore file. Explain what happened.

dvc add created a .gitignore file with the line /data. This makes git ignore the data folder so the images don't go to GitHub. DVC tracks the data instead and keeps a copy of it in .dvc/cache.

### Question 5: Do you see a .dvc file? What does it contain?

Yes, a data.dvc file was created. It contains the md5 hash of the data folder, its size, the number of files and the path. Git tracks this small file instead of the actual data and DVC uses the hash to know which version of the data to get.

### Question 6: You can check your main branch on the github web UI. Is the code there? Is the data there? Do you have any file that points to the data location. And what about dagshub web UI do you see the data?

The code is on GitHub but the data is not, there is no data folder there. The file that points to the data is data.dvc. It has the hash of the data folder and .dvc/config has the DagsHub URL where the data is stored. On DagsHub I can see the data folder marked as DVC with the training, evaluation and validation folders and all the images inside.

### Question 7: In a completely new temporary folder clone your github repo. Do you see the data folder? What dvc command is needed to get the data folder?

No, after git clone the data folder is not there. Git only downloads the code and the data.dvc pointer because the data itself is tracked by DVC and stored on DagsHub. To get it back we run dvc pull, which reads data.dvc and downloads the matching files from the DVC remote. Since config.local is not in git, the username and token have to be set again with --local in the new clone before pulling. In short git brings the code and the pointer while dvc pull brings back the actual dataset.

### Question 8: Do you still see the new folders you created? food11_processed and food11_processed_mini?

No. After going back to the commit that only tracked the raw data and running dvc checkout, the data folder only had food11_raw and the processed and mini folders were gone. That is because data.dvc in that old commit points to the older version of the data. After git checkout main and dvc checkout again, both folders came back from the local DVC cache without downloading anything.
