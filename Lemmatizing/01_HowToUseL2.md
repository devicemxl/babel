[Oracc] » [Help] » [Lemmatising] » Lemmatising

# Lemmatising: How To Use L2

This page summarises the steps required to use L2, the lemmatiser used by Oracc. First we describe what you need to know about editing ATF files, then glossary management, then rebuilding the whole project.

This page is designed as a refresher for those already familiar with lemmatisation. If you have not already done so, read the [tutorial on linguistic annotation] first.

## Editing and fixing ATF files

### Languages

If your project uses Akkadian, set the default language of your text using the [protocol line] \[http://oracc.museum.upenn.edu/ns/xtf/1.0/protocols.html\] `#atf: lang akk-x-[DIALECT]`. For instance, if your project's language should be described as, e.g., Old Babylonian, you will need to write:

#atf: lang akk-x-oldbab

If you need to switch languages or dialects in the middle of a text, you can use a [short code] \[http://oracc.museum.upenn.edu/doc/developer/l2/languages/#Language\_codes\]. For instance, to mark a Neo-Assyrian dialect word in an otherwise Standard Babylonian text, you can write, e.g.,

{d}NIN.LIL₂ ana {d}BAD %na a-bu-su %sb DAB-su

Here, the code `%na` marks the switch into Neo-Assyrian, while `%sb` marks the switch back to Standard Babylonian.

You do not mark a language switch at the end of a line, as the processor automatically returns to the default language at the start of each line.

For more about L2's handling of languages see the [languages] section of the Inline Tutorial.

### SENSE and EPOS

When you add a new lemmatisation which has a [SENSE] as well as a [GW], you always need to add an EPOS too, even when it is the same as the POS. For instance, instead of `+šaknu[appointee//governor]N$` the correct entry is:

+šaknu\[appointee//governor\]N'N$

But if there is no SENSE, there is no need to add an EPOS:

+šaknu\[appointee\]N$

If you forget to add an EPOS where it's needed, the checker will tell you!

### COFs and PSUs

Lemmatise Compound Orthographic Forms (COFs) [as described here].

You can add SENSEs to individual components of a Phrasal Semantic Unit (PSU) if this is appropriate. An overview of PSUs in L2 is given [here].

### Sentence boundaries

If you are in the habit of marking sentence boundaries in the lemmatisation with `+.` you will need to ensure that they occur _before_ the semi-colons that mark the end of a lemmatisation, not after them. That is, the correct form is, e.g.,

iddâk\[kill\]V +.; šumma\[if\]MOD;

not `iddâk[kill]V; +. šumma[if]MOD;`.

## Editing and fixing glossaries

### Language/dialect glossaries

There is a glossary for each dialect of the languages in your corpus (as defined by the [language] tags in your ATF files), with names such as `akk-x-oldass.glo` and `akk-x-stdbab.glo`. The higher-level language glossaries, such as `akk.glo` are now generated from these lower-level ones. So, when you need to hand-edit glossary entries, you will need to do so in the relevant dialect-level glossary or glossaries, not in the top-level language glossaries as before.

### Byforms

You can now use the [byforms] mechanism in your Sumerian glossary to handle phenomena such as suppletive verbs, collapsed compounds and variant frozen forms.

Byforms are not yet implemented for Akkadian, but if you see a need for them in your project please contact your liaison.

### COF and PSU handling

L2 handles Compound Orthographic Forms (COFs) in exactly the same way as before. You should not need to fix COF entries in the glossary if they are already entered correctly. A brief overview of COFs in L2 glossaries is given [here].

Error-checks of Phrasal Semantic Units (PSUs) are rigorous. You should not need to fix PSUs entries in the glossary if they are already entered correctly, except if they also contain a COF. A brief overview of PSUs in L2 glossaries is given [here].

## Rebuilding L2 projects

Here are some hints on how to fix most of the error messages relating to lemmatisation but if you notice error messages that you cannot interpret, please contact your liaison for help.

-   error messages with the label [(f2)]
-   error messages with the label [(lem)]
-   error messages with the label [unknown COF component]
-   error messages with the label [PSU component not found in glossary].

## Project configuration: Glossaries

You can control which glossaries are used to lemmatise your project, language by language. Use following option as many times as you need to:

<option name="\[LANGUAGE\]" value="\[PROJECT AND/OR GLOSSARY NAMES\]">

For instance:

<option name="%akk-x-ltebab" value="hbtin cams/gkab"/>
<option name="%akk-x-neoass" value=". .:akk-x-stdbab"/>

Here, the lemmatiser is told to look up forms tagged as Late Babylonian first in the HBTIN project's glossary (which is all LB), then in CAMS/GKAB's LB glossary. Neo-Assyrian forms are to be looked up first in the project's own NA glossary (the meaning of `.`) and then in the project's own SB glossary (the `.` followed by a `:` and the relevant language code).

If you do not add an entry to the config file for a particular language, the system will just use the project glossary for that language, as expected.

18 Dec 2019 osc at oracc dot org

Steve Tinney & Eleanor Robson

Steve Tinney & Eleanor Robson, 'Lemmatising: How To Use L2', _Oracc: The Open Richly Annotated Cuneiform Corpus_, Oracc, 2019 \[http://oracc.museum.upenn.edu/doc/help/lemmatising/lemmatising/\]

[Oracc]: ../../../index.html
[Help]: ../../../help/index.html "Help page overview"
[Lemmatising]: ../../../help/lemmatising/index.html "Lemmatising ATF Files"
[tutorial on linguistic annotation]: ../../../help/lemmatising/primer/index.html "Lemmatisation primer"
[protocol line]: http://oracc.museum.upenn.edu/ns/xtf/1.0/protocols.html "Link opens in new window"
[short code]: http://oracc.museum.upenn.edu/doc/developer/l2/languages/#Language_codes "Link opens in new window"
[languages]: ../../../help/editinginatf/primer/inlinetutorial/index.html#h_languages "Jump to  in ATF Inline Tutorial"
[SENSE]: ../../../help/lemmatising/primer/index.html#h_senseandepos "Jump to  in Lemmatisation primer"
[GW]: ../../../help/lemmatising/primer/index.html#h_replacingxs "Jump to  in Lemmatisation primer"
[as described here]: ../../../help/glossaries/cofs/index.html#h_lemmatizing "Jump to  in COFs: Compound Orthographic Forms"
[here]: ../../../help/glossaries/psus/index.html#h_glossarizing "Jump to  in PSUs: Phrasal Semantic Units"
[language]: #h_languages "Jump to  on this page"
[byforms]: ../../../help/glossaries/bffs/index.html "BFFs: Byforms"
[here]: ../../../help/glossaries/cofs/index.html#h_glossarizing "Jump to  in COFs: Compound Orthographic Forms"
[here]: ../../../help/glossaries/psus/index.html#h_glossarizing "Jump to  in PSUs: Phrasal Semantic Units"
[(f2)]: ../../../help/lemmatising/rebuilderrors/index.html#h_f2errors "Jump to  in Rebuild errors"
[(lem)]: ../../../help/lemmatising/rebuilderrors/index.html#h_lemerrors "Jump to  in Rebuild errors"
[unknown COF component]: ../../../help/glossaries/cofs/index.html#h_unknowncofcomponent "Jump to  in COFs: Compound Orthographic Forms"
[PSU component not found in glossary]: ../../../help/glossaries/psus/index.html#h_psucomponentnotfoundinglossary "Jump to  in PSUs: Phrasal Semantic Units"
