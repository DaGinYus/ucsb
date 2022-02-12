#!/bin/sh

# TKC!
# wget, grep, and sed
# Matthew Wong
# Phys 129L Hw6 Pb 1
# 2022-02-17

WEBADDRESS="http://web.physics.ucsb.edu/~phys129/lipman"

# ===EXPLANATION===
#
# Use `-O -` to specify stdout instead of write to disk.
# The -q option suppresses wget command output.
#
# The line in the .html file looks like:
#   Latest update: <span class="greenss">Tuesday, November&nbsp;30</span></p>
#
# `sed -e` means execute the expression
# In the first expression, we have `s/regexp/replacement/`
# The regexp `^` is the beginning of the line,
# `.` matches any character that is not a line break,
# `*` means match any amount of the preceding token, which is `.`
# (basically match all characters)
# Then we match `>`, which corresponds to the closing caret of the HTML tag.
# This matched expression is replaced with an empty string, in the `//`
# The HTML contains a `&nbsp;` (non-breaking space), so replace that with an actual space.
# Finally, we match everything in the closing HTML tag up until the end of the line `$`.
# Like the opening tag, this gets replaced with nothing.

echo "The web page announcements were last updated on:"
wget -qO - $WEBADDRESS | grep "Latest update" | sed -e 's/^.*">//' -e 's/&nbsp;/ /' -e 's/<.*$//'
