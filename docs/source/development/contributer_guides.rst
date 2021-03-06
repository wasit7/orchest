Contributer guides
==================

Contributor License Agreement
-----------------------------

Our CLA is an exact copy of the Apache CLA (apart from the names), which the cla-assistant
will automatically prompt you to sign upon a pull request. Signing is done electronically.

The CLA ensures that Orchest has clear ownership specification for all contributions, which in
turns lets us guarantee to users that we have no "stray" intellectual property or
differently-licensed material.


Development environment
-----------------------
To start hacking on Orchest you simply have to clone the repo from GitHub and start Orchest in
``dev`` mode.

.. code-block:: bash

   git clone https://github.com/orchest/orchest.git
   cd orchest

   # Before Orchest can be run in "dev" mode the front-end code has to
   # be compiled.
   scripts/dev_compile_frontend.sh

   # Start Orchest in dev mode which mounts the repo code to the correct
   # paths in the Docker containers to not require any rebuilds. In 
   # addition, servers build on Flask are started in development mode.
   ./orchest.sh start dev

``dev`` mode mounts the repository code from the filesystem (and thus adhering to branches) to the
appropriate paths in the Docker containers. This allows for active code changes being reflected
inside the application. In ``dev`` mode the Flask applications are run in development mode. The
following services support ``dev`` mode (others would have to be rebuild to show code changes):
``orchest-webserver``, ``auth-server``, ``file-manager`` and ``orchest-api``.

Additional useful scripts are included in the root-level ``scripts/`` directory, such as
``build_container.sh`` and ``run_tests.sh``.

Feel free to pick up any of the issues on `GitHub <https://github.com/orchest/orchest/issues>`_ or
create a custom pull request 💪.
