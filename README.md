# spoiler_core
My legacy to mankind. A fully functional spoiler generator with enough power to upset any GoT fan. It fetches its spoilers by crawling tvtropes

## Abstract
I used variants of this code for some of my other personal projects. Now you can, too!  
It does not randomly generate spoiler, instead, it fetches them from tvtropes.org  
The folks at tvtropes are nice enough to thoroughly mark every single spoiler on their pages,
but I found a way to use it for evil.  
(Basically, just scrape the text inside any paragraph containing a spoiler tag)

## Running
To get a taste of it, run:

    python spoiler_core.py
    
## Hacking
Just import the `SpoilerCore` class in your code, and call `getRandomSpoiler()`  
I may create a proper python package someday.
