# PyFind: Building a Python command-line tool

In this tutorial we will build a command-line tool in Python, and
along the way learn about some modules that make this task easier.


## Chapter 0: Get files from Git

Fork and clone the
[starter repository](https://www.github.com/cruhland/pyfind/).

## Chapter 1: Setting up

We will build a Python version of the Unix `find` command. The `find`
command searches through directory trees for files matching certain
criteria.

To test our program, we'll need a directory tree. Luckily, we can
create one using the `generate_files.py` program available in our
repo:

    $ python generate_files.py

This should create a directory `files` in the project directory that
contains a bunch of randomly named files and directories. We'll run
our PyFind program on this directory and compare its output with the
Unix `find` command.

## Chapter 2: Introducing `find`

The simplest usage of `find` is to give it a single file name as an
argument:

    $ find files

Try this out on the `files` directory that you generated in Chapter
1. Notice that it prints out the name `files`, and then prints out all
of the files and directories inside `files`, and all of the files and
directories inside _those_ directories, etc.

We want our PyFind program to do the same thing. To do this we will
use two modules:

1. `argparse` - For handling command-line arguments.
2. `os` - For using operating system services, such as viewing
   directories.

## Chapter 3: The `'argparse'` module

What are command-line arguments? They are a list of
whitespace-separated strings given after our program name when it is
run. To see this, save the following program in `arguments.py`:

    import sys

    if __name__ == '__main__':
        print sys.argv

Now, run it with some arguments, e.g.:

    $ python arguments.py These are the arguments.

You should see output like:

    ['arguments.py', 'These', 'are', 'the', 'arguments.']

What just happened? In the Python code, we imported the `sys`
module. This module defines a special list `argv` that stores the
arguments to the program. The first element of the list
(`sys.argv[0]`) is the name of the program, in this case
`arguments.py`. The rest of the elements are the space-separated
strings (if any) that we provided on the command line when the program
was run. Try running `arguments.py` with different numbers of
arguments to get more comfortable with the idea.

We have our PyFind program process its arguments using `sys.argv`, but
this would require a lot of work. We would need to validate that all
the arguments were specified correctly, and display error messages to
the user if not. There are a lot of established conventions for
command-line arguments that most programs obey, so we should follow
those conventions to keep our users happy.

The best way to do this is the Python module `argparse`. It lets us
describe what our arguments should look like, and it handles all the
low-level details of parsing and validation. It also displays
nicely-formatted help and error messages.

Now let's use `argparse` to get the directory to search in our PyFind
program. Create a file `find.py` and give it the following contents:

    import argparse

    def main():
        parser = argparse.ArgumentParser(description="Find files with Python")
        parser.add_argument("directory", help="the directory to search")
        args = parser.parse_args()

        print "Searching in %s..." % args.directory

    if __name__ == '__main__':
        main()

Try running your program with different arguments to see what
happens. Some suggestions:

    $ python find.py files
    $ python find.py foo
    $ python find.py foo bar
    $ python find.py
    $ python find.py -h
    $ python find.py --help

Notice how help text and error messages are appropriate for each of
the argument combinations you tried. If we used `sys.argv` we would
have had to handle all of that behavior ourselves.

## Chapter 5: The `'os'` module

Now that we have our directory to search, we need to actually look
through its contents and print them out. Getting information about
files and directories is one of the services provided by the operating
system. We can get access to these services from Python with the `os`
module, and its submodule `os.path`.

There are a large number of functions in these two modules, how do we
know which ones to call? We should first get a rough idea of how we
are going to inspect the directory tree and print it out. Run the Unix
`find` command again as a test; you should see something like the
following:

    $ find files
    files
    files/glove
    files/glove/ship
    files/glove/finger
    files/glove/cart
    files/glove/cart/clock
    files/glove/cart/clock/watch
    files/glove/cart/heart
    files/glove/cart/branch
    files/glove/receipt
    ...

Try to come up with a description of an algorithm in English that will
produce this output. Peek at the answer below when you think you've
figured it out:

<div class="spoilers">
For each of the items in a given directory, do the following:

1. Print out the path of the item
2. If the item is a directory, apply this algorithm to it
</div>

The interesting thing about this algorithm is that it refers to
itself. This hints that it can be implemented using a recursive
function, a function that calls itself. It turns out that a recursive
function is the most straightforward way to process a directory tree,
because the directories are nested inside each other over and over
again. Nested data structures like directory trees are called
_recursive data structures_, and _recursive functions_ are usually the
best way to process them. This is a specific case of a more general
pattern: **the structure of the algorithm should mimic the structure of
the data that it operates on**.

We still need to figure out which functions from the `os` and
`os.path` modules we need to use to implement this algorithm. Think
about each of the steps in the algorithm, and try to identify the
pieces that require data from the filesystem. Check your work against
the answer below before moving on:

<div class="spoilers">
- Get all the items in a given directory
- Find or create the path of a directory item
- Check if a directory item is itself a directory
</div>

The following functions might be useful for providing the missing
pieces for your algorithm. You will not need all of them, but you
should read their documentation to help you decide which to use:

- [`os.chdir(path)`](http://docs.python.org/2/library/os.html#os.chdir)
- [`os.getcwd()`](http://docs.python.org/2/library/os.html#os.getcwd)
- [`os.listdir(path)`](http://docs.python.org/2/library/os.html#os.listdir)
- [`os.path.abspath(path)`](http://docs.python.org/2/library/os.path.html#os.path.abspath)
- [`os.path.basename(path)`](http://docs.python.org/2/library/os.path.html#os.path.basename)
- [`os.path.dirname(path)`](http://docs.python.org/2/library/os.path.html#os.path.dirname)
- [`os.path.isfile(path)`](http://docs.python.org/2/library/os.path.html#os.path.isfile)
- [`os.path.isdir(path)`](http://docs.python.org/2/library/os.path.html#os.path.isdir)
- [`os.path.join(path1[, path2[, ...]])`](http://docs.python.org/2/library/os.path.html#os.path.join)
- [`os.path.normpath(path)`](http://docs.python.org/2/library/os.path.html#os.path.normpath)
- [`os.path.relpath(path[, start])`](http://docs.python.org/2/library/os.path.html#os.path.relpath)
- [`os.path.split(path)`](http://docs.python.org/2/library/os.path.html#os.path.split)

Now we have everything we need to write our recursive
directory-printing function in `find.py`. It should take the name of
the directory to print as an argument. Call it on the directory name
that you obtained using `argparse` in the previous chapter. To test
your code, you can run the following commands:

    $ find files > find.txt
    $ python find.py files > pyfind.txt
    $ diff find.txt pyfind.txt

These commands save the output of the Unix `find` command and your
PyFind implementation to some text files, and then compare them. The
`diff` command will show which lines of the output are different,
which you can use to debug your code. If `diff` gives no output, then
your code works! If you get stuck, peek at the reference
implementation below:

<div class="spoilers">

    def visit(file_name, base_path=""):
        full_path = os.path.join(base_path, file_name)
        print full_path
        if os.path.isdir(full_path):
            for name in os.listdir(full_path):
                visit(name, full_path)
</div>

## Chapter 6: Actually finding things with `find`

Now that our PyFind program is able to look at all the files and
directories in a directory tree, we can add the ability to print out
only the paths that meet criteria specified on the command line. One
of the simplest criteria is _type_, i.e., does the path represent a
file or a directory?

We can use the functions `os.path.isfile(path)` and
`os.path.isdir(path)` to detect whether a path is a file or a
directory. It's a little less clear how we might modify our recursive
directory tree function to use these functions to only print files or
directories. One approach would be to create two new recursive
functions:

    def visit_files(file_name, base_path=""):
        full_path = os.path.join(base_path, file_name)
        if os.path.isfile(full_path):
            print full_path
        if os.path.isdir(full_path):
            for name in os.listdir(full_path):
                visit_files(name, full_path)

    def visit_directories(file_name, base_path=""):
        full_path = os.path.join(base_path, file_name)
        if os.path.isdir(full_path):
            print full_path
        if os.path.isdir(full_path):
            for name in os.listdir(full_path):
                visit_directories(name, full_path)

This is not a maintainable solution. Most of the code in these
functions is the same, so if we ever want to modify the way in which
we visit the directories, we will have to remember to change it in
both functions. What if we could combine these two functions into a
single one that does the same thing, if given the right arguments? It
turns out that we can, although it might be difficult to see at first.

The process of combining similar pieces of code together into a single
more general piece of code is called _abstraction_. Usually, creating
an abstraction involves these steps:

1. Identify the common parts between the pieces of code being combined
2. The remaining parts are what is different between the pieces of
code
3. Replace each different part with a variable name
4. Wrap the code in a function that has the variable as a parameter
   (or if the pieces of code are already functions, just add a new
   parameter to them)

Try to follow these steps and combine the `visit_files` and
`visit_directories` functions into a single `visit_matching`
function. See below for a hint and the solution.

Hint:
<div class="spoilers">
The `visit_matching` function will need to take a function as an
argument.
</div>

Solution:
<div class="spoilers">

    def visit_matching(file_name, matches, base_path=""):
        full_path = os.path.join(base_path, file_name)
        if matches(full_path):
            print full_path
        if os.path.isdir(full_path):
            for name in os.listdir(full_path):
                visit_matching(name, matches, full_path)
</div>

With our new abstraction, we can search for files using

    visit_matching('files', os.path.isfile)

and search for directories using

    visit_matching('files', os.path.isdir)

However, our original `visit` function is almost identical to
`visit_matching`. Try to figure out what matching function we should
pass to `visit_matching` to make it do the same thing as
`visit`. Answer below.

<div class="spoilers">

    visit_matching('files', lambda path: True)
</div>

Now we can replace the call to our original recursive directory
function in `find.py` with a call to `visit_matching`. However, we
still need give PyFind users the ability to filter by file type from
the command line. This means we need to improve our `argparse` code.

Here's how to get the Unix `find` command to list files only and
directories only, respectively:

    $ find files -type f
    $ find files -type d

This is an example of an _optional argument_, so called because you do
not need to specify it. The optional argument has its own argument
that indicates which type we want to find. We can add the following
line to our `argparse` code in `find.py` to get this working for
PyFind:

    parser.add_argument("-type", help="filter by type", choices=['d', 'f'])

If you parse the arguments as `args = parser.parse_args()`, then the
argument to the `-type` option will be available as
`args.type`. Modify your code so that `-type f` and `-type d` behave
in the same way as they do for the Unix `find` command. Test your code
using `diff` as before, and try passing invalid arguments to see what
error messages you get.

After this chapter, here's an example of what your `find.py` file
should contain:

<div class="spoilers">

    import argparse
    import os

    def main():
        parser = argparse.ArgumentParser(description="Find files")
        parser.add_argument("directory", help="the directory to search")
        parser.add_argument("-type", help="filter by type", choices=['d', 'f'])
        args = parser.parse_args()

        matching = lambda path: True
        if args.type == 'f':
            matching = os.path.isfile
        elif args.type == 'd':
            matching = os.path.isdir

        visit_matching(args.directory, matching)

    def visit_matching(file_name, matches, base_path=""):
        full_path = os.path.join(base_path, file_name)
        if matches(full_path):
            print full_path
        if os.path.isdir(full_path):
            for name in os.listdir(full_path):
                visit_matching(name, matches, full_path)

    if __name__ == '__main__':
        main()
</div>

## Chapter 7: Filtering with the `datetime` module

The Unix `find` command also allows searching files by their
modification time. Unfortunately it's not very flexible: you can only
specify time in increments of minutes or days. We can do better using
the Python `datetime` module.

Let's start by implementing a new command-line argument,
`-m_before DATETIME`. This will cause PyFind to only return files or
directories that were modified before the given date and time. Let's
add the argument to our parser:

    parser.add_argument("-m_before", help="filter before the given date and time")

We then need to handle that argument if it is provided by the user. We
can just add another branch to our `if` statement:

    elif args.m_before:
        matching = modified_before(args.m_before)

With the above code, we first check if the `m_before` argument was
provided by the user. If it was, we call the function
`modified_before` (which we haven't written yet) with the value of the
`m_before` argument (which is hopefully a string representing a date
and time). The `modified_before` function then _returns another
function_ which becomes our `matching` function.

Time to write our `modified_before` function. This takes a date and
time formatted as a string, and returns a matching function that when
given a filesystem path, returns `True` if the item at that path was
modified before the given date and time, and `False` otherwise. A
high-level view of the code is the following:

    def modified_before(datetime_str):
        # Convert datetime_str to a reference datetime object

        def matching(path):
            # Get the modification timestamp of the item at path
            # Convert the modification timestamp to datetime
            # Compare the modification datetime to the reference
            # If the modification timestamp is earlier, return True
            # Otherwise, return False

        return matching

To fill in the comments with Python code, you will probably find the
following methods useful, be sure to read their documentation:

- `datetime.datetime.strptime(date_string, format)`
- `datetime.datetime.fromtimestamp(timestamp)`
- The `<` operation on `datetime` objects
- `os.path.getmtime(path)`

Once you think you've implemented `modified_before`, you should test
it out on the terminal with the `files` directory to see if it
works. The files will have random modification times, just run `ls -l`
to see them. Then run PyFind using the new `-m_before` argument with
the date and time you want to check for. Reveal the code below to
verify your implementation:

<div class="spoilers">

    def modified_before(datetime_str):
        reference_datetime = datetime.datetime.strptime(datetime_str, '%b %d %Y %I:%M:%S %p')

        def matching(path):
            modification_timestamp = os.path.getmtime(path)
            modification_datetime = datetime.datetime.fromtimestamp(modification_timestamp)
            return modification_datetime < reference_datetime

        return matching
</div>

Now that `-m_before` is working, implement the opposite argument,
`-m_after`.

## Chapter 8: More `datetime` filtering

Sometimes we want to find files modified in a particular month, but
not necessarily in the same year. Or maybe we know the hour at which
we modified a file, but don't remember the day. In this chapter we'll
implement this kind filtering in PyFind.

The command-line argument format we'll use looks like the following
example:

    python find.py files -m_in month=07,hour=20

This gives all files modified in hour 20 (between 8 pm and 9 pm)
of any day in July. Notice we have a new command-line switch, `-m_in`,
and a new format for specifying date and time components as key-value
pairs.

Your goal for this chapter is to add this new feature to PyFind on
your own, using what we've covered so far. One hint is that you will
find the [`datetime.datetime`
constructor](http://docs.python.org/2/library/datetime.html#datetime.datetime)
useful. Peek at the hints below if you get stuck:

Parser setup:
<div class="spoilers">

    parser.add_argument("-m_in", help="select files with the given "
                                 "values in their modification times")
</div>

Matching function selection:
<div class="spoilers">

    elif args.m_in:
        matching = modified_in(args.m_in)
</div>

Matching function definition:
<div class="spoilers">

    def modified_in(datetime_arg_str):
        datetime_values = {}
        for arg in datetime_arg_str.split(','):
            attr, value_str = arg.split('=')
            datetime_values[attr] = int(value_str)

        def matching(path):
            modification_timestamp = os.path.getmtime(path)
            modification_datetime = \
                datetime.datetime.fromtimestamp(modification_timestamp)
            for attr, value in datetime_values.items():
                if getattr(modification_datetime, attr) != value:
                    return False
            return True
        return matching
</div>

## Chapter 9: Conclusion

There are many more features that can be added to PyFind, if you're
looking for more challenges. Some ideas:

- Use the `datetime.timedelta` class with `-m_before` and `-m_after`
  to allow relative time boundaries. For example, `-m_after days=-3`
  would find all files modified later than three days ago.
- Combine filters together using `-and` and `-or` arguments, for
  example `-type d -and -m_in year=2012` to find all directories
  modified in 2012.
- Introduce `-size_below` and `-size_above` arguments for filtering by
  file size. Use the [`os.path.getsize(path)`
  function](http://docs.python.org/2/library/os.path.html#os.path.getsize)
  to get the size of a file.
- Introduce the `-regex` argument for filtering file names by regex.
- You can also run `man find` and read the documentation for the Unix
  `find` command to get more ideas.
