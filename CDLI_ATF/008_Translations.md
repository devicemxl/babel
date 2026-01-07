# Translations

Translations may be input as interlinear, within the ATF files, or extralinear either within ATF files or separately. The Oracc translation format and the special facilities it provides are described here.

## Location

Translations are a special part of an ATF text; they may be given within an ATF text which contains a transliteration or they may be in their own ATF text. If they are in their own ATF text they require their own `&`\-line which must be identical to the `&`\-line used in the corresponding transliteration (see [the ATF tutorial](../../../help/editinginatf/primer/structuretutorial/index.html#andlines "Jump to  in ATF Structure Tutorial") for further details on `&`\-lines).

Because the ATF processor requires access to both the transliteration and the translation of a text it is easiest practice to give translations along with the transliteration. While this is not a requirement, because the ATF processor can read multiple files on a single run and process them all simultaneously, the multi-file facility is not presently available in the webservice.

## Types

All translation types except interlinear are introduced by a `@translation` command followed by the translation type, a language code, and the word `project`. The keyword `project` indicates that this is the default translation of a text within a project, in order to facilitate cross-project sharing of texts.

### Interlinear

Interlinear translations are given using the ATF protocol `#tr.<LANG>:`; the translation follows. A language code may be given after a period: these language codes must follow the Oracc rules for language codes as given in the [GDL tutorial](../../../help/editinginatf/primer/inlinetutorial/index.html#sh_languages "Jump to  in ATF Inline Tutorial"). For an English translation the protocol would then be #tr.en:.

If no language code is given the default is `en`.

### Parallel

Parallel translations start with the command:

@translation parallel en project

(Here and in the following examples `en` may be any standard language code.)

The remainder of the translation must use exactly the same structural labeling as the transliteration; the ATF processor will automatically align the transliteration and translation using their common structure.

### Labeled

Labeled translations start with the command:

@translation labeled en project

Subsequent blocks of translation are introduced by `@label` or `@( )` commands where the remainder of the line, or the contents of the parentheses, gives the label. The label must be either a single label which matches a line label in the translated source, or a range, i.e., a pair of labels giving the start and end lines.

The following are all examples of valid translation labels:

@label o 17

This labels the translation of a single line of transliteration, from obverse line 17. It can also be written as `@(o 17)`.

@label r ii 3' - r ii 4'

This label, which can also be written as `@(r ii 3' - r ii 4')`, marks a block of translation that runs from reverse column 2, line 3' to line 4'. Even though they are adjacent lines on the same column, the start line and end line must both be given explicitly. A label `@label r ii 3' - 4'` is an error.

@label l.e. 1 - t.e. 2

Labels can describe blocks of translation that cross surfaces and columns. This example, which can also be written `@(l.e. 1 - t.e. 2)`, runs from the first line of the left edge to the second line of the top edge.

If you want to have two lines labelled exactly the same way, use `+` after the `@label`. For instance:

@label r 6
Witnesses: Anu-belšunu, son of Nidinti-Anu, descendant of Sin-leqe-unninni;

@label+ r 6
Anu-ab-uter, son of Anu-belšunu, descendant of Sin-leqe-unninni;

It is not necessary to use the `+` if your second label is, say, `@label r 6 - r 7`.

**N.B.:** Labeling in translations must always be done at the line level; a label such as `r` (reverse) is an error.

For further explanation of how labels work, and a complete list of label abbreviations, see the [labels](../../../help/editinginatf/labels/index.html "Labels") documentation.

### Unitary

Unitary translations—those whose translation blocks correspond to the annotated units (usually sentences) of a transliteration—start with the command.

@translation unitary en project

Subsequent blocks of translation are introduced by `@unit` commands where the remainder of the line gives a unit number; these can be found in the unit-view of the source texts—typically unit 1 is the first sentence, unit 2 is the second sentence, and so on.

Unitary translations may also follow `@unit` with a `@span` command which follows the same rules as a `@label` line.

## Conventions

### Block

A small set of essential block-level commands is available in labeled and unitary translation styles; if you want to use these block commands with interlinear or parallel styles, you can't. You must first convert your translation to use labeled or unitary style.

### Paragraphs

For labeled and unitary translation types the content of a translation unit is a single paragraph. A blank line is **required** to close the paragraph.

For parallel and interlinear translation types the content of a translation unit is the rest of the line following the label or `#tr:`, as well as any following lines which start with at least one space and which do not consist only of spaces:

#tr: this is a long interlinear translation which is more comfortably
     handled if split over more than one line.

### Headings

In labeled and unitary translation types headings may be used before the `@label`s. A heading consists of a paragraph beginning with one of the commands: `@h1`, `@h2`, `@h3` specifying first, second and third level headings respectively.

The content of a heading may use the same inline conventions as translation content.

@h1 Inana steals the @me

@label o 1 - o 10
...

### Dollar Lines

Translations may contain dollar-lines, in which case they must ordinarily correspond on a 1:1 basis with the $-lines in the transliteration. [See below](#h_alignment "Jump to  on this page") for a discussion of how to handle situations which do not conform to this constraint.

### Notes

In labeled and unitary translation types notes may be given immediately after either headings or translation paragraphs. These notes may begin with a note marker corresponding to a note marker in the preceding heading or translation content (see Inline Conventions below):

@label 1

The girl^1^ stood on the burning deck.

@note ^1^ Three manuscripts read instead: boy.

@label 2
...

If no note marker is given the note is automatically linked to the entire preceding heading or translation unit.

A note may contain one or more paragraphs; paragraphs are separated by blank lines (the processor understands that a line containing only spaces is a "blank line"). A blank line is **required** to close the final paragraph of the note.

### Inline

### Characters

The character set used must be Unicode—no ATF translation of sz (for š) and similar conventions is done.

### Supplied

Text supplied for the sense is given in parentheses, e.g., `He (Gudea) brought (stone) down from (the mountain).`

### Literal

Where the literal rendering is known but inadequate for the context, a word or words may be bracketed by matched pairs of `@"..."@` commands, e.g., `...ignore the @"striking"@ among...`.

### Foreign

Foreign words are indicated by placing an '@'-sign before the word, e.g., `Inana took the @me`.

### Uncertain

Uncertain translations are bracketed by matched pairs of `@?...?@` commands (note that the close-uncertain form is query then at-sign), e.g., `@?he built the temple?@`.

### Untranslateable

Untranslateable passages should be indicated by an ellipsis (`...`). At the end of a sentence, a four-dot ellipsis should be used (`....`). Every sequences of one or more x's in the transliteration should be represented by a (`...`) in the transliteration.

### Broken

For every `[...]` or sequence of x's in square brackets in the transliteration there should be a matching `[...]` in the translation.

Words that are entirely restored in the transliteration should be in square brackets `[ ]` in the translation, but partially restored ones should not. Do not put square brackets in the middle of words but use `@? ?@` to mark uncertainty if appropriate.

### Note markers

Note markers may be given by placing numbers between matched pairs of caret (`^`) characters: `this is noted.^1^`. Multiple notes may be referenced in a single marker by separating them with commas.

## Projects

Certain aspects of translation are project-specific and should be defined in a project style-manual. These include, among others, practices for normalizing proper names and whether or not to indicate breakage on the original object in the translation.

## Alignment

For most situations the default handling of alignment of transliteration and translation is adequate. In the normal case, each labeled translation block must have a corresponding label in the translation, and each translation dollar-line must have a matching dollar-line in the transliteration.

For special purposes—including migrating legacy data—several non-standard combinations of alignment are supported in ATF, however.

### Out of sequence translations

Sometimes you want to translate a block, say lines 3 to 8, but with the last line first. It would be tempting to say `@label 8 - 7` but this doesn't work because of the way the ATF processor uses the labels to do alignment of translation and transliteration.

Instead, you can use the label-as construction, in which the alignment label is given first as usual, then the displayed label is given afterwards. If you are using this method of alignment you should not use ranges in labels—just let the ATF processor determine the end of the block for you.

The label-as construction consists of a label, an equals sign surrounded by spaces, and a second label:

@label 3 = 8

Means: align on line 3, but display as line 8.

### Labeling lines within a paragraph

Some people like to label the lines of a translation within the block. Do this using the `@lab{...}` tag—this is set up to use the same display conventions as regular labels.

@label 1 - 4

This is some @lab{3}text with @lab{4}an unusual translation 
@lab{2}sequence.

### @-heading only in translation

This does not require any special action as the formatter automatically handles it; it is important to know, though, that the opposite case is not automatically handled: see the next paragraph.

### @-heading only in transliteration

In this case, it is necessary to give empty headings in the translation to align the transliteration/translation correctly.

@h1 Inscription 1
@m=locator Inscription\_1

1. %arc mnn 15 b zy ʾrqʾ

@h1 Inscription 2
@m=locator Inscription\_2

1. %arc ḥmšt ʿšr mnyn \[zy\] mlk

@translation labeled en project

@h1

@(Inscription\_1 1) Fifteen @i{mina}s (by the standard) of the land.

@h1

@(Inscription\_2 1) Fifteen @i{mina}s \[of\] the king.

### $-line only in transliteration

This does not necessarily require any special action; the translation automatically aligns on labels. An empty $-line may be used in the translation, however, the difference between no dollar line and and an empty dollar line being that in the former case the block-alignment of a labeled translation will extend to include the transliteration's $-line; in the latter case, the two $-lines will align, so the translation block will stop at the line before the transliteration's $-line.

### $-line only in translation

To create this effect an empty $-line must be entered in the transliteration.

### $-line in transliteration aligns with translation block

To do this, the transliteration $-line must first be given a label using the syntax `$@(LABEL)`, where `LABEL` is any unique label within the text. To achieve the alignment, the translation must then use the same label; this label is purely a convenience and is never rendered.

### $-line in translation aligns with text line in transliteration

Again, the $-line must be labeled in order to achieve this effect—in this case, the label of the transliteration line must be given as in, e.g., `$@(r 1)`.

Note that this idiom can also be used to align a translation $-line with a surface or column @-command in the transliteration. To align with `@reverse` you simply write, say, `$@(r) Rev`.

### Transliteration line is untranslated

If the transliteration should have space facing it, or some kind of comment, simply use an empty $-line with a label, as in the previous example.

### Translation has no corresponding transliteration

This effect can be obtained by creating a dummy transliteration line, which must have a unique label and contain only the inline comment `(#DUMMY#)`. The translation must use the dummy line's label; the dummy line creates no output other than blank space.

### A single transliteration line has two or more translation blocks

By default, the processor complains about this situation with a `translation alignment out of order` warning. To instruct the processor that this situation is in fact correct, follow the label with a `+` sign:

...
9. IGI {m}bar-ruq ITI ZIZ₂
...
@(9) Witness Barruq.

@(9)+ Month Shebat.

## Examples

### An Akkadian tablet in Unicode: SpTU 4, 221 (NB prebend sale) in Interlinear style

&P348808 = SpTU 4, 221
#atf: lang akk
#atf: use unicode
#project: cams

@tablet
@obverse
1.	\[ṭup\]-pi₂# GIŠ#.ŠUB.BA {lu₂}KU₄.E₂{+u₂-tu}
#tr.en: Tablet of the temple-enterer's prebend, 

2.	E₂ {m}{d}E₂.A--kur-ban-ni pa-pa-hu {d}INANA UNUG{ki} u
#tr.en: house of Ea-kurbanni (and) cella of Ištar of Uruk and

3.	{d}na-na-a 3 SILA₃ NINDA-HI.A 3 GUR KAŠ SAG <<ar₂-ki>>
#tr.en: Nanaya, (consisting of:) 3 @qū of bread, 3 @kurru of first-class beer,

4.	ma-ak-ka-su gi-nu-u₂ gu-uq-qu-u₂
#tr.en: good-quality dates, regular @ginû and @guqqû-offerings,

5.	SISKUR₂ LUGAL SISKUR₂ {lu₂}ka-ri-bi ki-i pi-i 1{+en}
#tr.en: offerings for the king, offerings for the @kāribu-priest according to @?the one?@

6.	{lu₂}KU₄.E₂ ša₂ E₂.AN.NA
#tr.en: temple-enterer of Eanna.

$	single ruling	

7.	ki-i 15 MA.NA KU₃.BABBAR KU₃.PAD.DU {m}NIG₂.DU DUMU-šu₂ {m}NUMUN--DU
#tr.en: For 15 minas of silver in blocks, Kudurru, son of Zer-ukin,

8.	it-ti {m}{d}AMAR.UTU--GAR--MU A-šu₂ ša₂ {m}{d}AMAR.UTU--MU--URI₃
#tr.en: with Marduk-šakin-šumi, son of Marduk-šum-uṣur,

9.	GANBA im-be₂-e#-ma i-šam ŠAM₂-šu₂ gam-ru-tu
#tr.en: agreed a price and then he (Kudurru) bought (the prebend) for its full price.

$	single ruling	

10.	PAP 15 MA.NA KU₃.BABBAR KU₃.PAD.DU a-di 5 GIN₂ KU₃.BABBAR
#tr.en: The total (is) 15 minas of silver in blocks together with 5 shekels of silver

### SpTU 4, 221 (NB prebend sale) in Parallel style

&P348808 = SpTU 4, 221
#atf: lang akk
#atf: use unicode
#project: cams

@tablet
@obverse
1.	\[ṭup\]-pi₂# GIŠ#.ŠUB.BA {lu₂}KU₄.E₂{+u₂-tu}
2.	E₂ {m}{d}E₂.A--kur-ban-ni pa-pa-hu {d}INANA UNUG{ki} u
3.	{d}na-na-a 3 SILA₃ NINDA-HI.A 3 GUR KAŠ SAG <<ar₂-ki>>
4.	ma-ak-ka-su gi-nu-u₂ gu-uq-qu-u₂
5.	SISKUR₂ LUGAL SISKUR₂ {lu₂}ka-ri-bi ki-i pi-i 1{+en}
6.	{lu₂}KU₄.E₂ ša₂ E₂.AN.NA
$	single ruling	
7.	ki-i 15 MA.NA KU₃.BABBAR KU₃.PAD.DU {m}NIG₂.DU DUMU-šu₂ {m}NUMUN--DU
8.	it-ti {m}{d}AMAR.UTU--GAR--MU A-šu₂ ša₂ {m}{d}AMAR.UTU--MU--URI₃
9.	GANBA im-be₂-e#-ma i-šam ŠAM₂-šu₂ gam-ru-tu
$	single ruling	
10.	PAP 15 MA.NA KU₃.BABBAR KU₃.PAD.DU a-di 5 GIN₂ KU₃.BABBAR

@translation parallel en project
@obverse
1. Tablet of the temple-enterer's prebend, 
2. house of Ea-kurbanni (and) cella of Ištar of Uruk and
3. Nanaya, (consisting of:) 3 @qū of bread, 3 @kurru of first-class beer,
4. good-quality dates, regular @ginû and @guqqû-offerings,
5. offerings for the king, offerings for the @kāribu-priest according to @?the one?@
6. temple-enterer of Eanna.
$ single ruling
7. For 15 minas of silver in blocks, Kudurru, son of Zer-ukin,
8. with Marduk-šakin-šumi, son of Marduk-šum-uṣur,
9. agreed a price and then he (Kudurru) bought (the prebend) for its full price.
$ single ruling
10. The total (is) 15 minas of silver in blocks together with 5 shekels of silver

### SpTU 4, 221 (NB prebend sale) in Labeled style

&P348808 = SpTU 4, 221
#atf: lang akk
#atf: use unicode
#project: cams

@tablet
@obverse
1.	\[ṭup\]-pi₂# GIŠ#.ŠUB.BA {lu₂}KU₄.E₂{+u₂-tu}
2.	E₂ {m}{d}E₂.A--kur-ban-ni pa-pa-hu {d}INANA UNUG{ki} u
3.	{d}na-na-a 3 SILA₃ NINDA-HI.A 3 GUR KAŠ SAG <<ar₂-ki>>
4.	ma-ak-ka-su gi-nu-u₂ gu-uq-qu-u₂
5.	SISKUR₂ LUGAL SISKUR₂ {lu₂}ka-ri-bi ki-i pi-i 1{+en}
6.	{lu₂}KU₄.E₂ ša₂ E₂.AN.NA
$	single ruling	
7.	ki-i 15 MA.NA KU₃.BABBAR KU₃.PAD.DU {m}NIG₂.DU DUMU-šu₂ {m}NUMUN--DU
8.	it-ti {m}{d}AMAR.UTU--GAR--MU A-šu₂ ša₂ {m}{d}AMAR.UTU--MU--URI₃
9.	GANBA im-be₂-e#-ma i-šam ŠAM₂-šu₂ gam-ru-tu
$	single ruling	
10.	PAP 15 MA.NA KU₃.BABBAR KU₃.PAD.DU a-di 5 GIN₂ KU₃.BABBAR

@translation labeled en project
@label o 1 - o 6
Tablet of the temple-enterer's prebend, house of Ea-kurbanni (and) cella 
of Ištar of Uruk and Nanaya, (consisting of:) 3 @qū of bread, 3 @kurru of 
first-class beer, good-quality dates, regular @ginû and @guqqû-offerings, 
offerings for the king, offerings for the @kāribu-priest according to 
@?the one?@ temple-enterer of Eanna.

$ single ruling

@label o 7 - o 9
For 15 minas of silver in blocks, Kudurru, son of Zer-ukin, with Marduk-
šakin-šumi, son of Marduk-šum-uṣur, agreed a price and then he (Kudurru) 
bought (the prebend) for its full price.

$ single ruling

@label o 10
The total (is) 15 minas of silver in blocks together with 5 shekels of silver

This is the translation style used in CAMS's edition of this text; you can see the online version [here](http://oracc.museum.upenn.edu/cams/gkab/P348808 "Link opens in new window") \[http://oracc.museum.upenn.edu/cams/gkab/P348808\].

### SpTU 4, 221 (NB prebend sale) in Unitary style

&P348808 = SpTU 4, 221
#atf: lang akk
#atf: use unicode
#project: cams

@tablet
@obverse
1.	\[ṭup\]-pi₂# GIŠ#.ŠUB.BA {lu₂}KU₄.E₂{+u₂-tu}
2.	E₂ {m}{d}E₂.A--kur-ban-ni pa-pa-hu {d}INANA UNUG{ki} u
3.	{d}na-na-a 3 SILA₃ NINDA-HI.A 3 GUR KAŠ SAG <<ar₂-ki>>
4.	ma-ak-ka-su gi-nu-u₂ gu-uq-qu-u₂
5.	SISKUR₂ LUGAL SISKUR₂ {lu₂}ka-ri-bi ki-i pi-i 1{+en}
6.	{lu₂}KU₄.E₂ ša₂ E₂.AN.NA
$	single ruling	
7.	ki-i 15 MA.NA KU₃.BABBAR KU₃.PAD.DU {m}NIG₂.DU DUMU-šu₂ {m}NUMUN--DU
8.	it-ti {m}{d}AMAR.UTU--GAR--MU A-šu₂ ša₂ {m}{d}AMAR.UTU--MU--URI₃
9.	GANBA im-be₂-e#-ma i-šam ŠAM₂-šu₂ gam-ru-tu
$	single ruling	
10.	PAP 15 MA.NA KU₃.BABBAR KU₃.PAD.DU a-di 5 GIN₂ KU₃.BABBAR

@translation unitary en project
@unit 1
@span o 1 - o 6
Tablet of the temple-enterer's prebend, house of Ea-kurbanni (and) cella 
of Ištar of Uruk and Nanaya, (consisting of:) 3 @qū of bread, 3 @kurru of 
first-class beer, good-quality dates, regular @ginû and @guqqû-offerings, 
offerings for the king, offerings for the @kāribu-priest according to 
@?the one?@ temple-enterer of Eanna.

$ single ruling

@unit 2
@span o 7 - o 9
For 15 minas of silver in blocks, Kudurru, son of Zer-ukin, with Marduk-
šakin-šumi, son of Marduk-šum-uṣur, agreed a price and then he (Kudurru) 
bought (the prebend) for its full price.

$ single ruling
@unit 3
@span o 10
The total (is) 15 minas of silver in blocks together with 5 shekels of silver

### A Sumerian composite text in ASCII: Gudea 1 in Interlinear style

&Q000887 = Gudea 1 \[E3/1.1.7.1\]
1.	{d}ba-u2#
#tr.en: For Bau

2.	munus sag9-ga
#tr.en: the good woman

3.	dumu an-na
#tr.en: child of An

4.	nin iri-kug-ga
#tr.en: lady of Iri-kug

5.	nin-a-ni
#tr.en: his lady

6.	gu3-de2-a
#tr.en: Gudea

7.	ensi2
#tr.en: ruler

8.	lagasz{ki}-ke4
#tr.en: of Lagaš

9.	e2 iri-kug-ga-ni
#tr.en: her house in Iri-kug

10.	mu-na-du3
#tr.en: he built.

### Gudea 1 in Parallel style

&Q000887 = Gudea 1 \[E3/1.1.7.1\]
@translation parallel en project

1.	For Bau,
2.	the good woman,
3.	child of An,
4.	lady of Iri-kug,
5.	his lady,
6.	Gudea,
7.	ruler
8.	of Lagaš,
9.	her house in Iri-kug
10.	he built.

### Gudea 1 in Labeled style

&Q000887 = Gudea 1 \[E3/1.1.7.1\]
@translation labeled en project

@label 1 - 5

For Bau, the good woman, child of An, lady of Iri-kug, his lady,

@label 6 - 8

Gudea, ruler of Lagaš,

@label 9 - 10
	
built her house in Iri-kug.

### Gudea 1 in Unitary style

&Q000887 = Gudea 1 \[E3/1.1.7.1\]
@translation unitary en project
@unit 1
@span 1 - 10

For Bau, the good woman, daughter of An, lady of Iri-kug, his
lady, Gudea, ruler of Lagaš built her house in Iri-kug.

18 Dec 2019 osc at oracc dot org

Steve Tinney & Eleanor Robson

Steve Tinney & Eleanor Robson, 'Translations', _Oracc: The Open Richly Annotated Cuneiform Corpus_, Oracc, 2019 \[http://oracc.museum.upenn.edu/doc/help/editinginatf/translations/\]
