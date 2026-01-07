CDLI ATF Primer
===============

If you are preparing texts for insertion directly into the CDLI repository you should read this document first.

ATF in CDLI and Oracc
---------------------

Before learning any ATF it is useful to know a little about the history and current state of ATF. ATF was developed for use in CDLI, and was first defined as a relatively small specification which used only ASCII characters. Over time, two things have happened. Firstly, the range of texts encoded in ATF has grown, and ATF has grown with it. Secondly, ATF has been extended to allow Assyriologists to process legacy data more quickly and to type new texts in a format that is very close to the way things look on screen.

Because of the archival nature of the CDLI repository, we do not allow extended ATF to be used in the repository itself. Texts in Oracc's extended ATF will be converted to the archival core ATF format that we call Canonical ATF (C-ATF). **Although C-ATF does not imitate the print versions of texts, C-ATF can be converted to a pretty-printed version using [this webservice](http://oracc.museum.upenn.edu/doc/wwwhome/util/atfproc.html "Link opens in new window") \[http://oracc.museum.upenn.edu/doc/wwwhome/util/atfproc.html\].**

**If you are typing texts to go directly into the CDLI repository you must follow the instructions in this document so that you create Canonical ATF (C-ATF) directly.**

Oracc Documentation
-------------------

Oracc documentation is generally written using extended ATF; when you are writing C-ATF you need to be careful to adjust the examples appropriately.

C-ATF Main Points
-----------------

*   ASCII Characters only
*   Sign values in Sumerian must conform to the set of CDLI values; See [http://cdli.ucla.edu/downloads.html](http://cdli.ucla.edu/downloads.html "Link opens in new window") \[http://cdli.ucla.edu/downloads.html\] and contact `cdli@cdli.ucla.edu` if you wish to recommend values which are not listed there.
*   readings not assigned indices by Borger, MZL, must be followed by 'x' (the letter lowercase ex) and a description of the sign using sign names in upper case, for instance `sudx(|SU.KUR|)`.
*   Never put brackets inside graphemes: write `ab#` not `[a]b`.
*   For purposes of qualifying state of preservation, both simple and complex signs are considered atoms; thus, a component of a complex sign such as `|UR2x(A.HA)|` is never qualified as damaged or broken, only the whole sign. Similarly, a damaged number notation, for instance `[5(disz)]+4(disz)` must be coded as `9(disz)#`.
*   Never put logograms in capitals: only uninterpreted sign names, and complex signs are in upper case in C-ATF
*   For logograms in non-Sumerian texts use underscores and lower case, i.e., write `%a _lugal_`, not `%a LUGAL`.
*   For logograms where the logogram language is not Sumerian, use a language switch after the underscore: `(%hit ...) _%a mu-u2_`
*   All numbers must be qualified (`3(disz)`, `4(u)` etc.) **except** sexagesimal numbers in Place Value notation (PVN).
*   The only ATF protocols that are allowed in C-ATF are:
    *   `#atf: lang XXX`, where XXX is a language code
    *   `#atf: use math`, where PVN is to be used
*   The `#`\-sign ("hash"-sign) introduces comments about individual line content and always follows the commented line
*   The `$`\-sign introduces comment of text structure, never of line content
*   `$`\-lines for breakage of uncertain length must conform to the following patterns:
    *   `$ broken` (for instances of loss of full surface or column)
    *   `$ beginning broken` (after this, use primes on subsequent line numbers but where the length of the break is known, instead enter all line numbers and use `[...]` for the line content; `beginning broken` may also refer to some unknown number of columns missing, after which the first preserved column is to be qualified `@column 1'` and so on)
    *   `$ rest broken` (see above for both missing lines and columns)
    *   `$ n lines broken` (within column and surface; line numbering after resumption of preserved text is in sequence with the number preceding the break with, for example, `5'.` following either `4.` or `4'.`.)

Examples in C-ATF
-----------------

### Example 1

&P100003 = AAS 015
#atf: lang sux
@tablet
@obverse
1. 1(disz) geme2 u4 1(disz)-sze3
2. ki dingir-ra-ta
3. da-da-ga
4. szu ba-ti
@reverse
1. mu ki-masz{ki} ba-hul

The various ATF features illustrated here are:

The `&-line`

Every text begins with an `&-line` giving the ID and the text's designation according to the CDLI catalog; if your text is not yet in the catalog, e-mail cdli@cdli.ucla.edu to get the ID and designation.

`#atf: lang sux`

You can specify the main language for the text; for Akkadian just write `#atf: lang akk`.

`@tablet`

You can specify an object type; this is normally @tablet, but others include @bulla and @envelope. If an object type which is used in the CDLI catalog is not understood by the ATF processor, you can use the exactly equivalent form `@object OBJECT_TYPE`, e.g., `@object head`.

`@obverse, @reverse`

You can specify the part of the object you are transliterating; the edges are given using: `@left @right @top @bottom` (but note that no physical surface of a tablet is to be included in C-ATF unless it, such as `@left` or in the case of occasional partial sums at the bottom of colums in Ur III administrative texts, assumes an explicit function in text format)

Lines of text

Lines of text are for the most part just like regular Assyriological practice. See [Example 2](#sh_example2 "Jump to  on this page") for how to do breakage.

Determinatives, phonetic complements and glosses

Determinatives are given in curly brackets.

Phonetic complements and glosses are marked with a `+` immediately after the first curly bracket; they are assumed to be in the same language as the rest of the word.

Rulings and Blank Spaces

Lines ruled on the tablet as paragraph separators, as well as empty space or space used for seal impressions, can be marked with $-lines ("dollar-lines").

Numbers

All numbers are qualified.

### Example 2

&P348658 = SpTU 2, 055
#atf: lang akk
@tablet

@obverse
1.	t,up-pi \_a-sza3\_ ki-szub-ba#-\[a ...\]
2.	{i7}har-ri sza2 {d}muati? x \[...\]
3.	ša2 qe2-reb unu#\[{ki}\]

Damage and breakage

There are no half-brackets in ATF: signs which are damaged are flagged with the hash-sign (`#`) after the grapheme.

Signs which are completely broken away are placed in square brackets; square brackets may not occur inside a grapheme, only before or after it. The ellipsis (`...`) may be used to indicate that an undeterminable number of signs is missing.

Signs which cannot be identified are transliterated as `x`; when a number is missing the convention is to use `n` as in `n(disz)`. Both within or after the parentheses further qualification of `n` as `n(disz)` is allowed.

Querying, Correction and Collation

The other flags are the query (`?`) which can be placed after a grapheme to indicate uncertainty of reading; the asterisk (`*`) which indicates a collated reading; and the exclamation mark which indicates correction. After a corrected sign, the actual sign on the tablet may optionally be given, using sign names in upper case: `a!` or `ki!(DI)`.

18 Dec 2019 osc at oracc dot org

Steve Tinney

Steve Tinney, 'CDLI ATF Primer', _Oracc: The Open Richly Annotated Cuneiform Corpus_, Oracc, 2019 \[http://oracc.museum.upenn.edu/doc/help/editinginatf/cdliatf/\]
