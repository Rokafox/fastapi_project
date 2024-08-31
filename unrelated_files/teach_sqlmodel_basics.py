from sqlmodel import Field, SQLModel, create_engine, Session, select


class Hero(SQLModel, table=True):
    """
    It's also possible to have models without table=True, those would be only data models, without a table in the database, 
    they would not be table models.
    Those data models will be very useful later, but for now, we'll just keep adding the table=True configuration.
    """
    id: int | None = Field(default=None, primary_key=True)
    """
    id is the primary key of the table.
    So, we need to mark id as the primary key.
    To do that, we use the special Field function from sqlmodel and set the argument primary_key=True
    """
    name: str
    """
    By default, 
    str fields are interpreted as VARCHAR in most databases and VARCHAR(255) in MySQL, 
    this way you know the same class will be compatible with the most popular databases without extra effort.

    We can also have name: str = Field(index=True) to create an index on the name column, this is for quary optimization:
    https://sqlmodel.tiangolo.com/tutorial/indexes/
    """
    secret_name: str
    age: int | None = None


"""
Each supported database has its own URL type. For example, for SQLite it is sqlite:/// followed by the file path.
A "URL type" refers to a connection string or database URL that specifies how to connect to a particular database. 
This URL includes information such as the database type, location, and any necessary credentials.

1. Database Type: Indicates the type of database (e.g., SQLite, PostgreSQL, MySQL).
2. Scheme: The protocol used to connect to the database (e.g., `sqlite`, `postgresql`, `mysql`).
3. Path or Host: The location of the database file or server.
4. Credentials: Username and password for authentication (if required).

Other examples for different databases:
- PostgreSQL: `postgresql://user:password@localhost/dbname`
- MySQL: `mysql://user:password@localhost/dbname`

SQLite supports a special database that lives all in memory. Hence, it's very fast, but be careful, 
the database gets deleted after the program terminates. 
You can specify this in-memory database by using just two slash characters (//) and no file name: sqlite://
"""

sqlite_url = "sqlite:///./unrelated_files/example_database.db"

"""
Create the engine, we are using the argument echo=True.
It will make the engine print all the SQL statements it executes, which can help you understand what's happening.
It is particularly useful for learning and debugging.
But in production, you would probably want to remove echo=True
"""

engine = create_engine(sqlite_url, echo=True)

"""
create the database and table.
Creating the engine doesn't create the example_database.db file.
But once we run SQLModel.metadata.create_all(engine), it creates the example_database.db file and creates the hero table in that database.
Both things are done in the following single step.

The SQLModel class has a metadata attribute. It is an instance of a class MetaData.
Whenever you create a class that inherits from SQLModel and is configured with table = True, it is registered in this metadata attribute.
So, by the last line, SQLModel.metadata already has the Hero registered.
metadata means "data about data".

This MetaData object at SQLModel.metadata has a create_all() method.
It takes an engine and uses it to create the database and all the tables registered in this MetaData object.
"""

def create_db_and_tables():
    """
    If SQLModel.metadata.create_all(engine) was not in a function and we tried to import something from this module 
    (from this file) in another, 
    it would try to create the database and table every time we executed that other file that imported this module.
    """
    SQLModel.metadata.create_all(engine)

"""
Output:
2024-08-30 23:15:34,551 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2024-08-30 23:15:34,551 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("hero")
2024-08-30 23:15:34,552 INFO sqlalchemy.engine.Engine [raw sql] ()
2024-08-30 23:15:34,552 INFO sqlalchemy.engine.Engine PRAGMA temp.table_info("hero")
2024-08-30 23:15:34,552 INFO sqlalchemy.engine.Engine [raw sql] ()
2024-08-30 23:15:34,552 INFO sqlalchemy.engine.Engine 
CREATE TABLE hero (
        id INTEGER NOT NULL, 
        name VARCHAR NOT NULL, 
        secret_name VARCHAR NOT NULL, 
        age INTEGER, 
        PRIMARY KEY (id)
)


2024-08-30 23:15:34,552 INFO sqlalchemy.engine.Engine [no key 0.00004s] ()
2024-08-30 23:15:34,558 INFO sqlalchemy.engine.Engine COMMIT
"""

def create_heroes():
    """
    Inserting data into the hero table.
    We already created a class Hero that represents the hero table in the database.
    Each instance we create will represent the data in a row in the database.
    Session manages the connection to the database and the transaction.
    """
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
    hero_4 = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32)
    hero_5 = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
    hero_6 = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36)
    hero_7 = Hero(name="Captain North America", secret_name="Esteban Rogelios", age=93)
    hero_8 = Hero(name="Iron Guy", secret_name="Tony Stank", age=110)

    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.add(hero_4)
        session.add(hero_5)
        session.add(hero_6)
        session.add(hero_7)
        session.add(hero_8)

        print("Hero 1:", hero_1)
        print("Hero 2:", hero_2)
        print("Hero 3:", hero_3)

        session.commit()

        print(f"Hero 1 ID: {hero_1.id}, Hero 1 Name: {hero_1.name}, Hero 1 Secret Name: {hero_1.secret_name}, Hero 1 Age: {hero_1.age}")

        # session.refresh(hero_1)
        # session.refresh(hero_2)
        # session.refresh(hero_3)
        """
        refresh could be useful, for example, if you are building a web API to create heroes. And once a hero is created with some data, 
        you return it to the client.
        You wouldn't want to return an object that looks empty because the automatic magic to refresh the data was not triggered.
        In this case, after committing the object to the database with the session, you could refresh it, and then return it to the client. 
        This would ensure that the object has its fresh data.
        """


"""
Selecting data, in sql, is done with the SELECT statement, here are some examples:

SELECT * FROM hero

SELECT id, name
FROM hero

SELECT hero.id, hero.name, hero.secret_name, hero.age
FROM hero

This will be particularly important later when working with multiple tables at the same time that could have the same name for some columns.
For example hero.id and party.id, or hero.name and party.name.
"""

def select_heroes():
    with Session(engine) as session:
        statement = select(Hero)
        results = session.exec(statement)
        print("Selecting all heroes:")
        print(type(results)) # <class 'sqlalchemy.engine.result.ScalarResult'>
        # The results object is an iterable that can be used to go through each one of the rows.
        for hero in results:
            print(hero)

"""
Here it starts to become more evident why we should have a single engine for the whole application, 
but different sessions for each group of operations.
This new session we created uses the same engine, but it's a new and independent session.
The code above creating the models could, for example, live in a function handling web API requests and creating models.
And the second section reading data from the database could be in another function for other requests.
So, both sections could be in different places and would need their own sessions.

But knowing what is each object and what it is all doing, we can simplify it a bit and put it in a more compact form:
def select_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        print(heroes)
"""


"""
filter data from sql, is done with the WHERE clause, after the SELECT statement.
"""

def select_heroes_b():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Deadpond")
        results = session.exec(statement)
        print("Selecting Deadpond:")
        for hero in results:
            print(hero)

"""
The object returned by select(Hero) is a special type of object with some methods.
One of those methods is .where() used to (unsurprisingly) add a WHERE to the SQL statement in that select object.
There are other methods that we will explore later. 
Most of these methods return the same object again after modifying it.
So we could call one after the other:

statement = select(Hero).where(Hero.name == "Deadpond").where(Hero.age == 48)

As an alternative to using multiple .where() we can also pass several expressions to a single .where():
statement = select(Hero).where(Hero.age >= 35, Hero.age < 40)

These last examples use where() with multiple expressions. And then those are combined in the final SQL using AND, 
which means that all of the expressions must be true in a row for it to be included in the results.
But we can also combine expressions using OR. Which means that any (but not necessarily all) of the expressions 
should be true in a row for it to be included.
To do it, you can import or_:
from sqlmodel import Field, Session, SQLModel, create_engine, or_, select
statement = select(Hero).where(or_(Hero.age <= 35, Hero.age > 90))

"""

"""
You already know how to filter rows to select using .where().
And you saw how when executing a select() it normally returns an iterable object.
Or you can call results.all() to get a list of all the rows right away, instead of an iterable.
But in many cases you really just want to read a single row, and having to deal with an iterable or a list is not as convenient.
Let's see the utilities to read a single row:
"""

def select_heroes_c():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.age <= 35)
        results = session.exec(statement)
        hero = results.first() # Will return the first row or None if there are no rows
        # hero = results.one() # Will return the first row or raise an exception if there are no rows or more than one row
        print("Hero with age <= 35:", hero)


"""
Select with limit and offset
We currently have 8 heroes in the database. But we could as well have thousands, so let's limit the results to get only the first 3:
"""

def select_heroes_d():
    with Session(engine) as session:
        statement = select(Hero).limit(3)
        results = session.exec(statement)
        heroes = results.all()
        print("Selecting the first 3 heroes:")
        print(heroes)

"""
Now we can limit the results to get only the first 3.
But imagine we are in a user interface showing the results in batches of 3 heroes at a time. How do we get the next 3?
We can use .offset():
"""

def select_heroes_e():
    with Session(engine) as session:
        statement = select(Hero).limit(3).offset(3)
        results = session.exec(statement)
        heroes = results.all()
        print("Selecting the next 3 heroes:")
        print(heroes)


"""
Update data in SQL is done with the UPDATE statement, here are some examples:
UPDATE hero
SET age=16
WHERE name = "Spider-Boy"
"""


def update_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")  
        results = session.exec(statement)  
        hero = results.one()  
        hero.age = 145  
        session.add(hero) # We can also add multiple objects to the session at once.
        session.commit()  
        """
        The data in the object would be automatically refreshed if we accessed an attribute, like hero.name.
        But in this example we are not accessing any attribute, we will only print the object. 
        And we also want to be explicit, so we will .refresh() the object directly:
        """  
        session.refresh(hero)
        print("Updated hero:", hero)  


"""
delete data in SQL is done with the DELETE statement:
DELETE FROM hero
WHERE name = "Spider-Boy" 
"""
def delete_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")  
        results = session.exec(statement)  
        hero = results.one()  
        print("Hero marked for deletion: ", hero)  
        session.delete(hero)  
        session.commit()  
        print("Deleted hero:", hero)  
        statement = select(Hero).where(Hero.name == "Spider-Boy")  
        results = session.exec(statement)  
        hero = results.first()  
        if hero is None:  
            print("There's no hero named Spider-Boy")  






if __name__ == "__main__":
    """
    The main purpose of the __name__ == "__main__" is to have some code that is executed when your file is called directly,
    but not when it is imported as a module in another file.
    """
    create_db_and_tables()
    create_heroes()
    select_heroes()
    select_heroes_b()
    select_heroes_c()
    select_heroes_d()
    select_heroes_e()
    update_heroes()
    delete_heroes()