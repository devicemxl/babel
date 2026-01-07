# ATF Quick Reference

A quick reference sheet for the ATF format.

## Structure Conventions

See the [Structure Tutorial](../../../help/editinginatf/primer/structuretutorial/index.html "ATF Structure Tutorial") for more details.

|     |     |
| --- | --- |
| &   | Text/catalogue number designator |
| @<type> | @composite (for composite texts) |
| @<object> | Object = @tablet, @envelope, @prism, @object <object-type> |
| @<surface> | Surface = @obverse, @reverse, @surface, @edge, @left, @right, @top, @bottom, @face \[a..z\] |
| @seal <n> | for transliteration of seal impressions on objects; n=number |
| @column | column |
| <number>. | line of text |
| <number>.<subcases>. | line of text with subdivision into cases |
| $ <qualification> <extent> <scope> <state> | non-text, such as breakage, blank lines, etc.  <br>qualification = at least, at most, about  <br>number = NUMBER, RANGE, n, several, some, start of, beginning of, middle of, end of, rest of  <br>scope = [OBJECT](#object "Jump to  on this page"), [SURFACE](#surface "Jump to  on this page"), case(s), column(s), line(s), surface  <br>state = blank, broken, damaged, effaced, illegible, missing, traces |
| $ <multiple> ruling | horizontal ruling(s) in the text  <br>multiple = single, double, triple |
| $ (image N = <text>) | location of inline image, such as a seal impression or a diagram |
| #   | comment line |
| \=: | multiplexing comment line giving original order of interpreted/reordered signs in preceding line of transliteration. |
| <whitespace> | continues previous line (modern convenience, not ancient line break) |

## Inline ASCII Conventions

See the [ATF Inline Tutorial](../../../help/editinginatf/primer/inlinetutorial/index.html "ATF Inline Tutorial") for more details.

|     |     |
| --- | --- |
| \[A-ZṢŠṬ\]\[a-zṣšṭ\]\[₀-₉\] | grapheme name |
| <hyphen> | joiner for graphemes of single word |
| <space> | word separator |
| !   | flags correction of sign |
| ?   | flags uncertainty of identification or reading |
| \*  | flags collation |
| #   | flags damage to sign |
| \[...\] | encloses material broken away from object |
| \[(...)\] | encloses material perhaps broken away from object |
| value(SIGN) | explanatory name or variant form after value |
| value!(SIGN) | actual signs on object given after corrected version |
| <...> | accidental omission supplied by editor |
| <(...)> | intentional omission supplied by editor |
| MIN<(...)> | surrogate text supplied by editor |
| <<...>> | material removed by editor |
| {...} | determinative delimiters (written in normal script) |
| {{...}} | gloss delimiters |
| $   | following sign is not a logogram |
| x   | unclear sign |
| X   | clear sign not yet identified |
| \|...\| | compound grapheme delimiters |
| \[.x%&+()\] | compound grapheme operators (see QR.3 below) |
| \[āēīū\], \[âêîû\] | long vowels in normalized Akkadian |
| %\[sahrux\] | language shift |
| %e,%u,%g,%n | register/writing system shift |

## Compound Grapheme Conventions

See the [ATF Inline Tutorial](../../../help/editinginatf/primer/inlinetutorial/index.html#Compound "Jump to  in ATF Inline Tutorial") for full documentation of these conventions.

|     |     |
| --- | --- |
| .   | juxtaposed signs, e.g., DU.DU<br><br>![du](../../../images/builder/du.png)<br><br>![du](../../../images/builder/du.png) |
| ×   | following sign(s) written over/within preceding sign, e.g., GA₂×AN<br><br>![ga2-times-an](../../../images/builder/ga2-times-an.png) |
| &   | signs are written one above the other, e.g., DU&DU<br><br>![du-over-du](../../../images/builder/du-over-du.png)<br><br>as opposed to standard DU<br><br>![du](../../../images/builder/du.png) |
| +   | signs are ligatured, e.g., \|LAGAB+LAGAB\|(nigin₂)<br><br>![nigin2](../../../images/builder/nigin2.png) |
| (...) | grouping of signs, e.g., GA₂×(ME.EN)<br><br>![ga2-times-me-en](../../../images/builder/ga2-times-me-en.png) |
| @g  | gunu, e.g., DU@g<br><br>![du-gunu.png](../../../images/builder/du-gunu.png)<br><br>as opposed to standard DU<br><br>![du](../../../images/builder/du.png) |
| @t  | tenu, e.g., GAN₂@t<br><br>![gan2-tenu](../../../images/builder/gan2-tenu.png) |
| @v  | variant, e.g., 4(ban₂)@v<br><br>![4ban2-variant](../../../images/builder/4ban2-variant.png)<br><br>as opposed to the standard 4(ban₂)<br><br>![4ban2](../../../images/builder/4ban2.png) |

18 Dec 2019 osc at oracc dot org

Steve Tinney & Eleanor Robson

Steve Tinney & Eleanor Robson, 'ATF Quick Reference', _Oracc: The Open Richly Annotated Cuneiform Corpus_, Oracc, 2019 \[http://oracc.museum.upenn.edu/doc/help/editinginatf/quickreference/\]
