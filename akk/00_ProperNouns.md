kk[Oracc] » [Help] » [Languages] » Proper nouns

# QPN: Oracc Linguistic Annotation for Proper Nouns

This document provides an overview of annotation conventions for proper nouns used in Oracc. We focus here on the data-entry view of linguistic annotation giving only enough additional technical background to ensure that correct annotation of ATF files can be carried out.

This document assumes knowledge of the introductory page on [Oraccc linguistic annotation].

## Transliteration

-   Proper nouns are transliterated without initial capitals, e.g., `{m}ha-am-mu-ra-bi` not `{d}Ha-am-mu-ra-bi`.
-   The male and female determinatives are {m} and {f} respectively, e.g., `{f}la-ma-as-sa-ni`.
-   Some projects, such as SAAo and CAMS, use double hyphens to mark internal word boundaries with double hyphens in ATF, so that they can be clearly distinguished (e.g., `{d}a-nu--ŠEŠ-šu--DIN` = Anu-ahšu-uballiṭ). However, new projects are encouraged not to use double hyphenation.

## Lemmatization

Most lemmatization of proper nouns follows the conventions of the relevant language; here is a summary of the conventions common to all proper nouns. For further language-specific information, see the pages on [Akkadian], [Aramaic], [Elamite], [Greek], [Old Persian], and [Sumerian].

This page describes explicit lemmatization. See the page on [Linguistic Annotation] for the difference between explicit and POS-only lemmatization of proper nouns.

### CF

-   CFs of proper nouns have initial capitals. For instance `{f}la-ma-as-sa-ni = +Lamassani[]PN$`.
-   Internal word boundaries are marked by single hyphens, with initial capitals for internal proper nouns. Compare `{m}{d}60-EN-šu-nu = +Anu-belšunu[]PN$` and `{m}ri-mut-{d}60 = +Rimut-Anu[]PN$`.
-   CFs of proper nouns **NEVER** use long vowels (i.e., not `Anu-bēlšunu` or `Rīmūt-Anu`).

Partially broken proper nouns should be lemmatised wherever possible, according to the following conventions:

Only illegible signs survive after the determinative (if there is one)

Lemmatise the whole name with CF `X`. For instance, `{m}x = +X[]PN$`.

No signs survive after the determinative

Lemmatise the whole name with CF `X`. For instance, `{m}[...] = +X[]PN$`.

One or more elements are completely missing

Lemmatise the missing elements with X, separated by hyphens. For instance, `{d}EN-[...] = +Bel-X[]PN$` and `x-x-u₂-bal-liṭ = +X-uballiṭ[]PN$`.

One or more elements are only partially preserved

Lemmatise the sign names of the partially preserved elements in capitals, separated by periods. For instance, in `{d}a-nu-$U₂-[...] = +Anu-U₂.X[]PN$` it is possible that the `U₂` might be read `šam` instead of `u₂`.

### GW and SENSE

There are three types of GW for proper nouns:

Modern-language GW

Use this type when your translation uses a modern word instead of the ancient one, e.g., `+Purattu[Euphrates]WN$`.

Numerical GW

Use this type when you need to distinguish between different individuals of the same name, and your translation uses the CF. For instance, `+Nidintu-Anu[01]PN$` is a different person to `+Nidintu-Anu[02]PN$`. Make sure to apply these numerical codings consistently across your corpus, so that it is always the same Nidintu-Anu who is assigned GW `[01]`. This will ensure that the glossary treats them as separate individuals.

Empty GW

Use this type when your translation uses the CF but you do not need or want to distinguish between individuals. For instance `+Ištar[]DN$` does not need a numerical or modern-language GW if she is written "Ištar" in the translation and there is only one deity of that name.

SENSEs are rarely used in lemmatising proper nouns.

### POS and EPOS

POS tags for proper nouns are not language-specific. In the table below, the `Class` column indicates how the different NN types are grouped in glossaries.

|     |     |     |     |
| --- | --- | --- | --- |POS Tags for Proper Nouns
| POS | Meaning | Class | Pseud-lang |
| --- | --- | --- | --- |
| AN  | Agricultural (locus) Name | Places | qpn-x-people |
| CN  | Celestial Name | Celestial | qpn-x-celest |
| DN  | Divine Name | Divine | qpn-x-divine |
| EN  | Ethnos Name | Ethnic | qpn-x-ethnic |
| FN  | Field Name | Places | qpn-x-places |
| GN  | Geographical Name (lands and other geographical entities without their own tag) | Places | qpn-x-places |
| LN  | Line Name (ancestral clan) | People | qpn-x-people |
| MN  | Month Name | Month | qpn-x-months |
| ON  | Object Name | Object | qpn-x-object |
| PN  | Personal Name | People | qpn-x-people |
| QN  | Quarter Name (city area) | Places | qpn-x-places |
| RN  | Royal Name | People | qpn-x-people |
| SN  | Settlement Name | Places | qpn-x-places |
| TN  | Temple Name | Temples | qpn-x-temple |
| WN  | Watercourse Name | Watercourses | qpn-x-waters |
| YN  | Year Name | Year name | qpn-x-ynames |

EPOS is helpful in cases where, for instance, royal names are deified or celestial entities are named after deities. For example:

4\. {mul}GU.LA u {d}ŠUL.GI
#lem: +Gula\[\]DN'CN$; u\[and\]CNJ; +Šulgi\[\]RN'DN$

### NORM0

It is only necessary to add a NORM0 to the lemmatisation if the spelling shows a morphological difference from the CF. For instance, `ak-ka-di-i = +Akkadu[Akkadian]EN$Akkadi`.

## Translation

Ideally, your translation of a proper noun should match _either_ the modern-language GW (see above) _or_ the CF, with short vowels, if the GW is empty or numerical.

18 Dec 2019 osc at oracc dot org

Eleanor Robson & Steve Tinney

Eleanor Robson & Steve Tinney, 'QPN: Oracc Linguistic Annotation for Proper Nouns', _Oracc: The Open Richly Annotated Cuneiform Corpus_, Oracc, 2019 \[http://oracc.museum.upenn.edu/doc/help/languages/propernouns/\]
