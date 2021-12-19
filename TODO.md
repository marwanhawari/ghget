1. Write tests
    - https vs http vs nothing (str.partition won't work)
    - root repo, root repo on diff branch/tag, top level dir, nested dir, top level file, nested file

Known bugs:
- If branch/tag has a / in it, it won't work
   - if I have branches 'main', 'main/ghget', need to distinguish b/w:
     - https://github.com/marwanhawari/ghget/tree/main/ghget (the ghget folder in the main branch)
     - https://github.com/marwanhawari/ghget/tree/main/ghget (the root of the main/ghget branch)