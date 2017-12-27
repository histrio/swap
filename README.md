# Swap

Test assignment for backend developer

API
---

There is a simple API available. First of all, httplib has been wrapped in
`http_request` function to ease of use.

`gen_ok` and `gen_err` functions have been generated to ease the creation
of flask responses

`Return` exception can be raised if one wants to answer something to the
request


Testing
-------

To test this, one should be using an sh compatible shell that support
`$(some command)` and `export ENV_VAR=` syntax.

Finally, tests are run using `tox`.


Reproducable Developing Environment
-----------------------------------

I had a lot of pain via setting up a developer environment for GAE. So, if it's not only me - use this:

vagrant up --provider=docker
vagrant ssh
cd /vagrant
make test
make run
