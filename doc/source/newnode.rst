.. _newnode:

Step by step guide to a new VAMDC node
======================================

Let's have a look at the structural diagram from the :ref:`intro` once more:

.. image:: nodelayout.png
   :width: 700 px
   :alt: Structural layout of a VAMDC node

If you have followed the instructions of the page on :ref:`prereq`, you 
are done with the yellow box in the figure. This page will tell you 
first how to configure and write the few code bits that your node needs 
before running (blue box), and then how to deploy the node and make it run 
as shown in the violet box.

It goes like this:

* Get the Nodesoftware and make a copy of the example node.
* Auto-create a new settings file and put your database connection there.
* Either
    * Write your data model and let Django create the database from it. Then use the import tool to put your data there.
    * Let Django write the model from an existing database that you already have.
* Assign names from the VAMDC dictionary to your data to make them globally understandable.
* Start/deploy your node and test it.


But let's take it step by step:

The main directory of your node
---------------------------------

Let's give the directory which holds your copy of :ref:`source` (it is 
called NodeSoftware and exists whereever you ran the *git clone* 
command, unless you moved it elsewhere and/or renamed it, which is 
absolutely no problem) a name and call it *$VAMDCROOT*. Let's also assume
the name of the dataset is *YourDBname*.

Inside $VAMDCROOT you find several subdirectories. For setting up a new 
node, you only need to care about the one called *nodes/* which contains 
the files for several nodes already, plus the example node. The first 
thing to do, is to make a copy of the ExampleNode::

    $ git clone git://github.com/VAMDC/NodeSoftware.git
    $ export VAMDCROOT=`pwd`/NodeSoftware/
    $ # (the last line is for Bash-like shells, for C-Shell use *setenv* instead of *export*
    $ cd $VAMDCROOT/nodes/
    $ cp -a ExampleNode YourDBname
    $ cd YourDBname/
 
Inside your node directory
---------------------------------

The first thing to do inside your node directory is to run::

    $ ./manage.py

This will generate a new file *settings.py* for you. This file is where 
you override the default settings which reside in *settings_default.py* (which you should not edit!). 
There are two configurations items that you need to fill

* The information on how to connect to your database.
* A name and email address for the node administrator(s).

You can leave the default values for now, if you do not yet know what to 
fill in.

There are only three more files that you will need to care about:

* *node/models.py* is where you put the data model,
* *node/dictionaries.py* is where you put the dictionaries and
* *node/queryfunc.py* is where you write the query function,

all of which will be explained in detail in the following.

The data model and the database
---------------------------------

By *data model* we mean the piece of Python code that tells Django the 
layout of the database, including the relations between the tables. By 
*database* we mean the actual relational database that is to hold the 
data. See :ref:`concepts` for some more lines on this.

There are two basic scenarios to come up with these two ingredients. 
Either the data are already in a relational database, or you want to 
create one.

Case 1: Existing database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to deploy the VAMDC node software on top of an existing 
relational database, the *data model* for Django can be automatically 
generated by running::

    $ ./manage.py inspectdb > node/models.py

This will look into the database that you told Django about in *settings.py* above 
and create a Python class for each table in the database and attributes 
for these that correspond to the table columns. An example may look like 
this::

    from django.db.models import *

    class Species(Model):
        id = IntegerField(primary_key=True)
        name = CharField(max_length=30)
        ion = IntegerField()
        mass = DecimalField(max_digits=7, decimal_places=2)
        massno = IntegerField()
        class Meta:
            db_table = u'species'

There is one important thing to do with these model definitions, apart 
from checking that the columns were detected correctly: The columns that 
act as a pointer to another table need to be replaced by *ForeignKeys*, 
thereby telling the framework how the tables relate to each other. This 
is best illustrated in an example. Suppose you have a second model, in 
addition to the one above, that was auto-detected as follows::

    class State(Model):
        id = IntegerField(primary_key=True)
        species = IntegerField()
        energy = DecimalField(max_digits=17, decimal_places=4)
        ...

Now suppose you know that the field called *species* is acutally a 
reference to the species-table. You would then change the class *State* 
as such::

    class State(Model):
        id = IntegerField(primary_key=True)
        species = ForeignKey(Species)
        energy = DecimalField(max_digits=17, decimal_places=4)
        ...

.. note:: 
    You will probably have to re-order the classes inside the file 
    *models.py*. The class that is referred to needs to be defined before 
    the one that refers to it.

Once you have finished your model, you should test it. Continuing the 
example above you could do::

    $ ./manage.py shell
    >>> from node.models import *
    >>> allspecies = Species.objects.all()
    >>> allspecies.count()
    XX # the number of species is returned
    >>> somestates = State.objects.filter(species__name='He')
    >>> for state in somestates: print state.energy


Case 2: Create a new database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this case we assume that the data are in ascii tables of arbitrary 
layout. The steps now are as follows:

#. Write the data model in $VAMDCROOT/nodes/YourDBname/node/models.py
#. Create an empty database with corresponding user and password
#. Tell the node software where to find this database.
#. Let the node software create the tables
#. Use the import tool to fill the database with the data.

First of all, you need to think about how the data should be structured. 
Data conversion (units, structure etc) can and should be done while 
importing the data since this saves work and execution time later. Since 
the data will need to be represented in the common XSAMS format, it is 
recommended to adopt a layout with separate tables for species, states, 
processes (radiative, collisions etc) and references.

Deviating data models are certainly possible, but will involve some more 
work on the query function (see below). In any case, do not so much 
think about how your data is structured now, but how you want it to be 
structured in the database, when writing the models.

Writing your data models is best learned from example. Have a look at 
the example from Case 1 above and at file *$VAMDCROOT/nodes/vald/node/models.py* 
inside the NodeSoftware to see how the model for VALD looks like. Keep 
in mind the following points:

* As mentioned, a *class* in the model becomes a *table* in the 
  database and the fields/members of the class correspond to the
  table columns.
* Each class should have one member with *primary_key=True*. If 
  not, one called *id* will be implicitly created for you.
* How you name your classes and fields is up to you. Sensible names will
  make it easier to write the dictionaries below.
* Use the appropriate field type for each bit of data, e.g. BooleanField, 
  CharField, PositiveSmallIntegerField, FloatField. There is also a 
  DecimalField that allows you to specify arbitrary precision which will 
  also be used in later ascii-representations of data.
* Use *ForeignKey()* to another class's primary key to connect your tables.
* The full list of possible fields can be found at
  http://docs.djangoproject.com/en/1.2/ref/models/fields/.
* If you know that a field will be empty sometimes, add *null=True*
  to the field definition inside the brackets ().
* For fields that are frequent selection criteria (like wavelength for
  a transition database), you can add *db_index=True* to the field
  to speed up searches along this column (at the expense of some
  disk space and computation time at database creation).
* If you do not define a table name for your model with the Meta class,
  as in the first example above, the table in the database will be named
  as the model, but lowercase and with a prefix *node_*.

Once you have a first draft of your data model, you test it by running::

    $ cd $VAMDCROOT/nodes/YourDBname/
    $ ./manage.py sqlall node

This will (if you have no error in the models) print the SQL statements 
that Django will use to create the database, using the file or 
connection information in *settings.py*. If you do not know SQL, you can 
ignore the output and move straight on to creating the database::

    $ ./manage.py syncdb

Now you have a fresh empty database. You can test it with the same 
commands as mentioned at the end of Case 1 above, replacing "Species" 
and "State" by you own model names.

.. note::
    There is no harm in deleting the database and re-creating it
    after improving your models. After all, the database is still
    empty at this stage and *syncdb* will always create it for
    you from the models, even if you change your database
    engine in *settings.py*.

.. note::
    If you use MySQL as your database engine, we recommend its internal
    storage engine InnoDB over the standard MyISAM. You can set this in 
    your settings.py by adding *'OPTIONS': {"init_command": 
    "SET storage_engine=INNODB"}* to your database setup. We also
    recommend to use UTF8 as default in your MySQL configuration or
    create your database with *CREATE DATABASE <dbname> CHARACTER SET utf8;*


How you fill your database with information from ascii-files is 
explained in the next chapter: :ref:`importing`. You can do this now and 
return here later, or continue with the steps below first.



The query routine
-----------------------------------

Now that we have a working database and the data model in place, we need 
to tell the framework how to run a query. This is a single function 
called *setupResults()* that must be written in the file 
*node/queryfunc.py* inside the directory of your node. You will find an
example on how this should work in that same file. It works like this:

* setupResults() is called from elsewhere and you need not run it 
  yourself.
* setupResults() gets an object as input, called *sql*.
  This is a parsed version of the query that holds the WHERE-part
  as *sql.where* and so on.
* We now need to run this query on the data model in order to get so
  called *QuerySets* which are basically unevaluated queries that
  can are simply passed on to the XML generator that takes care of
  the rest.
* You can also enforce limits on how much data can be returned.
* You should also calculate some statistics on how much information
  a query returns and return it as header information.

In a concrete example of an atomic transition database, it looks like this:

.. literalinclude:: queryfunc.py
   :linenos:

Explanations on what happens here:

* Lines 1-4: We import some helper functions from the sqlparser and the 
  dictionaries and models that reside in the same directory as 
  *queryfunc.py*
* Line 7: This uses the helper function where2q() to 
  convert the information in *sql.where* to QueryObjects that match your 
  model, using the RESTRICTABLES (see below). The result from where2q() is
  a string that needs to be executed with eval().
* In line 8 we simply pass these QueryObjects to the Transition model's 
  filter function. This returns a QuerySet, an unevaluated version of the 
  query.
* Line 9: We use the count() method on the QuerySet to get the 
  number of transitions.
* Line 11-14: We check if the number is larger than our limit and shorten
  the QuerySet if necessary. We also prepare a string with the percentage
  for the headers.
* Line 16-20: We use the ForeignKeys from the Transition model to the 
  State model that tell us which are the upper and lower states for a 
  transition. We put their ids in to a set which throws out duplicates and 
  then use this set of state_ids to get the QuerySet for the states that 
  belong to the selected transitions.
* Line 22-24: An alternative, more straight forward way to achieve the 
  same thing. This uses the ForeignKeys in the *inverse* direction, 
  connects the two queryObjects by an OR-relation, selects the states and 
  then throws away duplicates. The first approach proves faster if the 
  number of duplicates is large.
* Lines 26-27: We run count() on the states to get their number for the 
  headers and do a quick selection and count on the species, again using a 
  ForeignKey from the Transition model, this time to the Species.
* Lines 29-34: Put the statistics into a key-value structure where the 
  keys are the header names as definded by the VAMDC-TAP standard and the 
  values are the strings/numbers that we calculated above.
* Lines 37-40: Return the QuerySets and the headers, again as key-value 
  pairs. The keys that you can use here correspond to the major parts of 
  XSAMS and are named as:
  * Sources
  * AtomStates
  * MoleStates
  * CollTrans
  * RadTrans
  * Methods
  * MoleQNs
  * HeaderInfo

.. note::
    As you might have noticed, all restrictions are passed to the 
    Transitions model in the above example. This does not mean that we 
    cannot put constraints on e.g. the species here. We simply use the 
    models ForeignKey in that case in the RESTRICTABLES. An entry there 
    could e.g. be *'AtomIonCharge':'species__ion'* which will use the *ion* 
    field of the species model. Depending on your database layout, it might 
    not be possible to pass all restrictions to a single model. Then you 
    need to write a more advanced query than the shortcuts in Lines 7-8.

More comprehensive information on how to run queries within Django can be found at http://docs.djangoproject.com/en/1.2/topics/db/queries/.

The dictionaries
----------------------------------

As the last important step before the new node works, we need to define 
how the data relates to the VAMDC *dictionary*. If you have not done so 
yet, please read :ref:`conceptdict` before continuing.

What needs to be put into the file *node/dictionaries.py* is the 
definition of two variables that map the individual fields of the 
data model to the names from the dictionary, like this::

    RESTRICTABLES = {\
    'AtomSymbol':'species__name',
    'AtomStateEnergy':'upstate__energy',
    'AtomIonCharge':'species__ion',
    'RadTransWavelengthExperimentalValue':'vacwave',
    }

    RETURNABLES={\
    'SourceID':'Source.id',
    'SourceCategory':'journal', # using a constant string works
    'AtomStateEnergy':'AtomState.energy', 
    'RadTransWavelengthExperimentalValue':'RadTran.vacwave',
    }
    
.. note::
    There are tools for getting started with writing these and for
    validiation once you are done at http://vamdc.tmy.se/dict/

About the RESTRICTABLES
~~~~~~~~~~~~~~~~~~~~~~~~

As we have learned from writing the query function above, we can use the 
RESTRICTABLES to match the VAMDC dictionary names to places in our data 
model. The key in each key-value-pair is a name from the VAMDC 
dictionary and the values are the members of the model class that you 
want to query primarily.

The example above fits the one from the section about the query function 
above, so we know that the "main" model is the Transitions. Now if a 
query like "AtomIonCharge > 1" comes along, this can be translated into 
*Transition.objects.filter(species__ion__gt=1)* without further ado. 
Note that we here used a ForeignKey to the Species model; the values in 
the RESTRICTABLES need to be written from the perspective of the main 
model.

.. note::
    Even if you chose to not use the RESTRICTABLES in your 
    setupResults(), you are still encouraged to fill the keys (with the 
    values being empty), because they are automatically provided to the 
    VAMDC registry so that external services can figure out which names make 
    sense to query at this node.


About the RETURNABLES
~~~~~~~~~~~~~~~~~~~~~~~~

Equivalent to how the RESTRICTABLES take care of translating from global 
names to your custom data model when the query comes in, the 
RETURNABLES do the opposite on the way back, i.e. when the data reply 
is sent.

Again the keys of the key-value-pairs are the global names from the 
VAMDC dictionary. The values now are their corresponding places in the 
QuerySets that are constructed in setupResults() above. This means that 
the XML generator will loop over the QuerySet, getting each element, and 
try to evaluate the expression that you put in the RETURNABLES. 

Continuing our example from above, assume the State model has a field 
called *energy*, so each object in the QuerySet will have that value at 
*AtomState.energy*. Note that the first part before the dot is not the 
name of your model, but the *singular* of one of the names that you 
return from setupResults() (see above).

.. note::
    Again, at least the keys of the RETURNABLES should be filled (even 
    if you use your own generator for the XML output) because this allows 
    the registry to know what kind of data your node holds before querying 
    it.


Testing the node
------------------------------

Now you should have everything in place to run your node. If you still 
need to fill your database with the import tool, now is the time to do 
so according to :ref:`importing`.

Django comes with a built-in server for testing. You can start it
with::

$ ./manage.py runserver

This will use port 8000 at your local machine which means that you 
should be able to browse to http://127.0.0.1:8000/tap/availability/ and 
hopefully see a positive status message.

You should also be able to run queries by accessing URLS like::

    http://127.0.0.1:8000/tap/sync?LANG=VSS1&FORMAT=XSAMS&QUERY=SELECT ALL WHERE AtomIonCharge > 1

replacing the last part by whatever restriction makes sense for your data set.

.. note::
	The URL has to be URL-encoded when testing from a script or
	similar. Web browsers usually do that for you. To also see
	the statistics headers, you can use *wget -S -O output.xml "<URL>"*.

A more extensive test framework is in the making and will be documented 
here soon. In any case you should run test queries to your node and make 
sure that the output in terms of volume and values matches your 
expectations.


Deployment in Apache
--------------------------------

How and on which server you set up your node to run permanently, is much 
dependent on your technical resources and the solution we give here is 
just one out of several possibilities. It involves the Apache webserver 
and its mod_wsgi plugin to run Python code. You can find two example 
files in your node directory:

* *apache.conf*: This is an Apache config file that defines a virtual 
  server, bound to a certain host name. You will have to edit several 
  things in that file before it will work in Apache: the server name
  and the path to the node software in a few places. On a Debian-like 
  system you would then move this file to 
  */etc/apache2/sites-available/vamdcnode* and run *a2ensite vamdcnode* to 
  activate it.
* *django.wsgi*: This is the file that the previous one points to in its 
  WsgiScriptAlias. Edit the path and your node's name.

Once you have set this up and re-started the Apache webserver, your node 
should deliver data at the configured URL.
