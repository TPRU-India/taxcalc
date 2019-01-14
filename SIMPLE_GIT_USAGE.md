Simple Git Usage
================

This list of elementary git commands assumes that you (1) have read
the [USA Tax-Calculator Contributor
Guide](https://github.com/PSLmodels/Tax-Calculator/blob/master/CONTRIBUTING.md#tax-calculator-contributor-guide),
(2) have forked the [central GitHub pitaxcalc-demo
repository](https://github.com/TPRU-demo/pitaxcalc-demo) to your
GitHub account, and (3) have cloned your forked repository to your
local computer.  After doing these three things: the central GitHub
repository is known as `upstream` and your personal forked GitHub
repository is known as `origin`.  Below we will refer to the cloned
repository on your computer as the `local repo`.

Git is a complex distributed version control system and there are many
ways to use it.  Below are a few simple git commands that do basic
things in your local repo.

**List all branches and find out which branch you're on**
```
git branch
```

**Check overall status of current branch**
```
git status
```

**Switch to another existing branch**
```
git checkout [existing-branch-name]
```

**Synchronize local repo with origin and upstream repositories**
```
gitsync
```
or if master is the current branch
```
git fetch upstream
git merge upstream/master
git push origin master
```

**Create a new branch**
```
git checkout -b [new-branch-name]
```

**List all file changes on current branch since last commit**
```
git diff
```

**Add new file to local repo**
```
git add [new-file-name]
```

**Rename existing file in local repo**
```
git mv [existing-file-name] [new-file-name]
```

**Remove (that is, delete) existing file from local repo**
```
git rm [existing-file-name]
```

**Merge other branch contents into current branch**
```
git merge [other-branch-name]
```

**Revert uncommitted file changes on current branch**
```
git checkout -- [existing-file-name]
```

**Commit file changes to current branch**
```
git commit -a -m "[short-description]"
```

**Push committed changes to current branch to origin**
```
git push origin [existing-branch-name]
```

**Submit pushed branch as pull request**
```
do this interactively in your browser at the
[central GitHub pitaxcalc-demo
repository](https://github.com/TPRU-demo/pitaxcalc-demo)
```

**Delete an old branch from local repo**
```
git branch -d [existing-branch-name]
```

**Make a new local branch same as a pending GitHub pull request**
```
gitpr [PRNUM]
```
or if master is the current branch
```
git fetch upstream pull/[PRNUM]/head:pr-[PRNUM]
git checkout pr-[PRNUM]
git status
```
