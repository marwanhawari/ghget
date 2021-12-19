# TODO

1. Initial request to contents - then you can tell if it is a file or a dir
2. If file - then download file
    Need a new method to construct raw_url
3. If dir - then need to need to second a request to the root of the repo to get the tree SHA of the dir of interest
4. Then do a 3rd request to the tree SHA of the dir of interest and mkdir and download files for everything in the response



1. Make 1 request to the root of the dir to get the tree
2. Save what their specific file/dir to download was (ex: docs/algorithms) -> algorithms is now the root dir where everything will be saved
3. 