client module
=============
Messaging client application. Supports
sending messages to users who are online

Supports command line arguments:

``python client.py {server name} {port} -n or --name {user name} -p or -password {password}``


Example:

*Run application with user test1 and password 123*

* ``python client.py ip_address some_port -n test1 -p 123``

database.py
~~~~~~~~~~~~~~

.. autoclass:: client_file.client_database.ClientDatabase
	:members:

transport.py
~~~~~~~~~~~~~~

.. autoclass:: client_file.transp.ClientTransport
	:members:

main_window.py
~~~~~~~~~~~~~~

.. autoclass:: client_file.main_window.ClientMainWindow
	:members:

start_dialog.py
~~~~~~~~~~~~~~~

.. autoclass:: client_file.user_name_dialog.UserNameDialog
	:members:


add_contact.py
~~~~~~~~~~~~~~

.. autoclass:: client_file.add_contact.AddContactDialog
	:members:


del_contact.py
~~~~~~~~~~~~~~

.. autoclass:: client_file.del_contact.DelContactDialog
	:members: