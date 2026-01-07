[Oracc] » [Help] » [Lemmatising] » How L2 works

# L2: How It Works

This document provides an overview of how the lemmatizer, L2, works to help Oracc builders understand what files are used for validation and how to control lemmatization.

## Overview

The lemmatizer binds corpora to glossaries. Interlinear lemmatizations are entered in the ATF files of the corpus and are checked and expanded by the lemmatizer to create fully qualified instances which may include normalization, morphological analysis and other information attached to them. The instances are then harvested and transformed into a glossary which has two basic formats: the editable format and the web format.

L2 has a very flexible approach to language handling, as a language in L2 is defined by a full language tag (dropping script components). Oracc defines a full set of basic language/dialect combinations, but projects may define additional ones if necessary. When we talk about "a project" having "a glossary" in this document, we mean that a project may have, in fact, many glossaries, one for each language or dialect. Some configuration settings may be applied at the language level or the project level. Thus, in the discussion of L2 modes below one can apply the same policy to all languages or have a blanket policy for the project and different settings for some languages.

## Projects

The relationship between lemmatization and projects in L2 is very simple: texts are only ever lemmatized within their owner project. Texts may be borrowed by other projects (proxied), but the borrowing project cannot change the lemmatization of the text.

## Functions

L2 performs three functions: it checks existing lemmatizations against one or more control lists; it expands existing lemmatizations (thus allowing the inline lemmatization to be shorter and easier to read); and it suggests lemmatizations for unlemmatized forms based on those same control lists.

## Signatures

We also refer to the control lists as signature sets or just "signatures". An L2 signature is a string which encodes all of the information relevant to an instance of a lemmatized word: for those familiar with L1 a signature is like a form, but with some additional information and without spaces between the fields.

Signatures may be derived from glossaries or from lemmatized corpora, and can be local to the project in which the text is lemmatized, or external to the project (in L1 the distinction was simply project versus system glossaries; in L2 it is possible to give a list of projects to search for lemmatizations).

## Modes

L2 can operate in any of three modes: automatic (auto), manual or mixed.

### Auto mode

In auto mode, the signatures which L2 uses to lemmatize texts in their own project are derived directly from the lemmatized corpus. Auto mode is suitable for smaller and/or more homogenous projects where it is feasible to track right and wrong glossary entries simply by reading through the web glossary.

### Manual mode

In manual mode, the signatures are derived from a glossary, which may be edited by hand to include information which is relevant to words and senses rather than to instances. The instance data needed to generate signature sets is stored in the glossary as `@form` lines, and the signatures used for checking and new lemmatization are derived only from the glossary.

### Mixed mode

In mixed mode, a manual glossary is used to maintain data relevant to words and senses, but the instance data is not stored in the glossary. Instead, the instance data is harvested from the corpus as with auto mode. Mixed mode is appropriate for the same kinds of project as auto mode.

## Glossaries

L2 always works with at least an automatically generated glossary. This is always constructed from the lemmatized texts in a project's corpus (including texts which may have been borrowed from other projects). This corpus-based glossary is the version from which the web format glossary is derived.

In addition, a project may have a manual glossary. This can be edited both to control which forms are considered valid in a project and to add information like bibliography, language-specific citation forms etc.

When creating the web glossary, the situation where there is no manual glossary is straightforward. When there is a manual glossary, however, complications arise because the corpus-based glossary may have instances which are not covered in the manual glossary (i.e., invalid instances or outlaws), and the manual glossary may have forms which are not attested in the corpus (i.e., ghosts). Configuration options control how to handle these cases. Outlaws may be dropped, included with special marking (e.g., hilighting in red) or included without special marking. Similarly with ghosts, which have their own configuration variable so that the two can be handled differently if desired.

18 Dec 2019 osc at oracc dot org

Steve Tinney

Steve Tinney, 'L2: How It Works', _Oracc: The Open Richly Annotated Cuneiform Corpus_, Oracc, 2019 \[http://oracc.museum.upenn.edu/doc/help/lemmatising/howl2works/\]

[Oracc]: ../../../index.html
[Help]: ../../../help/index.html "Help page overview"
[Lemmatising]: ../../../help/lemmatising/index.html "Lemmatising ATF Files"
