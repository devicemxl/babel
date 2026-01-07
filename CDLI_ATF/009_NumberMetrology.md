# Numbers and Metrology in Oracc Corpora

This document describes how to transliterate weights and measures in ATF for Oracc corpora.

## Introduction

Almost all modern writing systems use just ten graphemes — the digits 0–9 — to write numbers with, whether we are counting individual objects, measuring lengths, calculating volumes, or weighing things. However, there are many different notations for numbers in cuneiform, depending on what is being counted, measured, weighed or calculated. If that weren't complicated enough, several of those separate notation systems use the same graphemes with different, context-dependent meanings.

For instance, the U sign 𒌋 has the value 10 when counting individual objects, but is also an area measure (BUR₃) which is 3 (not 10) times larger than the EŠE₃ unit.

-   In Akkadian texts, metrological units are transliterated in capital letters, as logograms, whether they are written explicitly or implicitly (in count-unit graphemes); for instance, `1(BAN₂) 5 SILA₃`. In Sumerian texts, they are transliterated in lower case: `1(ban₂) 20 sila₃`.
    

This example raises a further complicating factor: the fact that in many cuneiform metrological systems, especially those created in the late fourth and early third millennia, the numbers and units are not written separately but as _count-unit graphemes_. Thus in the classic Ur III-OB area system the U sign 𒌋 means "1 BUR₃" and three U signs 𒌍 means "3 BUR₃". (We always transliterate these count-unit signs with the unit in parentheses immediately after the number, like this: `1(BUR₃)` and `3(BUR₃)`.)

For all these reasons, it is essential to be as explicit and as consistent as possible when transliterating, lemmatising, and translating numbers, weights and measures. This document sets out good practice for Oracc projects. It builds on earlier [numbers and metrology documentation for CDLI corpora](../../../help/editinginatf/cdliatf/numbers/index.html "Numbers and Metrology in CDLI Corpora").

## General principles

### Transliteration

The basic principle of transliterating numbers and units — as with all transliteration — is that the transliteration must _unambiguously_ represent the signs on the tablet. A cuneiformist reading your transliteration must be able to tell immediately which wedges the scribe put on the clay, and the ATF processor must be able to parse your text without ambiguity. For instance, a transliteration such as `150` is invalid ATF, as there is no cuneiform sign "150". You must write either `3.20` if the number is in base 60 or `1 ME 50` if the scribe has used number-words as well as numerals.

-   In standard CDLI notation numbers are always qualified; numbers in the system where one is written as a vertical wedge are qualified with disz, as in 1(disz); numbers written with tens and units have their tens qualified with u: 25 is thus transliterated as 2(u) 5(disz), ensuring a one-to-one relationship between graphemes on the tablet and transliteration.
    
-   In the second and first millennia, most numbers most of the time were written with the DIŠ (one) and U (ten) signs, in combinations from 1 to 59 in base 60. When your text uses this sort of notation, you can [transliterate the numerals](../../../help/editinginatf/metrology/metrologicaltables/index.html#numbers "Jump to  in Oracc metrology guidelines") without explicitly stating that they are written with DIŠ and U. In ATF we call these _diš-less numbers_ and they are more fully documented on the [Mathematical Conventions](../../../help/editinginatf/maths/index.html "Mathematical Notations in Oracc corpora") page.
    
    When a number between 1 and 59 is written with the diš-less shorthand it is the exact equivalent of the full writing using separate transliterations of tens and units.
-   Similarly, in most contexts, the unit fractions can simply be transliterated as `1/2, 1/3, 2/3, 5/6` and not `1/2(DIŠ)`, etc. See [below](#Notes "Jump to  on this page") for notes on fractions in particular metrological systems.
    
-   On the Upper Euphrates and in Assyria scribes often wrote six to nine U signs to mean 60-90. You should transliterate these numbers as `6(U) 7(U) 8(U) 9(U)` (because an unqualified transliteration would be ambiguous).
    
-   In metrological systems with notations other than the diš-oriented base-60 system, these must always be specified in the transliteration. For instance, you must write `4(U) 2(AŠ) GUR` and not `42 GUR`.
    
-   Indicate deliberately omitted metrological units with parentheses inside angle brackets, thus: `3 <(KUŠ₃)>` and `4(U) 2(AŠ) <(GUR)>`.
    
-   If the scribe wrote a numeral with the "wrong" number sign then you should explicitly transliterate this too. Compare for instance `5(AŠ) NINDA` (unusual or incorrect writing) and `5 NINDA` (correct writing with DIŠ).
    
-   Abbreviated transliterations such as `1.0.3, 4 SILA₃` and `2.3.1, 25 SAR` are not allowed, and nor are readings such as `BANMIN` for `2(BAN₂)`.
    

There are further notes on specific metrological systems [below](#Notes "Jump to  on this page").

Here is part of an Old Babylonian tabular account transliterated according to Oracc standards in an [ODS spreadsheet](../layouts/) \[../layouts/\]:

![Part of OECT 15, 18, an Old Babylonian tabular account, in ODS-ATF](../../../images/builder/metrol-xlit.png)

Note the differences between diš-less notations in the length system (where missing unit signs are supplied as necessary) and the count-unit graphemes of the volume system.

### Lemmatisation

For general documentation on lemmatisation, see the [Linguistic Annotation](../../../help/lemmatising/primer/index.html "Lemmatisation primer") pages.

-   Numerals and count-unit graphemes are lemmatised as `n`.
    
-   Numbers written syllabically in Akkadian, and as numerals with phonetic complements, should be lemmatised wherever possible.
    
-   Similarly, in narrative contexts in Sumerian number words should be used where possible (where known!), and lemmatized appropriately. For instance, write `diŋir imin-bi` and lemmatize as `imin[seven]` (rather than `7-bi`, lemmatized as `n`).
    
-   Metrological units in Akkadian texts are lemmatised as shown in the [Metrology Tables](../../../help/editinginatf/metrology/metrologicaltables/index.html "Oracc metrology guidelines"), with the SENSE "unit" and the NORM0 in the absolute case if they are written logographically. Syllabically written metrological units should be normalised as any other Akkadian word.
    
-   There are some metrological units whose Akkadian readings are unknown. They should be lemmatised with the logogram as the GW and NORM0, as shown in the [Metrology Tables](../../../help/editinginatf/metrology/metrologicaltables/index.html "Oracc metrology guidelines"). For instance `1 UŠ` is lemmatised as `n; +UŠ[unit]N$`.
    

Here the same Old Babylonian tabular account has been lemmatised:

![Part of OECT 15, 18, an Old Babylonian tabular account, in lemmatised ODS-ATF](../../../images/builder/metrol-lemm.png)

### Translation

For general documentation on translation, see the [Translation](../../../help/editinginatf/translations/index.html "Translations") pages.

-   Translate units into English wherever possible. Recommended translations are given in the [Metrology Tables](../../../help/editinginatf/metrology/metrologicaltables/index.html "Oracc metrology guidelines").
    
-   Try to reflect the structure of the cuneiform notation in translations, rather than converting to decimal values or modern units. The [Metrology Tables](../../../help/editinginatf/metrology/metrologicaltables/index.html "Oracc metrology guidelines") give approximate modern equivalents, which you can show in parentheses afterwards if appropriate. For instance, you might translate `55 NINDA 3 KUŠ₃` by `55 rods, 3 cubits (c.330.25 m)`.
    
-   It's a good idea, though not essential, to reflect the use of count-unit graphemes in your translation too. For instance, you might translate `1(BAN₂) 5.1/2 SILA₃` as `1(@sūtu) 5 1/2 @qû (c.15 litres)`.
    

The same Old Babylonian tabular account translated:

![Part of OECT 15, 18, an Old Babylonian tabular account, in ODS-ATF translation](../../../images/builder/metrol-xlat.png)

## Metrology Tables

[These tables](../../../help/editinginatf/metrology/metrologicaltables/index.html "Oracc metrology guidelines") give the signs, transliterations, lemmatisations, translations and approximate modern equivalents for the major metrological systems of second and first-millennia Babylonia:

### Diš-less numbers

-   [Unit fractions](../../../help/editinginatf/metrology/metrologicaltables/index.html#unit_fractions "Jump to  in Oracc metrology guidelines")
-   [Ones](../../../help/editinginatf/metrology/metrologicaltables/index.html#ones "Jump to  in Oracc metrology guidelines")
-   [Tens](../../../help/editinginatf/metrology/metrologicaltables/index.html#tens "Jump to  in Oracc metrology guidelines")

### Classic Ur III-OB metrologies

-   [Length](../../../help/editinginatf/metrology/metrologicaltables/index.html#length "Jump to  in Oracc metrology guidelines")
-   [Area, volume, and bricks](../../../help/editinginatf/metrology/metrologicaltables/index.html#area "Jump to  in Oracc metrology guidelines")
-   [Capacity](../../../help/editinginatf/metrology/metrologicaltables/index.html#capacity "Jump to  in Oracc metrology guidelines")
-   [Weight](../../../help/editinginatf/metrology/metrologicaltables/index.html#weight "Jump to  in Oracc metrology guidelines")

### Kassite and first-millennium metrologies

-   [_arû_\-measure](../../../help/editinginatf/metrology/metrologicaltables/index.html#aru "Jump to  in Oracc metrology guidelines") for lengths and areas
-   [_arû_ "seed measure"](../../../help/editinginatf/metrology/metrologicaltables/index.html#aru_seed "Jump to  in Oracc metrology guidelines") for areas and capacities
-   [_aslu_\-measure](../../../help/editinginatf/metrology/metrologicaltables/index.html#aslu "Jump to  in Oracc metrology guidelines") for lengths and areas
-   [_aslu_ "seed measure"](../../../help/editinginatf/metrology/metrologicaltables/index.html#aslu_seed "Jump to  in Oracc metrology guidelines") for areas and capacities
-   ["Reed measure"](../../../help/editinginatf/metrology/metrologicaltables/index.html#reed "Jump to  in Oracc metrology guidelines") for small lengths and areas

If you need further metrological units or systems to be documented, please email the Oracc Steering Committee osc at oracc dot org.

## Notes on specific metrological systems

### Ur III-OB systems

-   In the [area-volume-brick system](../../../help/editinginatf/metrology/metrologicaltables/index.html#area "Jump to  in Oracc metrology guidelines"), the sign GANA₂ separates the large-value count-unit graphemes from the lower-value "diš-less" ones. ATF treats GANA₂ as punctuation in this context, so it must be written as `*GANA₂` or `*(GANA₂)` with no translation. For instance: `2(EŠE) *GANA₂ 40 SAR`, translated as `2(@eblu) 40 @mūšaru`. (It is good practice to read the sign GANA₂ as `AŠA₅` when it means "field", to further avoid ambiguity.)
    
-   In the [area-volume-brick](../../../help/editinginatf/metrology/metrologicaltables/index.html#area "Jump to  in Oracc metrology guidelines") and [capacity](../../../help/editinginatf/metrology/metrologicaltables/index.html#capacity "Jump to  in Oracc metrology guidelines") systems respectively, the SAR and SILA are divided into 60 shekels and the shekel into 180 grains, just as in the [weight system](../../../help/editinginatf/metrology/metrologicaltables/index.html#weight "Jump to  in Oracc metrology guidelines").
    
-   In the [area-volume-brick](../../../help/editinginatf/metrology/metrologicaltables/index.html#area "Jump to  in Oracc metrology guidelines"), [capacity](../../../help/editinginatf/metrology/metrologicaltables/index.html#capacity "Jump to  in Oracc metrology guidelines") and [weight](../../../help/editinginatf/metrology/metrologicaltables/index.html#weight "Jump to  in Oracc metrology guidelines") systems, respectively, the base-60 multiples of the BUR₃, GUR and GUN can be represented sexagesimally in translation. For instance, `5(GEŠ₂) 2(U) 5(AŠ) GUR` can be translated as `5.25(@kurru)` and `1(ŠARʾU) 2(BURʾU) 4(BUR₃)` as `1.24(@būru)`.
    

### Post-OB systems

There were several parallel post-OB length-area systems in use, depending on the context of use. ["Reed measure"](../../../help/editinginatf/metrology/metrologicaltables/index.html#reed "Jump to  in Oracc metrology guidelines") was used for small areas such as houses, while two different "Seed measures" — [_arû_](../../../help/editinginatf/metrology/metrologicaltables/index.html#aru "Jump to  in Oracc metrology guidelines") and [_aslu_](../../../help/editinginatf/metrology/metrologicaltables/index.html#aslu "Jump to  in Oracc metrology guidelines") (not to be confused with the _ašlu_ unit)— were used for larger ones such as fields.

-   The Ur III-OB [weight system](../../../help/editinginatf/metrology/metrologicaltables/index.html#weight "Jump to  in Oracc metrology guidelines") continues unchanged into later periods.
    
-   The larger units of the post-OB systems for lengths areas, and capacities are identical to those of the Ur III-OB [length](../../../help/editinginatf/metrology/metrologicaltables/index.html#length "Jump to  in Oracc metrology guidelines") and [area](../../../help/editinginatf/metrology/metrologicaltables/index.html#area "Jump to  in Oracc metrology guidelines") systems and are thus omitted from the [Metrology Tables](../../../help/editinginatf/metrology/metrologicaltables/index.html "Oracc metrology guidelines").
    
-   Note that several relationships between units are different to those of the Ur III-OB systems.
    
-   In area-capacity systems the sign PI separates the large-value count-unit graphemes from the lower-value ones. ATF treats PI as punctuation in this context, so it must be written as `*PI` or `*(PI)`. It is not translated. For instance: `1(AŠ) GUR 2(BARIG) *PI 3(BAN₂)`, translated as `1 @kurru, 2(@pānu), 3(@sūtu)`.
    

18 Dec 2019 osc at oracc dot org

Eleanor Robson

Eleanor Robson, 'Numbers and Metrology in Oracc Corpora', _Oracc: The Open Richly Annotated Cuneiform Corpus_, Oracc, 2019 \[http://oracc.museum.upenn.edu/doc/help/editinginatf/metrology/\]
