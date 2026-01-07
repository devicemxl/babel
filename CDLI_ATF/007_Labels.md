# Labels

Labels are generated for lines by the ATF processor and are used to reference lines in some parts of the ATF system. This document describes the syntax of labels.

## Overview

Labels are a shorthand way of referring to the location of a line on an object. For transliterations, labels consist of at most three parts: a `SURFACE` abbreviation, a `COLUMN` designation and a `LINE` number.

### SURFACE

The `SURFACE` field is an abbreviation of ATF surface tags according to the following table:

| ATF | LABEL |
| --- | --- |
| @obverse | o   |
| @reverse | r   |
| @bottom | b.e. |
| @edge | e.  |
| @left | l.e. |
| @right | r.e. |
| @top | t.e. |

If the transliteration does not give `@obverse` explicitly, labels for line numbers on the obverse do not include the \`o'.

### COLUMN

Column numbers in labels are rendered in roman numerals, which both follows normal Assyriological practice and avoids possible confusion with the line numbers. This does mean, however, that the notations for column numbers in ATF sources and labels are different: `@column 1` in a label is `i`.

If the transliteration does not include column number tags, no column number component is included in the label.

### LINE

There are two possible line numbers which the ATF processor can use in labels. By default, the processor renumbers lines according to CDLI conventions--restarting line numbers at \`1' at the start of each surface and numbering lines consecutively. However, in contexts where stability is required--where the labels are being used to link exemplar lines to composite lines, for example--the ATF protocol:

#atf: use mylines

should be used. This instructs the processor to prefer the user's line numbers to its auto-generated ones. The line numbers in transliterations have few restrictions--as long as they consist of a series of non-spaces followed by a period followed by a space they are considered acceptable.

## Syntax

### LABEL

Considering the preceding comments and using the convention `?` to indicate optional components, the syntax of a single label is then:

LABEL => SURFACE? COLUMN? LINE

### LABEL\_RANGE

There is a standard syntax for ranges also, which must be observed when, e.g., translations use labeling to refer to blocks of transliteration. In such cases, two labels may be given and **must** be separated by the sequence: SPACES HYPHEN SPACES. The reason for requiring the spaces is that ATF line numbers may contain hyphens so we require ranges to include spaces between the components.

Formally, then, we have the following definition:

LABEL\_RANGE => LABEL ' - ' LABEL

### LABEL\_SPEC

Combining the preceding definitions, we can now define a label specification, LABEL\_SPEC, as follows (using the standard notation of vertical bar (\`|') = OR):

LABEL\_SPEC => LABEL | LABEL\_RANGE

## Examples

Let the notation `@obverse ... @column 1 ... 1.` mean that the ATF transliteration has block tags `@obverse` and `@column 1`, among other possible content, and that `1.` is a line number. Then the following relations apply:

| ATF | LABEL |
| --- | --- |
| 1.  | 1   |
| @column 1 ... 1. | i 1 |
| @obverse ... @column 1 ... 1. | o i 1 |
| @left ... 3'. | l.e. 3' |

## Related documentation

-   [Labeled translations](../../../help/editinginatf/translations/index.html#sh_labeled "Jump to  in Translations")
-   [ATF linkage](../../../help/editinginatf/linkage/index.html "ATF Linkage")

18 Dec 2019 osc at oracc dot org

Steve Tinney

Steve Tinney, 'Labels', _Oracc: The Open Richly Annotated Cuneiform Corpus_, Oracc, 2019 \[http://oracc.museum.upenn.edu/doc/help/editinginatf/labels/\]
