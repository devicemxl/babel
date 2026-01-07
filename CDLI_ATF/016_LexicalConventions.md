[Oracc] » [Help] » [Editing in ATF] » Lexical texts

# ATF Lexical Conventions

This page describes the ATF features for working with lexical texts. The original version of this document was written by Madeleine Fitzgerald and Steve Tinney.

## Protocol

Lexical texts are indicated by a special protocol which should be given at the start of each file. This protocol takes the form:

#atf: use lexical

The use of the lexical protocol also automatically enables the `#atf: use mylines` protocol.

## Fields

Columns of lexical texts are treated as fields in the ATF sense, i.e., they are segments of a line which have distinct content. The ATF field-separator `','` is used to separate columns of a lexical text; if the physical alignment of a lexical text is to be mimicked, the ATF column-separator code `'&'` can be used instead.

Fields are marked for their content, whether the column contains a sign, a pronunciation, a translation or other data type. If the column is unmarked, the column contains a word or phrase.

The following are the markers for column types. Note that there are both shorthand and explicit markers. Shorthand markers must be preceded and followed by at least one space or tab character.

| Shorthand | Explicit | Meaning |
| --- | --- | --- |
| #   | ,!sv | column that follows is sign value |
| "   | ,!pr | column that follows is pronunciation |
| ~   | ,!sg | column that follows is sign |
| \|  | ,!sn | column that follows is ancient sign name |
| \=  | ,!eq | column that follows is an equivalent (translation or synonym) |
| ^   | ,!wp | column that follows is a word or phrase; this is the default column type and the `','` may be omitted if it is the first column |
| @   | ,!cs | column that follows gives the contained signs which occur within a container sign |

In addition, a bullet-character may be transliterated at the start of the line using '\*', optionally followed by the grapheme in parenthesis, e.g., `*` or `*(disz)`.

Example:

  1\. !pr e-a ,!sg A ,!eq %a na-a-qu

which may also be entered as:

  1\. " e-a ~ A = %a na-a-qu

This is a three-column text with the first column being the pronunciation, the second being the sign, and the third being the translation, in this case into Akkadian as indicated by the standard [language shift] marker "%a." The first example is the full form with the standard notation for field breaks, `','` followed by the notation for the type of column. The second example above is the same transliteration with shorthand rather than explicit notation. Remember that it is very important to have whitespace on either side of the shorthand markers.

## Examples

### Paleographic Ea

  1\. !sg A

This example shows how to mark up a single column list of sign names.

### Proto-Ea

  1\. !pr e-a ,!sg A

### Proto-Aa

  1\. !pr e-a ,!sg A ,!eq%a mu-u

Here we have a three-column list with pronunciation, sign name, and akkadian translation. Shorthand for the same line of translation would be:

  1\. " e-a : A = %a mu-u

### Unilingual

  1\. !wp a 

or:

  1\. ^ a

Note that because `!wp` is the default field type, this can also be written as:

  1\. a

### Bilingual

  1\. !wp a ,!eq%a mu-u 

In this case we have a two column list with the Sumerian word in the first column and the Akkadian translation in the second. The shorthand version would be

  1\. ^ a = %a mu-u 

or (because an unmarked column is assumed to contain a word or phrase):

  1\. a = %a mu-u

Note again the whitespace on each side of the shorthand markers ^ and = in the last two examples above.

### Trilingual etc.

    1\. !wp a ,!eq%a mu-u ,!eq%h ba-ba
    
    A three-column text with Sumerian, Akkadian, and Hittite, which can also be rendered in shorthand as:
    
    1\. ^ a = %a mu-u = %h ba-ba
    
    or:
    
    1\. a = %a mu-u = %h ba-ba

### Prism with unilingual Sumerian vocabulary excerpt from Hh

    #atf use lexical
    &Pxxxxxx = Hh IX excerpt 44
    @prism
    @face 1
    @column 1
    1. ,!pr a-ab ,!wp ab
    2. ,!pr i-ig ,!wp ig

### Syllabary

    #atf use lexical
    &Pxxxxxx = XX
    @tablet
    @obverse
    1. \* ,!pr du-u ,!sg KAK
    
    or:
    
    1\. \* " du-u : KAK

### Trilingual

    #atf use lexical
    &Pxxxxxx = XX
    @tablet
    @obverse
    1. " tak-tak ~ TAK4.TAK4 | tak min-a-bi = %a e-ze-bu = %h ar-ha da-lu-mar

### Unilingual Proto-Ea

    #atf use lexical
    &Pxxxxxx = XX
    @tablet
    @obverse
    1. " su-un : BUR2
    2. " bu-ur : BUR2
    3. " du-un : BUR2
    4. " u3-szu-um : BUR2

### Bilingual Proto-Ea

    #atf use lexical
    &Pxxxxxx = XX
    @tablet
    @obverse
    1. ,!pr mu-ul  ,!sg MUL ,!eq%a ka-ka-bu
    2. "           ~        =%a szi-t,ir-tu
    3. "           ~        =%a na-pa-hu
    4. "           ~        =%a na-ba-t,u
    5. " szu2-hub2 ~    MUL = %a szu-hu-pu

Remember that `!pr` is equivalent to `"`, not "ditto," and `!sg` is equivalent to `~ ;` .

If you want to indicate that empty space is meant to indicate a repetition of data from a preceding line, you can include the data between <(...)> (intentional omission supplied by editor). The example above would then be rendered as follows:

    #atf use lexical
    &Pxxxxxx = XX
    @tablet
    @obverse
    1. ,!pr mu-ul  ,!sg MUL , !eq %a ka-ka-bu
    2. <(mu-ul)> ~ <(MUL)> = %a szi-t,ir-tu
    3. <(mu-ul)> ~ <(MUL)> = %a na-pa-hu
    4. <(mu-ul)> ~ <(MUL)> = %a na-ba-t,u
    5. " szu2-hub2  ~ MUL = %a szu-hu-pu

### Emesal

    #atf use lexical
    &Pxxxxxx = XX
    @tablet
    @obverse
    1. %e ga-sza-an = %eg nin = %a bel-tu
    2. %e u5-mu = %eg i3-gisz = %a el-lu
    3. %e ze2-eg3 = %eg szum2 = %a na-da-nu

18 Dec 2019 osc at oracc dot org

Steve Tinney

Steve Tinney, 'ATF Lexical Conventions', _Oracc: The Open Richly Annotated Cuneiform Corpus_, Oracc, 2019 \[http://oracc.museum.upenn.edu/doc/help/editinginatf/lexicaltexts/\]
