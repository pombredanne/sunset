Have you ever added a hack that you told yourself you would remember to get rid of later on?
Sunset is a tool to help you remember -- all you have to do is wrap your code with special
comments and have Sunset run automatically as part of your automated code quality processes :)

Currently, Sunset is in pre-release development and only supports scanning Python source code.

## Usage

To mark a single line of code to sunset, be sure to end the comment with `<<`:

```python
ENABLE_HACK = True      # >>SUNSET 2015-01-01<<
```

To mark a block of code, use `>>SUNSET` and `<<SUNSET` style comments:

```python
# >>SUNSET 2015-01-01
if ENABLE_HACK:
  # dastardly deeds not shown to protect the innocent
  pass
# <<SUNSET
```

## Scanner examples

Scan an individual filefiles in directories

```bash
$ sunset scan file1.py
ALERT    file1.py:100-123   expired 3 days ago
WARNING  file1.py:128       expires in 5 days
```

Scan a directory

```bash
$ sunset scan .
ALERT    file1.py:100-123   expired 3 days ago
WARNING  file2.py:10-12     expires in 3 days
WARNING  file1.py:128       expires in 5 days
```

Scan a directory recursively

```bash
$ sunset scan -R .
ALERT    file1.py:100-123   expired 3 days ago
ALERT    lib/file1.py:11    expired 1 day ago
WARNING  file2.py:10-12     expires in 3 days
WARNING  file1.py:128       expires in 5 days
```

Show only alerts

```bash
$ sunset scan -R --only=ALERT .
ALERT    file1.py:100-123   expired 3 days ago
```

Show only items within 3 days from now

```bash
$ sunset scan -R --within=3d .
ALERT    file1.py:100-123   expired 3 days ago
WARNING  file2.py:10-12     expires in 3 days
```

Output as CSV

```bash
$ sunset scan --output=csv file1.py
ALERT,file1.py,100-123,-3
WARNING,file1.py,128,5
```