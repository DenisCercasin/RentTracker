---
title: Git Workflow
parent: Wiki
nav_order: 3
---

## 🧠 Git Workflow
### Pull (Always UP-to-Date)
- Always pull the latest changes at the beginning and end of the work session to get the latest changes from the remote branch:

```
git pull
```
    
### One branch per feature

- Each feature or task should be developed in its own Git branch. This keeps changes organized and allows for easier testing and merging.

```
git checkout -b branch-name
```
    
### Git fetch (Check Remote Without Changing Local)
- We use git fetch when you want to see changes from the remote repository without affecting my local code. This is helpful if teammate using VS Code has pushed updates - that we want to review, but not yet merge.


```
git fetch
```
### Git merge (Combine Branches)

- Use git merge at the end of a feature when it’s ready to be integrated into main or another shared branch. Only merge after discussing with the teammate to avoid conflicts.

```
git merge branch-name
```
### Git checkout origin/main (Read-Only Test)

- This command switches to the remote version of main on Github (read-only). It’s useful for comparing or testing the current state of the main branch without affecting your local work.

- If the changes look good, switch back to your local branch and merge:
 ```
git checkout main
 ```
 then
   ```
git merge origin/main
   ```
### Git diff origin/main  (Preview Differences)

- We use this to see the differences between my local branch and the remote main branch. It’s useful for previewing changes before merging.

- If the changes look good, switch back to your local branch and merge:
 ```
 git diff origin/main
   ```
### Pull request (Team Collaboration)
- You use it to propose changes from your branch into another branch (usually main). This feature is in Plattforms such as GitHub.

### Git Push (Upload Changes)
- Sends my local commits to the remote repository (e.g., GitHub).  

```
git push 
```

---

### 📚 Sources / Inspiration

- [Atlassian Community: Comparing Git Workflows](https://www.atlassian.com/git/tutorials/comparing-workflows)
- [What is a Git Workflow?](https://about.gitlab.com/topics/version-control/what-is-git-workflow/)
- [Gitflow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
- [Getting started with Git and GitHub workflows, Prof. Dr. Alexander Eck, HWR Berlin](https://hwrberlin.github.io/fswd/git.html)


