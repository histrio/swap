# Swap

Test assignment for backend developer

API
---

- **[<code>GET</code> item]()**
- **[<code>POST</code> item]()**
- **[<code>POST</code> swapping]()**


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
