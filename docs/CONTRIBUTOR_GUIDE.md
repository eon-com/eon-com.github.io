## Contributor Guide

> _This document is currently work-in-progress. Any feedback is welcome._

**Initial Setup**

1. Fork the project on GitHub.
2. Clone your fork (and enter the project directory).

```
git clone https://github.com/<your-username>/<project-name>.git
cd <project-name>
```

3. Add the upstream project as a remote.

```
git remote add upstream https://github.com/eon-com/<project-name>.git
```

**Making Changes**

1. To make changes, create a new branch.

```
git checkout -b my-changes
```

2. Add, commit, and push the changes to your fork.

```
git add .
git commit -m "My changes"
git push origin my-changes
```

3. On GitHub, open a pull request asking for your changes to be integrated.

**Updating Your Fork**

- To update your fork, pull from the upstream project.

```
git checkout master
git pull upstream master
```
