[Oracc] » [Help] » [Lemmatising] » Rebuild errors

# Rebuild errors

This page gives some help with fixing rebuild error messages that arise through lemmatisation or glossary management problems.

## F2 errors

An L2 feature common to several subsystems is the 'form' or 'signature'. This is the basic component of interlinear lemmatization, for example. All of the L2 programs which are written in C use the same parser for these forms, so the messages the parser produces may occur in a variety of contexts. When the messages are produced as part of lemma-checking, they are labeled as '(f2)'.

## F2 Diagnostics

### xxx: parse error at 'x'

This is an error which is generated when the F2 parser is expecting to find any of the delimiter characters that separate parts of the form. The first thing it tells you is the string it is looking at when it finds the parse error, and at the end of the line it tells you which character in the string was the one that confused it.

Here's a real-life example:

    sb-I.atf:575: (f2) stack: parse error at 's'

Looking at line 575 of the offending file we see:

    147\. zar
    #lem: zar\[sheaf (of barley); stack of sheaves\]N

So, the error is detected at the 's' of 'stacks'. In L2 semi-colons are not allowed within a sense: the normal meaning of such a semi-colon in a glossary or dictionary is that multiple senses are involved, and in L2 the correct way to handle that is to define multiple `@sense` lines in the glossary entry, and to separate the GW and the SENSE with `//` in the lemmatization:

    147\. zar
    #lem: zar\[sheaf (of barley)//stack of sheaves\]N

## LEM errors

This is a list of (lem) error messages that might seem rather mysterious at first, with hints on what they mean and how to fix them. Do get in touch if there are others you would like to be added.

``(lem) no FORM `EN.NAM' and no matches for mīnûm[what?]QP in glossary dccmt:akk-x-oldbab``

The usual cause of this sort of error messages is a surplus `$` in an auto-lemmatised form, i.e., `mīnûm[what?]QP$` instead of correct `mīnûm[what?]QP`. Just delete the `$`.

``(lem) no FORM `EN.NAM' and no matches for mīnûm[what?]QP in glossary cdli:akk-x-oldbab``

Here the lemmatiser is looking for a form in a putative `cdli` OB glossary, not the project's own one. This is because the protocol lines are in the wrong order. In Oracc 2 the `#project:` protocol line _must_ come before the `#atf:` protocol lines. Moving the `#project:` protocol line to before the `#atf:` protocol lines will fix this error.

[Oracc]: ../../../index.html
[Help]: ../../../help/index.html "Help page overview"
[Lemmatising]: ../../../help/lemmatising/index.html "Lemmatising ATF Files"
