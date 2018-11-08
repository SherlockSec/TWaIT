# TWaIT
Twin With an Interesting Twist (TWaIT) is a website cloning with a twist.

## What is TWaIT?

TWaIT uses tools such as `httrack` and `beef-xss` among others to create an authentic looking clone.

## What's with the name?

We originally came up with `Twin With A Twist`, and didn't see anything wrong. It was only when we made this repo that we noticed the abbriviation. We then very quickly changed the name once we realised our mistake. The new name is `Twin With an Interesting Twist`.

## How does it work?

TWaIT clones a website using `httrack`, then injects a `beef-xss` hook and hosts it locally using `apache2`. This makes an identical copy apart from the hook.

## How do you use it?

The useage of the tool is as follows   
```sudo ./twait.py -u [URL] -o [OUTPUT FOLDER] -p [BEEF IP]```  
And here is an example:  
``` sudo ./twait.py -u https://www.catgirlcareco.org -o catgirl -p 127.0.0.1```  
(Make Neko's Not Nukes)  

## Where can we find you?

[@SherlockSec](https://twitter.com/SherlockSec) - Twitter
