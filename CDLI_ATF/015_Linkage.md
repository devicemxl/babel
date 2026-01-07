[Oracc] » [Help] » [Editing in ATF] » Linkage

# ATF Linkage

This document describes the ATF mechanisms for intertext linking. The original version of this document was written by Madeleine Fitzgerald and Steve Tinney.

[Background] | [Operators] | [Targets and Link Definitions] | [Labels] | [Syntax] | [Implementation] | [Examples]

## Background

The ATF format supports inline notations of three relationships between lines in different texts:

-   parallels, in which a line or lines in one text are similar to lines in another text
-   sources, or lines which are being included in a composite text but originate in other texts
-   contributors, or lines which are being entered in a transliteration and at the same time are relevant to the reconstruction of a composite text

## Operators

Linking composite text lines to lines in individual texts, lines in exemplars to lines in composite texts, and matching lines in two or more individual exemplars or composite texts are indicated with the following notation at the beginning of the next line after the line of transliterated text to be linked.

<<

line comes from tablet instance (source)

\>>

line goes to composite text (contributor)

||

before reference to line in parallel composite or tablet (parallel)

The source ('comes from') and contributor ('goes to') facilities are intended to allow creation of composite texts in the absence of a complete set of transliterated sources and, conversely, to allow the transliteration of individual sources by reference to a composite text which may not yet include the original sources.

The parallel link facility is especially useful for editing tablets such as those containing liturgical texts and incantations where creating a composite text may be practically futile as well as methodologically dubious.

## Targets and Link Definitions

A `TARGET` is a reference to another text related to the one at hand. Every linked text must be defined and given a `TARGET` identifier in the file in which it is to be used before the first use; we recommend grouping all the definitions together just before the `&`\-line (text ID/name line).

A linked text definition takes the form:
  
  #link: def linktext <TARGET> = <ID> = <NAME>

For example:
  
  #link: def A =  P227635 = CBS 10792 (OB Syllabary B)

The variable elements of this definition are:

TARGET

the name that is used in the link specifiers; this is normally an uppercase letter, e.g., `A`, but the only actual restriction on the spelling of a target is that it may not contain any whitespace.

ID

the ID as assigned by the CDLI project; for transliterated objects this begins with a 'P', e.g., P123456. Other text types have similar identifiers with different initial letters.

NAME

the human-readable name assigned by the CDLI project; in the XML format this is the value of the 'N' attribute.

The ID and NAME values of texts can be obtained from the CDLI website; for texts which have not yet been assigned ID's, use an initial 'X' followed by digits as an interim measure and e-mail the CDLI staff to request IDs (cdli@ucla.edu).

## Labels

The target is followed by a label that gives the location of the related text in the target document. Labels are constructed according to the following abbreviations (which are designed to be easy to type while still allowing programmatic reconstruction of the location of the reference in the XML dataset):

-   o = obverse
-   r = reverse
-   t = top edge
-   b = bottom edge
-   l = left edge
-   r = right edge
-   e = edge
-   <surface> = other surface, e.g., `shoulder`
-   face a..z = prism face a to z
-   seal n = seal n (n = the number of the seal in the transliteration)
-   <roman> = column number in lowercase roman numerals
-   <line number>

Spaces are required between elements of a label, for example, o i 2 = obverse, column 1, line 2.

Two labels, a 'from' label and a 'to' label, are used when there is a need to indicate a range of text beyond a single line in the target document. A range requires a hypehn character between the two labels.

## Syntax

The syntax of these constructs is either:
    
    <OPERATOR> <TARGET> <LABEL>
    
    or:
    
    <OPERATOR> <TARGET> <FROM\_LABEL> - <TO\_LABEL>

## Implementation Notes

A separate program manages the links in such a way that it is unnecessary to group together all of the links to a specific parallel. In other words, given three texts which contain the same parallel, let's say Liturgy 1, 2 and 3, one can encode the relationship as follows:

    @transliteration
    #link: def A = P222222 = Liturgy 2
    &P111111 = Liturgy 1
    1. a-u-a
    || A 1
    
    &P222222 = Liturgy 2
    1. a-u2-a
    
    #link: def A = P222222 = Liturgy 2
    &P333333 = Liturgy 3
    1. a-u3-a
    || A 1

The link manager will resolve the links in Liturgy 1 and Liturgy 3 and construct a link-ring in which all three parallels refer mutually to each other. The search engine will automatically display all parallels whenever a match is found in any of the lines.

## Examples

**(a) Source (line in composite 'comes from' exemplar):**

    _File 1:_
    
    &P121323 = OB Lu excerpt N 4304
    1. lu2
    
    _File 2:_
    
    @composite
    #link: def A = P123123 = OB Lu excerpt N 4304
    &Q123238 = A = OB Lu A
    1. lu2
    << A 1
    
**(b) Contributor (line in exemplar 'goes to' composite)**
    
    _File 1:_
    
    @composite
    &Q123238 = OB Lu A
    1. lu2
    
    _File 2:_
    
    #link: def A = Q128238 = OB Lu A
    &P121323 = OB Lu excerpt N 4304
    1. A
    >>A 1

**(c) Parallel**
    
    _File 1:_
    
    &P123456 = Kusu Incantation version 1
    @reverse
    @column 2
    1. \[am husz gal\] du7-du7 gi-\[izi-la2\] 
    
    _File 2:_
    
    #link: def D = P123456 = Kusu Incantation version 1
    &P123457 = Kusu Incantation version 2
    1. am husz# gal du7-du7 gi-\[izi-la2\]
    || D r ii 1

The above example shows two exemplars of a text. The second transliteration contains a definition of the first text as "D" and indicates that its first line is paralleled (||) in the first line of the second column of the reverse of the first text. Parallels may be drawn between composite texts, transliterations or a combination of the two.

18 Dec 2019 osc at oracc dot org

Steve Tinney

Steve Tinney, 'ATF Linkage', _Oracc: The Open Richly Annotated Cuneiform Corpus_, Oracc, 2019 \[http://oracc.museum.upenn.edu/doc/help/editinginatf/linkage/\]
