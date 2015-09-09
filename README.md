# MySQL Directory Tree

Once I got test task at interview  where I was required to create a webapp (using Python and MySQL) 
which would represent directory structure with possibility to add and remove directories and to 
show and hide their structure. I didn't make it at the time, but after I got some experience I decided to 
make at least prototype of the app, so here it is. It uses D3.js for rendering directory structure and
Flask with Flask-RESTful for backend.

Please note that MySQL in general doesn't work really well with tree-like structures, here I used so-called
[Nested Set Model](http://mikehillyer.com/articles/managing-hierarchical-data-in-mysql/) for implementing it, 
but, again, in general you will need something more suitable than relational model databases.  

## Installation

You have to have mysql server installed and running at localhost.

```
git clone
cd 
pip install -r requirements.txt
mysql -h localhost -u <username> -p < dbgen.sql 

```

## Usage

```
python dbtree.py
```
will run Flask development server ( You may change it to Gunicorn, if you like, but in this case it doesn't matter much).

Open your browser at 127.0.0.1:5000.

I highly recommend to use [virtualenv](http://pypi.python.org/pypi/virtualenv) and run all the above in dedicated environment.

## License
MIT
