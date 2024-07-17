Hit the api endpoint.. 

The endpoint returns 1 post that has not yet been published to mastodon. 

How is this done

It will select for posts id's that are not in the mastodon posts table. 

It will Return the post data in json format


## The Client App

### Hits the endpoint for some data

### Hits the mastodon endpoint

### Update the database via an update endpoint




## The Mastodon Post Table

* Id : Auto increment
* PostId: The post url
* PostDate: The actualPost Date
* SocialLink: The actual Social Link, VarChar 255
* SocialPostDate: The actual social post date


