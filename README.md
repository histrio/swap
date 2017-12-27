# Swap

Test assignment for backend developer

API
---

- **[<code>GET</code> item](#api)**

  Get list of items available for swapping 
    - `owner` (optional) get items for owner

- **[<code>POST</code> item](#api)**

  Publish an item you wish to swap 

- **[<code>POST</code> swapping](#api)**

  Swap one of your items to someone item. 


Testing
-------

To test this, one should be using an sh compatible shell that support
`$(some command)` and `export ENV_VAR=` syntax.

Finally, tests are run using `make test`.


Reproducible Developing Environment
-----------------------------------

I had a lot of pain via setting up a developer environment for GAE. So, if it's not only me - use this:

vagrant up --provider=docker
vagrant ssh
cd /vagrant
make test
make run
