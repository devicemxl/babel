[Oracc] » [Help] » [Lemmatising] » Signatures

# Signatures

Signatures are the string representation of an instance's lemmatization data and consists of a sequence of fields, each introduced by a distinct prefix character or characters. A complete signature looks like this:

@epsd2%sux:a=a\[water//water\]N'N/a#~$a

Abbreviated Signatures

Oracc's lemmatization allows users to enter just a few key pieces of a signature (this is the "instance lemmatization") and the lemmatizer looks this data up in the glossary and creates complete signatures from it.

Users typically enter just the citation form (CF, a in the example above) and the sense (SENSE, water above), and the instance lemmatization is then `a[water]`. It is also not uncommon to give simply a Part-of-Speech, such as `PN`, for the instance lemmatization.

Signature Fields and Prefix Characters

@ = PROJECT

The project to which this signature belongs

% = LANG

The language for the signature; may also have a writing system, e.g., %akk-949 for normalized Akkadian

: = FORM

The form of the word as it appears in the text

\= = CF

The = separates FORM and CF, or Citation Form; the equals may be omitted if the CF is the first entry in the signature, as in a\[water\]

\[ ... \]

Square brackets surround the GW, or Guide Word, and/or SENSE

//

Only within \[...\], the double slash // separates GW and SENSE

POS

The POS (Part-of-Speech) is identified by its position immediately after the closing square bracket of \[...\]

' = EPOS

The right-quote, ', is the prefix character for the EPOS, the Effective Part-of-Speech

$ = NORM

The normalized version of the writing. This varies by language: in Akkadian, for example, it is the transcription of the word-form, without hyphens and determinatives and with accents. This is not used in the source version of Sumerian glossaries because it can be computed from the morphology (see below).

\* = STEM

The STEM, which may be a form of the BASE in Sumerian, or a notation such as D, Š, N, in Akkadian, or possibly other conventions for other languages.

/ = BASE

The BASE utilized in a Sumerian writing. This must match a base given in the `@bases` part of the entry.

\+ = CONT

The Sumerian grapheme following the base, used only when that grapheme is the continuation of the end of the BASE, e.g., `-ma` in `inim-ma`. The deconstruction of the grapheme gives the consonant which continues the grapheme followed by the vowel which is normally a morpheme or morpheme constituent.

\# = MORPH

The morphology string for the writing.

\## = MORPH2

The second morphology string for the writing.

@ = RWS

The RWS, Register or Writing System, for the form.

[Oracc]: ../../../index.html
[Help]: ../../../help/index.html "Help page overview"
[Lemmatising]: ../../../help/lemmatising/index.html "Lemmatising ATF Files"
