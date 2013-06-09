# [sblog](http://songguo.sinaapp.com/blog) :: A simple and beautiful blog for you

**Note: The original version of the blog is [here](https://github.com/yueyoum/paper). I have done a lot        of modifications to it for meeting my needs.If you do not like sblog, please go to the original version      [here](https://github.com/yueyoum/paper)
**

You may want to skip to [Installation](#Installation).

## Demo

You can visit sblog [here](http://songguo.sinaapp.com/blog).

## Functions or Features added


### Tag Cloud

I add the tag cloud in the right side of sblog. Tag cloud should be generated dynamically according to the number of the corresponding blogs. A python moduel called **python-tagcloud** can do this, but it needs many dependencies which related to OS. 

Because sblog is hosted at [SAE](http://songguo.sinaapp.com) and lack of dependencies **python-tagcloud** needed, so I generate a static tag cloud for sblog. If you use sblog in you own computer or VPS, you can use **python-tagcloud**, it's very cool!

### Excerpt

The home page shows excerpts of the latest blogs sorted by creation time.

You can do a quick view for every blog. If you like some one, you can click the title for details.

### Markdown Live Preview and Post
Thanks for (MD Preview)[markdownlivepreview.com]. You can edit markdown and make a quick preview very very handy. After you finish the edition of your blog, you can post it to your blog database online.
Not every one can post it, it needs security key which set by you!

It is very convenient, isn't?


## Installation and Usage



<a name="Installation" />
# Installation

1. You probably already have python and bottle (if not, go get it right now.  I'll
   wait).  However, for this beast, you will need **python 2.75** and **bottle 0.11**.


2. Get **SQLAlchemy** [here](http://www.sqlalchemy.org/). SQLAlchemy is the Python SQL toolkit and    Object Relational Mapper that gives application developers the full power and flexibility of SQL.

3. Get **markdown**, **jinja2**. You can easily fine them in [PYPI](pypi.python.org).


4. Clone the repository from `git://github.com/songuo/sblog.git`.
   
5. First you should configure your environment in setting.py, including database arguments and so on.         


6. Do the following for initialization:
        
        python syncdb.py
        cat "It's me!" > templates/me.html

   
7. Create your security key:

        python bin/generate_key.py

   
8. Run sblog:

        python app.py

It needs wsgi server for python!


Any questions: [songguo.hit@gmail.com](songguo.hit@gmail.com "mailto:songguo.hit@gmail.com")
