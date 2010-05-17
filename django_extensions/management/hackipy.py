#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,__builtin__

def my_runsource(self, source, filename='<input>', symbol='single'):
    """Compile and run some source in the interpreter.
    A heck by Amit Aronovitch for ipython to better support unicode
    Arguments are as for compile_command().

    One several things can happen:

    1) The input is incorrect; compile_command() raised an
    exception (SyntaxError or OverflowError).  A syntax traceback
    will be printed by calling the showsyntaxerror() method.

    2) The input is incomplete, and more input is required;
    compile_command() returned None.  Nothing happens.

    3) The input is complete; compile_command() returned a code
    object.  The code is executed by calling self.runcode() (which
    also handles run-time exceptions, except for SystemExit).

    The return value is:

      - True in case 2

      - False in the other cases, unless an exception is raised, where
      None is returned instead.  This can be used by external callers to
      know whether to continue feeding input or not.

    The return value can be used to decide whether to use sys.ps1 or
    sys.ps2 to prompt the next line."""

    # if the source code has leading blanks, add 'if 1:\n' to it
    # this allows execution of indented pasted code. It is tempting
    # to add '\n' at the end of source to run commands like ' a=1'
    # directly, but this fails for more complicated scenarios
    
    #AA: following line commented out to resolve encoding issue (github:25)
    #source=source.encode(self.stdin_encoding)
    if source[:1] in [' ', '\t']:
        source = 'if 1:\n%s' % source
    
    try:
        code = self.compile(source,filename,symbol)
    except (OverflowError, SyntaxError, ValueError, TypeError, MemoryError):
        # Case 1
        self.showsyntaxerror(filename)
        return None

    if code is None:
        # Case 2
        return True

    # Case 3
    # We store the code object so that threaded shells and
    # custom exception handlers can access all this info if needed.
    # The source corresponding to this can be obtained from the
    # buffer attribute as '\n'.join(self.buffer).
    self.code_to_run = code
    # now actually execute the code object
    if self.runcode(code) == 0:
        return False
    else:
        return None

