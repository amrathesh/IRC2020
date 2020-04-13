# IRC2020
The official repository of Team Astra Robotics for IRC 2020

## Getting around the repository

Files pertaining to various tasks in IRC 2020 as well as subsystems in them have been pushed onto the repository for backup and development purposes. Kindly use them and add anymore developments if found. Each folder has a self-explanatory name along with a README file which explains what each code is. Please read them for better understanding of the codes written.

## Instructions for using repository
Seeing that a new repo has been made to put resources onto, doubts might originate on how to go about putting the resources in the right way and also how to access them uniformly. Fret not, for the readme file will explain it as satisfactorily as possible 

>The following commands have been tried and tested on Linux Operating Systems to be working correctly. Execute these as required on terminal or command prompt on your OS after downloading and successfully installing Git. 

If it is required to upload something new, it is required to have the resources that is already on the repo, so first step is to pull all the changes accordingly. In order to do so, run the following commands after setting your configs in git. 
> Here is the link in case you haven't done it : [Git config setup](https://confluence.atlassian.com/bitbucket/configure-your-dvcs-username-for-commits-950301867.html)

Make a directory called "IRC2020" and run the following first:

### Commands to pull 
`git init`
>Initialises the local repository, that is, your folder

`git remote add <nickname> https://github.com/astra-robotics/IRC2020`
>The nickname must be memorable as you will be using this to do further operations without typing or copying the whole link. I will be referencing the nickname as 'x'.

`git pull x master`
>This will download contents of the existing online repo on your own local folder so that things could be updated online with no issues. 

This completes the repository pulling part 

### Commands to push 
`git add -A`
>Adds all the files in the current folder onto the git stream for a commit 

`git commit -m "insert meaningful message"`
>This message is what it will show beside the changed files implying a change or a meaningful message to the others

`git push x master`
>This command pushes all the committed files on your local repository to the online repository for anybody to view and see or just for you to access anywhere
>This also asks for your username and password. Provide username and password of **your** account. As you are added into the github page as a collaborator, it will be fine!

ANDDD YOU ARE DONE! You will have all the new files up and running safely. 

If you are planning to just get the files on your device, you can run the following code below to clone the files only

`git clone https://github.com/astra-robotics/IRC2020`

Happy gitting it ;)
