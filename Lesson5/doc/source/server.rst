Server module
=============

Server application for messaging.

Provides the following functions:

1. Registering and deleting users.
2. User authorization.
3. Passing messages between users.
4. Storage of login history and user statistics.

server.py
~~~~~~~~~~~~~~
.. automodule:: server
   :members:
   :undoc-members:
   :show-inheritance:

core.py
~~~~~~~~~~~~~~

.. autoclass:: server_file.core.MessageProcessor
	:members:

server_database.py
~~~~~~~~~~~~~~~~~~~

.. autoclass:: server_file.server_database.DataBase
	:members: