[Oracc] » [Help] » [Languages] » Akkadian

# AKK: Oracc Linguistic Annotation for Akkadian

This document provides an overview of language-specific annotation conventions for Akkadian used in Oracc. We focus here on the data-entry view of linguistic annotation giving only enough additional technical background to ensure that correct annotation of ATF files can be carried out. This document assumes knowledge of the introductory page on Oraccc linguistic annotation.

## General principles

If you haven't done so already, start by reading some or all of the page on [Oracc Linguistic Annotation] page.

Lemmatisations take one of two forms:

-   **short:** `NORM0[SENSE]POS` if the lemmatisation is already fully known by the system (e.g. `kalbi[dog]N`).
    
-   **long:** `+CF[GW//SENSE]POS'EPOS$NORM0` if the lemmatisation contains any new information (e.g. `+kalbu[dog]N$kalbika`).
    

The main thing to remember is that you are not lemmatising for other people but for the computer, and that the computer has no intuition. Inconsistencies produce duplicate entries in the glossaries, which are fiddly and time-consuming to fix.

After establishing some general principles, we describe in more detail how to manage the different components of the lemmatisation entry. At the end we show you how to deal with compound orthographic forms (crasis and logograms which straightforwardly resolve into two or more Akadian words), phrasal semanitic units (multi-word idioms), and proper nouns.

## Transliteration Stylesheet

Unless your project is primarily working with legacy data, you should follow the [Oracc stylesheet for Akkadian transliteration]. This will save you a lot of work by enabling your project to use a related, more mature project's glossaries as the starting point for your lemmatisation, such as [CAMS] \[http://oracc.museum.upenn.edu/cams/gkab/\]. But this will only work optimally if you use these same spelling and ATF formatting conventions.

## Good work habits

-   Run the checker and lemmatiser every line or so, for maximum efficiency.
    
-   When you have finished editing a text, run the Harvest Notices tool on the ATF menu. This will list all the long-form lemmatisations you have added, enabling you to check them again.
    

Check automatically entered lemmatisations for:

-   correct normalisation;
    
-   correct sense.
    

If you need to change either of them, use the long form of lemmatisation.

Sometimes the lemmatiser will make several suggestions for alternative lemmatisations, like this: `pān[front]N|immar[see]V|innamir[appear]V|igi[reciprocal]N` for the transliteration `IGI`. Just delete all but the relevant lemmatisation (making sure you delete all the `|`'s too).

When adding new lemmatisations check whether the word already exists in the online glossary for your project:

-   If it is already in the glossary, with a different spelling or sense (but check you have not mistyped the transliteration!) use the same CF and GW in the long form, adding new normalisation and sense as necessary.
    
-   If it is not yet in the glossary, add it with the the long form of lemmatisation.
    

## Citation Forms (CF)

We call the "dialect" of CFs "Conventional Akkadian" (CA) because it does not consistently represent any actually attested variety of the language. It is essential to follow the _Concise Dictionary of Akkadian_ for CFs, even when it differs from CAD. This is important for inter-project compatibility and the ePAD.

However, there are some small but consistent ways in which Conventional Akkadian diverges from CDA's conventions:

-   There is no mimation in CFs (but of course you can give mimation in NORM0s).
    
-   All verbal adjectives and participles have independent CFs even if they are not listed separately in CDA.
    
-   Conventional Akkadian ignores the parentheses in CDA CFs but keeps their contents, e.g., CDA _a(p)puttum_ becomes CA `+apputtu[difficult situation]N$`.
    
-   Where CDA has alternatives marked with a slash (/), choose the first, e.g., CDA _anḫullû/u?_ becomes CA `+anhullû[(a plant?)]N$`.
    

## Guide Words (GW) and Senses

Generally, we use the first translation in CDA as the GW. So when there are alternatives separated by commas, we use the first one, e.g., CDA's _adirtu_, "fear, apprehension" becomes `+adirtu[fear]N`.

Exceptions include:

-   GWs from volumes of CAD that are more recent than CDA (but the CDA citation form must still be used).
    
-   Two exceptions (simply because they are so deeply embedded in the glossaries that they are too labour intensive to change now): `ālu[city]N` not "village"; and `libbu[interior]N` not "inner body".
    
-   If the lemma is a substantivised adjective and CDA gives an adjectival translation, e.g. _qardu_ (CDA "valiant", give a generalised nominal meaning as GW, e.g., `+qardu[valiant one]N$`. If CDA gives a nominal meaning, e.g., "hero", then use that one.
    
-   For uncertain meanings use ? after GW, e.g., `+karmittu[butterfly?]N$`, but don't use initial ~ as CDA does.
    
-   For generic meanings use parenthesised GWs, e.g. \[(a tree)\].
    
-   For unknown meanings also use parentheses, e.g. \[(meaning unknown)\].
    
-   Do not use @ to indicate Akkadian in GWs.
    
-   The GW or sense for all weights and measures is \[unit\], e.g., `+biltu[load//unit]N'N$bilat`.
    
-   If a CDA entry has no overall GW, but a different GW for each numbered part of the entry, use the first as GW and then choose whichever is most appropriate as the sense.
    
-   Keep the GW as short as possible, e.g., avoid the definite article. Don't use "to" in the GWs of verbs.
    
-   But expand abbreviations, e.g., CDA "s.o." becomes `someone`, "s.th." becomes `something`, and "o.s." becomes `oneself`.
    
-   For state verbs use the convention \[be(come) something\] rather than \[be something\], e.g., CDA _adāru,_ "be dark, gloomy" becomes `+adāru[be(come) dark]V$īdur`.
    

If you want to add a local meaning (sense), follow the GW with // and then the sense, e.g. `+hiāṭu[supervise//survey]V'V$hīṭma`. List a sense only when there is significant variation from the GW. For a verb with a G stem GW, list the meaning of another verbal stem as a subsense only if there is significant variation in meaning, e.g., do not list an N stem passive meaning as a subsense if it is a simple passive form of the G stem active GW.

## Parts of Speech (POS and EPOS)

Whenever you add a SENSE you also need to specificy a new, locally valid POS for a word, even if it is the same as that for the GW. We call this an EPOS (Effective Part of Speech) and mark it immediately after the POS, like this: `+kī[like//when]PRP'SBJ$`.

Here are some useful rules about POS and EPOS:

-   Infinitives are nouns. Classify them as V'N, with gerund sense, e.g., `+qabû[say//saying]V'N$`.
    
-   [Statives are a form of verbal adjective.] \[http://oracc.museum.upenn.edu/saao/knpp/cuneiformrevealed/akkadianlanguage/possessionandexistence/#statives\] Classify them as AJ (with no EPOS), e.g., `+šaṭru[written]AJ$šaṭirma`.
    
-   Classify verbal adjectives and participles as AJ (with no EPOS) when they modify a noun, e.g., `+šaṭru[written]AJ$šaṭrūti`.
    
-   Classify verbal adjectives and participles as N (with no EPOS) when used as substantives, e.g., e.g., `+qardu[valiant one]N$`.
    
-   Classify substantives as N when used in stative.
    

Other important points to note:

-   _šū_ etc. are IPs not DPs, although they can have a demonstrative sense.
    
-   Most of the pronouns can also be used to modify a noun, but remain pronouns in our conventions.
    
-   Be careful not to mark adjectives as nouns.
    
-   Similarly, distinguish nouns from prepositions: in prepositional phrases such as _ina muhhi_, _muhhu_ is a noun.
    
-   But reanalyse N as PRP (i.e., as N'PRP) when the PRP is omitted from phrases such as _ina mahar_. Compare, for instance, `ina[in]PRP; mahar[front]N; ili[god]N` with `mahar[before]'PRP ili[god]N`.
    
-   You can use POS and EPOS in proper nouns too, where appropriate, e.g., `{mul}DA.MU = +Damu[]DN'CN$`.
    

## Normalisations (NORM0)

-   Do not use secondary length. Maintain final vowel length as if no suffix were present (includes possessive suffixes and -ma).
    
-   \-ma is not hyphenated in normalisations, e.g., `+šaṭru[written]AJ$šaṭirma`.
    
-   For words with non-standard morphology, normalise what is written, e.g. tuš-za-zi = tušzazi not tušzaz. Mark vowel length where appropriate. Don't try to guess what the scribe "meant" to write.
    
-   If in doubt over i/e choose i.
    
-   Write the first person gen. possessive suffix as _iya,_ not _ia,_ e.g., `+bēlu[lord]N$bēliya`.
    
-   For _pû_ "mouth" normalise construct state _pî_ and suffixed form _pîšu_ etc.
    
-   \* I-w verbs in preterite and precative have long first vowel, unless shown to be short by syncope, e.g., _ūbil_ but _ubla_.
    

## Difficult words

It's not always possible to fully lemmatise every word in a text.

-   For numbers, only lemmatise writings that start syllabically or have a phonetic complement (e.g. `2{+u} = +šanû[two]NU$`; otherwise leave them as `n`. Note that the POS for both cardinal and ordinal numbers is NU.
    
-   If you can identify a word's citation form then you should also try to normalise it too.
    
-   Don't bother trying to lemmatise partially preserved words which you cannot restore, such as `tu-ša-[...]`. The lemmatiser will class them as unlemmatisable by default; don't try to override this.
    
-   Sometimes, especially in very technical contexts such as mathematical astronomy, the meaning of a logogram is known but its Akkadian reading is not. For instance, BAR (Akkadian reading unknown) can mean "lunar velocity". In such cases the logogram becomes the citation form: `+BAR[(lunar velocity)]N$`.
    
-   However, if you can identify the word but don't know what it means, you can lemmatise like this: `+šahû[(meaning unknown)]V$ištahhi`.
    
-   Sometimes, especially in highly technical contexts, it is desirable to gloss GWs with further explanation. This is done in the context of [glossary management].
    

## Marking sentences

Insert `+.` in the lemmatisation line to mark sentences, not clauses – that is, wherever you judge the translation needs a full stop. A good rule of thumb is that `+.` follows indicative verbs that lack the _\-ma_ suffix. Its primary aim is to allow for transliteration-translation sentence-alignment in due course. It is not necessary (or perhaps is pointless to try and add it) in fragmentary texts. It is preceded and (unless at the end of a line) followed by white space.

## Compound Orthographic Forms (COF)

COFs are forms that are written as one word but in fact should be understood as more than one lemma. Their meanings are transparent and they do not justify a separate entry in the glossary.

-   Link two crasis words in Akkadian by `&` (no white space or semi-colon), e.g., `ip-pan = ina[in]PRP&pān[front]N`, "in front of".
    
-   Compound logograms should be treated in the same way: e.g., `BAR.RA.NA = +ina[in//on]PRP'PRP$&+ahu[arm//side]N'N$ahišu`, "on his side".
    

## Phrasal Semantic Units (PSU)

A PSU is a multi-word idiom, whose meaning cannot be inferred from the lemmatisation of its component parts. Each PSU needs its own, manually entered glossary entry. We try to keep PSUs to a minimum.

-   If it's written logographically, treat the logogram as a single word and lemmatise the Akkadian words individually with an ampersand in between: `EME.UR.GI₇ = +lišānu[tongue]N$lišān&+kalbu[dog]N$kalbi`.
    
-   If it's written two (or more) Akkadian words, transliterate and lemmatise them separately, as normal words.
    
-   Either way, write a comment line underneath: `# psu: lišān kalbi [hound's-tongue] N` so that it can be added into the glossary manually. You only need to so this if the PSU or its spelling is new.
    
-   Don't use senses in PSUs – they're not needed and can seriously complicate the process of adding them to the glossaries.
    
-   Some phrases can be idiomatic or non-idiomatic, depending on the context. Use `!` before the first lemma of a PSU to show that it is NOT a PSU in this instance. For instance, if `ana[to]PRP; ṭarsi[extent]N` is in your glossary with the meaning "opposite", write `!ana[to]PRP; ṭarsi[extent]N` when you want this phrase to keep its literal meaning, "to an extent".
    
-   Use - before a lemma to omit a word (usually a MOD or AV) from the middle of a PSU, e.g., `libbašu[interior]N; -ul[not]MOD; iṭâb[be(come) good]V` for `libba ṭiābu [be(come) satisfied] V`.
    
-   Specify the sense of an idiom, in the GW of the first Akkadian element, like this: `ŠA₃.HUL = +lumnu[evil+=eclipsed state]N$lumun&+libbu[interior]N$libbi,` where _lumun libbi_ has the GW "sorrow" but in some (mostly astronomical) contexts means "eclipsed state".
    
-   You can use PSUs for proper nouns too. However, as we have said, it's a good idea to keep their use to a minimum, as they are fiddly to implement.
    

## Proper Nouns

-   In lemmatisation and translation proper nouns have an initial capital (also for any internal instance of a proper noun) and are hyphenated at any internal word boundary, e.g., `ri-hat-{d}60 = +Rihat-Anu[]PN$`.
    
-   The CF used in lemmatisation and the form used in translation should match. If you want to use a modern equivalent in the translation, this should be your GW, e.g., `+Purattu[Euphrates]WN`$.
    
-   In lemmatisation and translation, DO NOT mark long vowels in proper nouns.
    
-   If the writing of a proper noun displays a case ending, then in lemmatisation give the appropriate declined form as the NORM0. Otherwise don't try to guess the NORM0, and leave it to match the CF. Note that Anu(m) is not declined: several instances of the writing {d}a-nu-um follow _ša_.
    
-   In lemmatisation and translation of Sumerian names, use single rather than reduplicated consonants, e.g., Ezida not Ezidda.
    
-   Use divine numbers in transliteration and the name in lemmatisation and translation, e.g., `ri-hat-{d}60 = +Rihat-Anu[]PN$`.
    
-   If a god is an 'anthropomorphic' being, heavenly body, or mythical location, lemmatise as DN (or DN'GN if appropriate, e.g., Apsu) with CF in the absolute state if used, e.g., `+Nisaba[]DN$; +Bel[]DN$`.
    
-   Otherwise, even if written with {d}, lemmatise as a common noun with CF in the nominative singular if used, e.g., `nissabu[grain]N; bēlu[lord]N`.
    

See the page on [Linguistic Annotation of Proper Nouns] for more information.

## POS Tags

The following lists of pronouns and function words are exemplary rather than exhaustive; the POS categorizations are based on W. von Soden, _Grundriss der akkadischen Grammatik_, 3rd edition (Analecta Orientalia 33). Biblical Institute Press, 1995.

|     |     |
| --- | --- |BASIC WORD CLASSES
| AJ  | adjective (including statives) |
| AV  | adverb |
| N   | noun (including statives) |
| NU  | number |
| V   | verb (including infinitives, marked with EPOS 'N and gerundive GW) |

Adverbs include temporal adverbs (e.g., inanna\[now\], anumma\[now//herewith\], šattišam\[yearly\]), interrogative adverbs (e.g., ali\[where?\], ammīni\[why?\], kī\[how?\], mati\[when?\]), and demonstrative adverbs (e.g., kīam\[thus\]).

|     |     |     |     |
| --- | --- | --- | --- |PRONOUNS
| DP  | demonstrative pronoun |
|     | annû\[this\] |
|     | ullû\[that\] |
| IP  | independent/anaphoric pronoun |
|     | nom. | acc./gen. | dat. |
|     | anāku\[I\] | yâti\[me\] | yâšim\[to me\] |
|     | attā\[you\] | kâta\[you\] | kâšim\[to you\] |
|     | attī\[you\] |
|     | šū\[he//it\] | šuāti\[him//it\] | šuāšim\[to him//to it\] |
|     | šī\[she//it\] | šiāti\[her//it\] | šiāšim\[to her//to it\] |
|     | nīnu\[we\] | niāti\[us\] | niāšim\[to us\] |
|     | attunu\[you\] | kunūti\[you\] | kunūšim\[to you\] |
|     | attina\[you\] | kināti\[you\] | kināšim\[to you\] |
|     | šunu\[they\] | šunūti\[them\] | šunūšim\[to them\] |
|     | šina\[they\] | šināti\[them\] | šināšim\[to them\] |
| PP  | possessive pronoun |
|     | yû\[mine\] |
|     | kû\[yours\] |
|     | šû\[his//hers//its\] |
|     | nû\[ours\] |
|     | kunû\[yours\] |
|     | šunû\[theirs\] |
| QP  | interrogative pronoun |
|     | ayyû\[which?\] |
|     | mīnu\[what?\] |
|     | mannu\[who?\] |
| RP  | reflexive/reciprocal pronoun |
|     | ramānu\[self//own\] |
|     | ahāmiš\[one another\] |
| XP  | indefinite pronoun |
|     | ayyumma\[whoever//whichever\] |
|     | mamman\[someone//anyone\] |
|     | mimma\[something//anything\] |
| REL | relative pronoun |
|     | ša\[that\] |
|     | šūt\[that\] |
|     | šīt\[that\] |
|     | mala\[as much as\] |
|     | mimmû\[all that\] |
| DET | determinative pronoun |
|     | ša\[of\] |
|     | šūt\[of\] |
|     | šīt\[of\] |

|     |     |
| --- | --- |OTHER PARTS OF SPEECH
| CNJ | conjunction |
|     | lū\[either\] |
|     | u\[and\] |
|     | ū\[or\] |
| J   | interjection |
|     | anna\[yes\] |
|     | ai\[alas\] |
|     | ullu\[no\] |
| MOD | modal, negative, or conditional particle |
|     | ai\[not\] |
|     | lā\[not\] |
|     | lu\[either\] |
|     | lū\[indeed\] |
|     | lū\[may\] |
|     | šumma\[if\] |
|     | ul\[not\] |
| PRP | preposition |
|     | adi\[until\] |
|     | ana\[at//to\] |
|     | aššu\[about\] |
|     | balu\[without\] |
|     | eli\[on//over\] |
|     | ina\[in//from\] |
|     | ištu\[from\] |
|     | itti\[with\] |
|     | kī\[like\] |
|     | kīma\[like//instead of\] |
|     | lāma\[before\] |
|     | mala\[as much as\] |
|     | qadu\[with\] |
| SBJ | subjunction |
|     | adi\[until\] |
|     | ašar\[where\] |
|     | aššu\[because\] |
|     | ēma\[wherever//whenever\] |
|     | inūma\[when\] |
|     | ištu\[since\] |
|     | kī\[when\] |
|     | kīma\[as\] |
|     | lāma\[before\] |
|     | warka\[after\] |

## Roots

If you want to assign [roots] to Akkadian content words (nouns, adjectives, verbs and adverbs), you must do this in your project's Akkadian glossary (the `akk.glo` file). See the [Projects and Emacs] page for more information.

There is a list of Akkadian roots on a [separate page].

## Dialects

You must always explicitly mark the dialects of Akkadian used in your texts. You may also wish to use dialect forms as the headwords of your glossary.

-   For texts that are entirely in a single dialect, add that information to the language declaration protocol at the top of the file. For instance, for a Neo-Assyrian text you would type:
    
    #atf: lang akk-x-neoass
    
    The dialect codes are given in the [Languages section of the GDL tutorial].
    
-   You can mark dialect-switching in the middle of a text too (as, for instance, when Neo-Assrian letter writers quote Standard Babylonian works). To do this, write the short, inline form of the dialect code in the transliteration line before each dialect-switch. Almost all of them are self-explanatory: `%na` for Neo-Assyrian, `%ob` for Old Babylonian; they are all listed in the [Languages section of the GDL tutorial].
    
    For instance, here a scholar quotes a two-line omen in Standard Babylonian (`%sb`), then comments on it in Neo-Assyrian )`%na`) with an occasional Neo-Babylonian (`%nb`) word:
    
        &P336511 = SAA 08, 051
        
        #atf: lang akk-x-neoass
        #project: saao/saa08
        #atf: use unicode
        
        @tablet
        @reverse
        1. %sb \[\*\] {mul#}.dil-bat AGA GI₆  ap-\[rat MI₂.(PEŠ₂)-MEŠ\] 
            ; a-gu-u ṣa-al-mu
        2. %sb \[NITA\]-MEŠ#  U₃.TU-MEŠ# ; u₂-la-a-\[da\]
        $ single ruling
        3. {mul}UDU.IDIM %nb it-ti %na {mul}\[dil-bat GUB-ma\]
    
    In the first two lines of this example, the dialect switching always runs to the end of the line, so there is no need to explicitly switch back.
    
-   Dialect CFs can be added by hand to the glossary; see the [Projects and Emacs] page for more information.

18 Dec 2019 osc at oracc dot org

Eleanor Robson
