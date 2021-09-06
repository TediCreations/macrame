Shell completion
================

Usage
************

The supported shells are bash and zsh.

To enable autocompletion you need to configure it in your environment.

Bash
************

Place the following in your ~/.bashrc:

.. code-block:: console

   source <(macrame --print_shell_completion_script=bash)

Zsh
************

Place the following in your ~/.zshrc:

.. code-block:: console

   source <(macrame --print_shell_completion_script=zsh)
