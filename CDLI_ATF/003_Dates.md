Date Specifications for CDLI/Oracc
==================================

This document describes the conventions used for specifying dates in the CDLI catalogs and gives a list of kings and dynasties. This list is a work-in-progress; e-mail corrections to Steve Tinney at stinney at upenn dot edu.

Scheme
------

The general scheme of dates is a sequence of up to five members giving the following data:

\[DYNASTY/ERA\] . \[RULER\] . \[YEAR\] . \[MONTH\] . \[DAY\]

The actual syntax of a single date specification gives an instance of each of these members with the members separated by periods:

Ur III.Shulgi.23.04.5

The form of each member is described in the following below.

### Dynasties

A dynasty is specified using the basic combination:

\[CITY\] \[NUMBER\]

This specification is deliberately open-ended since new finds will inevitably require additional dynasty designations. Actual examples include:

Lagash I
Agade
Lagash II
Ur III
Isin I
Larsa
Babylon I
Mari

In transcriptions of city and ruler names /sh/ is used for /shin/.

### Eras

The Seleucid Era is indicated by the prefix `SE`. \[more needed here\]

### Rulers

Rulers are specified by giving the normal form of their name in transcription rather than transliteration and are normalized following Brinkman's list in _Ancient Mesopotamia_, if they occur in that list. Rulers must be unique within their dynasty, appending the conventional 'I', 'II' etc., as required. A provisional list of dynasties and rulers follows.

### Years

Years are given using the lettering or numbering system appropriate to the dynasty/ruler in question. For years which correspond to year-names the canonical equivalency of year-name to year-number is given below.

Where years are named by symbols other than year-names, such as limmu-officials, the year may be given as the number in the reign of the ruler, the symbol, or both. The syntax of this is:

\[YEAR\]? =? \[SYMBOL\]?

Where either part is optional and the equals-sign may be omitted if both parts are not given. If `[SYMBOL]` could be confused with a year letter or number, the equals-sign must be given.

In the following examples, (1) shows how to indicate a date according to a year named after a limmu at Tuttul where the year of the ruler's reign which corresponds to the limmu is unknown. Example (2) shows how to do the same when the year of the ruler is known:

(1)  Tuttul.Yasmah-Addu.3=Ibni-Adad.06.09
(2)  Tuttul.Yasmah-Addu.Ibni-Adad.06.09

### Months

Months consist of one or two parts:

\[CALENDAR\] \[NUMBER|NAME\]

or

\[NUMBER|NAME\]

The optional `CALENDAR` portion consists of a city name or other code which identifies the date's calendar if that calendar is not the standard Mesopotamian calendar.

The `NUMBER|NAME` portion consists of either a month number given as a pair of arabic numerals or the transcription of a month name; the latter convention should only be used for months whose position in a given calendar is uncertain.

### Days

Days are given as a pair of arabic numerals.

### Hyphen

Unspecified components of the date are given with double zero ('00'); components which are broken are given with double hyphen ('--'):

Ur III.00.00.4.25 (no year name given)

Ur III.--.--.4.25 (year name broken)

18 Dec 2019 osc at oracc dot org

Steve Tinney

Steve Tinney, 'Date Specifications for CDLI/Oracc', _Oracc: The Open Richly Annotated Cuneiform Corpus_, Oracc, 2019 \[http://oracc.museum.upenn.edu/doc/help/editinginatf/cdliatf/dates/\]
