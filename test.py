


async def main():
    doc_db_lib = __import__('doc-db-lib')
    DB = doc_db_lib.DB

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

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())