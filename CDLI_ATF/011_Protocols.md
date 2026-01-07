# ATF Protocols

This page offers an overview of the protocols which may be used in ATF documents.

Protocols are statements which are interpreted or stored by the ATF processor but are not part of the text edition proper. Protocols are all named and may trigger special processing within the ATF processor.

Protocols are indicated in ATF by a line beginning with the hash character (`#`), a known protocol name and a colon character (`:`).

With the exception of `#note:`, protocols must occur on a single line; multiple protocols do not need blank lines between them except for multiple `#note:` protocols which behave like comments.

Protocols are divided into four classes:

outer

protocols which may only occur at the very beginning of the document; only `#basket:` may occur in this location.

start

protocols which may occur at the start of a text; only `#atf:`, `#bib:`, `#link:`, `#note:` and `#version:` may occur in this location.

after

protocols which may occur only after all other protocols have been given in a particular section; only `#note:` may occur in this location. Other protocols are not required before `#note:`, but if they are present they must precede it.

inter

protocols which may occur between lines of a text; only `#bib:`, `#lem:`, `#note:` and `#var:` may occur in this location.

#bib: MSL 14, 343

1. a
#lem: a\[water\]
#note: This can only occur after any protocols other than #note:.

### #atf:

Introduces directives to the ATF processor. Implemented directives are:

`lang <LANG>`

Sets the default language for the text; see under [languages in the GDL tutorial](../../../help/editinginatf/primer/inlinetutorial/index.html#sh_languages "Jump to  in ATF Inline Tutorial") for more information.

#atf: lang qpc

`use <FEATURE>`

The `use` directive enables [less commonly used ATF features](../../../help/editinginatf/advancedconventions/index.html "ATF Advanced Conventions"), which are turned off by default, to be turned on. `FEATURE` must be one of: alignment-groups; legacy; lexical; math; mylines.

#atf: use lexical

### #basket:

This protocol is used only by the CDLI ATF repository system; the content is a token used internally by the repository and should not be changed by users.

### #bib:

Bibliography information my be included using this protocol and may then be included with locator strings to provide text and publication information, e.g.:

&P312111 = Some Lexical Text
1. a
#bib: MSL 14, 33

It could be rendered as: `(Some Lexical Text 1 [MSL 14, 33])` but is not currently implemented.

### #lem:

Gives lemmatization for the line before. The format is a list of lemmata separated by semi-colon-space (`;` ) and the number of lemmata must equal the number of words in the lemmatized line:

1\. a i3-nag
#lem: a\[water\]; naj\[drink\]

### #lemmatizer:

Introduces directives to the lemmatization subsystem. Implemented directives are:

`sparse do <FIELDS>`

Enables selective lemmatization which is useful for texts where not all fields have been (or can be) lemmatized. The `<FIELDS>` must match field names used in the document. See the lexical documentation for an example.

### #link:

Introduces directives to the linkage subsystem. Implemented directives are:

`def <SYMBOL> = <ID> = <NAME>`

Defines a SYMBOL to refer to the text indicated by ID and NAME; interlinear links can then refer to the text via the symbol (see the linkage documentation for more information and examples):

&P123321 = Some Exemplar
#link: def A = Q000002 = Archaic Lu A
1. NAMESZDA
>> A 1

### #note:

Notes given using this protocol are included in the rendered ATF text.

### #syntax:

Introduces directives to the syntax processing subsystem. Implemented directives are:

`line_is_unit`

Instructs the unit-processor to treat each line as a unit by default. This protocol is automatically emitted when `#atf: use lexical` is given.

### #var:

Informal annotation of text variants; see the composites documentation for a more structured implementation.

### #version:

Provides a location in the ATF file for a version number or version control system string.

18 Dec 2019 osc at oracc dot org

Steve Tinney

Steve Tinney, 'ATF Protocols', _Oracc: The Open Richly Annotated Cuneiform Corpus_, Oracc, 2019 \[http://oracc.museum.upenn.edu/doc/help/editinginatf/protocols/\]
