[Oracc][] » [Help][] » [Editing in ATF][] » Scores

# Scores

This document describes how to create scores using Oracc.

## Overview

Oracc divides scores into two types and two modes. The two types are the matrix and the synoptic; the two modes are parsed and unparsed. To specify that an ATF transliteration is some kind of score, you give one of the following @-protocols immediately after the &-line:

@score matrix parsed
@score matrix unparsed
@score synoptic parsed
@score synoptic unparsed

Both types of scores use a composite line--the reconstructed line which does not belong to a physical source--and exemplar lines, which are the individual manuscript witnesses. In a synopsis, the composite line may be empty; in either type the exemplars may be empty.

### Matrix

In a matrix, the composite line is used to establish a set of columns; the exemplar lines are given in schematic form, with each column of the composite having a corresponding entry in the exemplars' columns. Matrices may be specified at the grapheme or word level: in Sumerian, they are typically specified at the grapheme level. The actual rules for matrices are given later in this page, but an example will give the general idea:

1\.     	

    šag4-ga-ne2 er2 im-si  edin-še3  ba-ra-e3
    
    N1,i\_1:    .    .  ,   +   +  +   +    ,    +  +  +
    N2,1:	   +	+  +   .   .  .   .    .    .  .  .
    N3,1:	   +    .  .   .   .  .   .    .    .  .  .
    Ki4,1:	   .	.  .   .   .  .   ,    +    +  +  +
    Šad1,1:	   .	+  +   +   +  +   +    +    ,  .  .
    Su1,2':	   .	.  .   .   .  ši  +    .    .  .  .
    X5,i\_1:	   .	.  .   .   .  .   .    .    .  .  .

The default matrix-level is graphemic. To specify that your matrix is word-level in a parsed score, add the token `word` at the end of the `@score` line (note that you don't need to do this with an unparsed matrix):

@score matrix parsed word

### Synoptic

In a synoptic score, the composite line and exemplar lines are both written out in full. The composite line may be empty, but this is not a recommended practice (it is allowed, as there is so much legacy data using this approach, but for new data the editor should, whenever possible, specify the composite text and ensure that it is properly used as the basis for translation).

### Parsed

In a parsed score, the composite and exemplar lines are validated and parsed according to the respective rules of the score types.

### Unparsed

In an unparsed score, the composite line must be parsable, but the exemplars are treated as a blob of text which is opaque to Oracc's parsers. This is strictly a transitional feature, which allows legacy data to be presented to users until such time as the necessary changes can be made to bring the score in line with Oracc parsing conventions.

## Conventions

### Labels

The composite and exemplar line-labeling conventions are shared by all types and modes of score.

### Composite

The composite line label has the same format as any other transliteration line in ATF: it is a string terminated by a period and one or more space or tab characters.

### Exemplar

An exemplar line label is basically string terminated by a colon and one or more space or tab characters. This string, however, has its own internal structure, consisting of a siglum, or code for a witness, and an optional line label.

Siglum

The siglum is typically a letter, often with numeric subscripts. To assist in alignment, numeric subscripts should be given with ASCII digits 0..9, which are automatically converted to Unicode subscript numbers by the processor.

In all types and modes of scores, the sigla must be defined in the ATF source for the score even when they are also defined in an external catalogue. This is done using the `#link` protocol:

#link: def A = P123456 = N 1

Additional identifiers may be given, but need not be. If no P-number has been assigned to the source, an X-number may be used, in which case additional identifiers such as publication places are strongly encouraged:

#link: def B = X000001 = N 1 = PBS 1, 29

Siglum Map

Siglum maps can be used when the exemplar lines reference a tablet by fragment rather than the main source. To use this feature, first declare the exemplar as above, then define the maps, then use the fragment reference in the exemplar lines.

The template for a map entry is:

#key: siglum-map FROM\_SIGLUM=>TO\_SIGLUM

Putting all of the components together, a full example looks like this:

    #link: def A = cmawro:P445799 = KUB 37, 44-49
    
    ...text
    
    #key: siglum-map A₁=>A
    #key: siglum-map A₂=>A
    #key: siglum-map A₃=>A
    
    ...
    
    A₁,obv\_i\_1′:	...

Label

A line-label may also be given, separated from the siglum by a comma. The label should conform to Oracc standards, with spaces replaced by underscores:

A,i\_1: a

A label may reference part of a line by including letter subscripts separated from the label by a semi-colon:

A,i\_1;a: a

A label may reference a range, separating the parts with a hyphen surrounded by underscores (the Oracc label specification requires spaces around a range-hyphen as line-numbers themselves may contain hyphens):

A,i\_1\_-\_i\_2b: a

### Synopses

Synoptic conventions for parsed line-content are simple: they are regular ATF.

### Matrices

Matrices have quite different conventions for composite and exemplar lines.

### Composite

Composite lines in matrices are basically in ATF, with these additions:

#

A hash-sign can be used to create an empty column in the composite; this is used when an exemplar has additional material which is not included in the composite.

0

A number-zero can be used as a grapheme to create an additional column within a word. This is useful when, for example, an exemplar has an additional component in a Sumerian verbal prefix chain.

### Exemplar Grapheme Codes

\+ (plus sign)

grapheme positively preserved

\- (minus sign)

grapheme positively omitted

`.` (period)

grapheme broken

`,` (comma)

grapheme traces fit composite

`x` (lowercase letter ex)

grapheme traces do not fit composite

`^` (caret)

exemplar adds following sign relative to composite

`#` (hash)

creates empty cell as in composite; if text is broken, use `#` or `.` depending on whether it is likely that the exemplar originally may have had a corresponding sign

### Exemplar Code Flags

These are a subset of the standard ATF flags (`#` is not used as a flag in matrices):

!

corrected reading

?

uncertain reading

\*

collated

### Exemplar Line Divisions

`;` (semi-colon)

indented line split point

`/` (forward slash)

line break (often with ruling; used with ranges)

### Replacements

`& (ampersand)`

at start of alignment column means text replaces how ever many columns the corresponding word occupies in the main text; must come at the start of a word.

&\[0-9\] (ampersand followed by digits)

at start of alignment column means text replaces how ever many columns the corresponding number of words occupy in the main text; must come at the start of a word.

&& (double ampersand)

at start of alignment column means following text replaces rest of line; no word alignment is done in this case.

### Dollar-lines

Lines beginning with a `$` are ATF $-line. If the $-line comes immediately after the composite, it is included in the composite. If the $-line contains an exemplar label, it pertains to that witness:

Ki1: $ Omits.

## Computing Witness Transliterations

Oracc can compute transliterations from scores of both kinds by sorting on the labels, splitting and reassembling portions of lines as necessary. For parsed synopses this procedure is relatively straightforward as the transliterations are already ATF. For unparsed synopses the witness transliteration is assumed invalid by the Oracc processor and is presented as-is.

For matrices, only the parsed form can be turned into witness transliterations: unparsed matrices cannot be meaningfully handled by the processor.

## Matrix Witnesses

In a matrix, the grapheme codes are simply replaced as appropriate with graphemes from the composite line. Where the exemplar contains transliteration, the texts replaces the text in the composite line. This results in a number of preferred-practice recommendations to ensure that the witness generation is as accurate as possible:

-   If the text involves different hyphenation the word or words should be given in their entirety, with the relevant &-span notation (to enable correct derivation of exemplar transliterations from the matrix). See DD 25 where both of the words must vary from the composite and so it might be tempting to use rest-of-line transliteration. Instead, we do word alignment for each word so that variant searching can work
-   Where reasonable, word alignment should be maintained, but where texts diverge extensively there may be no alternative to transliterating the exemplar in full (see DD line 13, exemplar Ki₁ for examples of both word alignment and rest-of-line transliteration).
-   The note marker ^\[DIGITS\]^ should be used in the matrix to handle insertions that belong in the witness transliteration but which overload the matrix structure. If the text immediately following the corresponding note label begins with a +, it is included with the matrix line's text when the source is rendered as a witness transliteration; this text must be terminated by a period followed by a space.
    
        55: ... szu-na ba-...  
        
        N₂₁\_r\_5': + +^1^ 
        
        #note: +{{NI?}} . Any note begins here ...  
        
        Is rendered as:
        
         
        5. ... szu-na{{NI?}} ba-... 
    
    After the initial +, text is inserted literally--to get a space or hyphen before the text it must be given after the +. The same rules apply at the end of the inserted text, hence the space before the closing period in the example above.
    

18 Dec 2019 osc at oracc dot org

Steve Tinney

Steve Tinney, 'Scores', _Oracc: The Open Richly Annotated Cuneiform Corpus_, Oracc, 2019 \[http://oracc.museum.upenn.edu/doc/help/editinginatf/scores/\]

[Oracc]: ../../../index.html
[Help]: ../../../help/index.html "Help page overview"
[Editing in ATF]: ../../../help/editinginatf/index.html "Working with ATF to edit texts"
