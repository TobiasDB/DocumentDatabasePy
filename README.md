# doc-database-lib

An Async Document Database Libary with ODM

## Installation

use the package manager pip to install doc-database-lib from the index xxxx

```bash
pip install doc-database-lib
```

## Basic Usage

```python
from doc_database_lib import DB

# Create a connection
db = DB('mongodb://localhost:8081', 'userdb')

# Add a document to database
user = {'username': 'JohnSmith', 'password': 'supersecret'}
uid = await db.put_one('users', user)

# Update a document in the database
success = await db.update_one('users', uid, {'email': 'JohnSmith@email.com'})

# Get a document from the database
user = await db.get_one('users', uid)

# Remove a document from the database
success = await db.delete_one('users', uid)
```

## Basic ODM Usage

```python
from doc_database_lib import DB
from doc_database_lib.odm import Document

class User(Document):
    username: str
    password: str

# Create a connection
db = DB('mongodb://localhost:8081', 'userdb')

# Use the model in the ODM
User.use(db, 'users')

# Get all users in the database
users = await User.gets()

# Add a document to database
user = User(**{'username': 'JohnSmith', 'password': 'supersecret'})

# Add model instance to the database
uid = await user.put()

# Update a model instance in the database
user.email = 'JohnSmith@email.com'
success  = await user.update()

# Update a model instance from the database
await user.get()

# Remove a document from the database
success = await user.delete()
```

