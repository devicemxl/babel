[Oracc] » [Help] » [Lemmatising] » Syntax

# L2: Signature/Lemmatization Syntax

This document describes extant and planned elements of the syntax of signatures and the lemmatization specifications that use them. There is also an [introductory page about signatures].

The forms of signatures and inline lemmatizations proper are identical as far as core and adjunct fields are concerned. Signatures are simply lemmatizations prefixed with a project and a lang/form pair.

## Prefix Fields

| Key Char | Field |
| --- | --- |
| `@...` | Project name |
| `%...` |     |
| :...= | Form (Unicode text, no 'equals' signs) |

@dcclt%sux-emesal:ma=

## Core Fields

| Key Char | Abbrev | Full Name |
| --- | --- | --- |
|     | CF  | Citation Form |
| `[...]` | GW  | Guide Word |
| `//` | SENSE | Sense |
|     | POS | Part of Speech |
| `$` | NORM | Normalization |

## Adjunct Fields

| Key Char | Abbrev | Full Name |
| --- | --- | --- |
| `'` | EPOS | Effective Part of Speech |
| `/` | BASE | Word Base |
| `+` | CONT | Base Continuation |
| `*` | STEM | Word Stem |
| `#` | M1  | Morphology 1 |
| `##` | M2  | Morphology 2 |

Note: augmentation and disambiguation do not need to be handled explicitly in signatures because they are rewritten as part of the FORM or M1 fields.

## Para-lemma Features

### Properties

Properties can also be specified on lemmata using the '$'-notation. The full form is:

    $PROPERTY=VALUE

No spaces are allowed. If 'VALUE' is unique within the values given in the project's 00lib/properties.xml then the PROPERTY component is optional giving the short form:

    $VALUE

### Anchors

Any lemma can be labeled with an anchor which can be used as the target of a reference. This can be used to handle anaphora:

    #lem: ...  Anu-uballit\[1\]PN @1 ...
    
    #lem: abišu\[father\] =1

A simple label consists of the at-sign (`@`) followed by digits, but arbitrary labels may be given subject to the constraint that no label may contain spaces:

    #lem: ...  Anu-uballit\[1\]PN @mystery-man ...
    
    #lem: abišu\[father\] =mystery-man

### Syntax Hinting

### Top vs Internal

Top-level boundaries may be given to mark discourse (`:`), sentence (`.`), clause (`;`) and phrase (`,`) boundaries.

Bracketing is implicit between top-level constituents:

    a b ; c , d e ; f g . h i : j k

Is identical to:

    ( ( (a b) ; (c) , (d e) ; (f g) ) . ( h i ) ) : ( j k )

To annotate internal phrase structure one can add parentheses explicitly:

    a b ; c , (d e , f g) , h i .

Here, `(d e , f g)` is first parsed as a top-level constituent, then recursively parsed.

### Labeling Units

A unit can always be labelled by giving the label after its opening parenthesis. For units with explicit dividers, the label may be given after the divider:

    (S a b ; (PRP c d)) :DATE e f

### Conjunction and Modification

    `+&`, `+>`, `+<` imply a phrase boundary, i.e., they are equivalent to `+,+&` etc.
    
    kud\[fish\]; +& muszen\[bird\]
    
    kud\[fish\]; tur\[small\]; +& (muszen\[bird\]; gal\[big\])

### Linksets

Linksets allow arbitrary collections of words to be collected as discontinuous units. These are generally identified by the various analyzer programs, but we define a mechanism for specifying them manually to supplement or override the programs.

Linksets can be defined and populated using two notations:

     ##TYPE/INDEX\[/MEMBER\]
    
     #INDEX/\[MEMBER\]
    
    Where INDEX may be a simple integer or a more complex symbol:
    
     ##date/from ... #from ... #from
    
     ##date/to ... #to ... #to

`[MEMBER]` in each case enables the lemma(ta) to be associated with an element in the linkset structure. Suppose any date should consist of a year, month and day element. A date linkset might then look something like this:

     #lem: mu\[year\] ##date/doc/year; Šulgir\[1\]RN #doc/year; lugal\[king\] #doc/year
    
     #lem: iti\[month\]; Ubigu\[1\]MN #doc/month; ud\[day\]; n #doc/day

Note that many dates can be parsed successfully by machine, but this mechanism allows manual tagging of dates that aren't handled by the machine.

18 Dec 2019 osc at oracc dot org

Steve Tinney

Steve Tinney, 'L2: Signature/Lemmatization Syntax', _Oracc: The Open Richly Annotated Cuneiform Corpus_, Oracc, 2019 \[http://oracc.museum.upenn.edu/doc/help/lemmatising/syntax/\]

[Oracc]: ../../../index.html
[Help]: ../../../help/index.html "Help page overview"
[Lemmatising]: ../../../help/lemmatising/index.html "Lemmatising ATF Files"
[introductory page about signatures]: ../../../help/lemmatising/signatures/index.html "Signatures"
