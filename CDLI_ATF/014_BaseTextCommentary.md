[Oracc] » [Help] » [Editing in ATF] » Commentary

# Base Text and Commentary

This page describes the ATF mechanism for linking a scholarly commentary to its base text.

## Commentary Protocol

ATF commentaries do not need a special protocol: four field designations are always available for dividing commentary lines into different parts:

`!qt`

to introduce a quote from the base text;

`!bs`

to introduce the base word(s) commented upon;

`!cm`

to introduce a commentary on the base word(s);

`!zz`

to mark text as not belonging to a quote, base of comment.

each of these elements must be surrounded by white space: instead of `[!cm` write `!cm [`.

18 Dec 2019 osc at oracc dot org

Niek Veldhuis

Niek Veldhuis, 'Base Text and Commentary', _Oracc: The Open Richly Annotated Cuneiform Corpus_, Oracc, 2019 \[http://oracc.museum.upenn.edu/doc/help/editinginatf/commentary/\]

[Oracc]: ../../../index.html
[Help]: ../../../help/index.html "Help page overview"
[Editing in ATF]: ../../../help/editinginatf/index.html "Working with ATF to edit texts"
