[Oracc] » [Help] » [Languages] » [Akkadian] » Akkadian stylesheet

# Akkadian Stylesheet

There are many valid ways to transliterate Akkadian in ATF, but the more similarly people transliterate texts for Oracc, the better the corpora will work together. This document sets out Oracc's recommended transliteration conventions for Akkadian.

## Syllabic signs

ATF determines only that syllabic signs be written in lower case, and separated by hyphens. The choice of sign values is constrained by the Oracc Global Sign List, which is essentially the sign values given in Borger, _Mesopotamisches Zeichenlexikon_ (MZL), 2003. Oracc corpora use the following conventions:

-   although the ATF checker recognises acute and grave accents in legacy data (pre-existing material converted to ATF format), their use is deprecated in the creation of new ATF. Subscript ₂ and ₃ are strongly recommended instead (but note that the HTML versions of ATF texts can be displayed using acutes and graves, however the diacritics are marked in the ATF);
-   first-millennium corpora, such as [CAMS] \[http://oracc.museum.upenn.edu/cams/\], generally avoid mimation (e.g., tu₄, not tum), unless this entails using very rare values of a sign, or it's otherwise apparent that mimation is prevalent in the text;
-   similarly, we do not hyper-correct case endings, so that for instance in accusative feminine nouns final UD is read as tu₂, not ta₅ (e.g., na-piš-tu₂, not na-piš-ta₅);
-   although ʾ alone is a valid value, for reasons of legibility ʾa and, where appropriate, aʾ are preferred.
-   as required by ATF, sign values that are not in Borger's _MZL_ are written with subscript ₓ and the sign name (e.g., sutₓ(BAN₂) ).

## Logograms

Logograms are written in capitals, of course, and separated internally by dots (e.g., GIR₂.TAB).

-   Vowel-final values of logograms are normally preferred to consonant final values (e.g., U₄ rather than UD), unless this entails using very rare values of the sign;
-   logographic suffixes (which indicate Akkadian morphology, such as plurality, or suffixes) are separated from the logogram itself with a hyphen (e.g., U₄-ME, E₂-BI, 3-TA.AM₃). Further examples: \-A.NI, \-E.NE, \-HI.A, \-KAM, \-KAM₂, \-MEŠ, \-MIN.

It is not always clear in **Old Babylonian texts** whether one is dealing with logograms or genuine Sumerian. A useful rule of thumb is that the presence of syllabically written Akkadian words suggests that the whole text is in Akkadian. However, year names are best treated as 'real' Sumerian, even in otherwise Akkadian texts. If in doubt, consult your OSC liaison, who will be happy to help. There is a separate documentation page on how to mark [language (and dialect) shifts] in ATF.

## Determinatives

In ATF determinatives are written lower-case in curly brackets (e.g., {d}IŠKUR, sip-par{ki}). Determinatives specify the semantic set to which a noun belongs, and therefore exclude instances such as plural markers. Note that the _Concise Dictionary of Akkadian_ treats determinatives as logograms. So, for instance, where _CDA_ writes, e.g., Ú.GÍR.HAB, CAMS writes {u₂}GIR₂.HAB.

-   Oracc corpora use {iti}NE etc. for month names, not ITI NE ;
-   we use {tu₁₅}MAR.TU etc. for winds and directions, not {im}MAR.TU;
-   {m} and {f} are used for male and female and PNs, such as {m}na-di-nu {f}tab-luṭ
-   but {lu₂} and {munus} mark male and female professions such as {lu₂}UŠ₁₁.DU = kaššāpu and {munus}UŠ₁₁.DU = kaššaptu;
-   and note {iri} (not {uru}).

Sometimes it is not immediately obvious if a sign should be treated as a standalone logogram or as a determinative. As a general rule of thumb, if you wouldn't lemmatise it as a word, treat it as a determinative.

## Phonetic complements

Phonetic complements are preceded by a + inside curly brackets (e.g., KUR{+ud} = ikšud). We distinguish them from suffixes, which are written as lower-case syllabic signs, separated from the logogram with a hyphen (e.g., KUR{+ud}-an-ni = ikšudanni).

Thus abstract endings on logograms are treated as phonetic complements (e.g., LUGAL{+u-tu₂}),, not suffixes, because šarru and šarrūtu are different words.

## Proper nouns

It is Oracc-wide style that proper nouns are always lemmatised and translated with short vowels throughout. Note that initial capitals are not used in transliteration, only in lemmatisation and normalisation.

Following the practice of the State Archives of Assyria project, inside Akkadian proper nouns CAMS marks internal word boundaries with double hyphens in ATF, so that they can be clearly distinguished (e.g., {d}a-nu--ŠEŠ-šu--DIN = Anu-ahšu-uballiṭ). However, new projects are encouraged not to use double hyphenation.

## Numbers

Transliterate numbers as they are written—do not convert them into modern decimal notation. It is always important to note whether the scribe has written "a hundred" as, say 1 ME or 1 ŠU 40. Always note which sign has been used to write the numeral unless the writing is in purely sexagesimal notation.

-   We treat syllabic suffixes on numerals as phonetic complements (e.g., 1{+en} = ištēn) and lemmatise them as number words, not as numerals;
-   we group the constituent parts of a sexagesimal number with full stops, so that it is lemmatised as a single number (e.g., 1.40 is one number but 1 40 is two numbers). This is essentially a shorthand for the more explicit notation 1(DIŠ).4(U) used in other contexts (for more details see the page on [mathematical notations] \[../../../ATF/math.html\] in ATF).
-   we transliterate numerical divine names as {d}60, {d}30 etc., but lemmatise as the god's name: Anu, Sin, etc.;
-   and note 15 = imittu and 2.30 (not 150) = šumēlu.

## Reporting errors in the CAMS glossaries

Many projects use CAMS as their base glossary. Although we try to keep CAMS as consistent and error-free as possible, its size and diversity mean that is impossible to have complete control over it. You will almost certainly find inadvertent exceptions to this stylesheet in the CAMS glossaries. We welcome notifications of such errors to osc at oracc dot org. We will then endeavour to correct or document them as soon as possible.

18 Dec 2019 osc at oracc dot org

Eleanor Robson

Eleanor Robson, 'Akkadian Stylesheet', _Oracc: The Open Richly Annotated Cuneiform Corpus_, Oracc, 2019 \[http://oracc.museum.upenn.edu/doc/help/languages/akkadian/akkadianstylesheet/\]
