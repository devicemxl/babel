[Oracc] » [Help] » [Editing in ATF] » Composites

# ATF Composites Conventions

This document describes ATF features which are available when entering composite texts.

Composite texts by convention have an ID beginning with Q and are declared by an @-line which immediately follows the &-line for the text:

    &Q000002 = Archaic Lu A
    @composite

Composite IDs are listed in the [Oracc Qcat] \[http://oracc.museum.upenn.edu/qcat\]. To obtain an ID for a composite text email osc at oracc dot org.

## Structure

Most of the @-lines which are permitted in transliterations are not permitted in composites; this is because composites are organized around documentary structure rather than the structure of a physical object. The one exception is that milestones are allowed in composites.

Documentary divisions are indicated in ATF by use of the `@div` tag which is followed by the name of the division and an optional name for the division. The `@div` tag requires a closing `@end` tag, which must take as its single argument the name of its corresponding opening `@div`. `@div`'s of different kinds may not be interwoven.
 
    @div part 1
    ...
    @end part
    
    @div colophon
    ...
    @end colophon

In the liturgical corpus (including ETCSL editions of texts which could reasonably be considered liturgical), kirugu and other rubrics are used as logical structures, and they contain subdivisions giving the actual rubric; this is supported with the following syntax:
    
    @div kirugu 1
    1.  tur3-ra-na ...
    
    @div rubric kirugu
    10. ki-ru-gu2 1(disz)-a-kam
    @end rubric
    
    @end kirugu
    
    @div giszgigal 1
    11. u2-a a-u3-a u2-a-u2-a
    
    @div rubric giszgigal
    12. gisz-gi4-gal2-bi-im
    @end rubric
    
    @end giszgigal

A physical location may be given in a composite by using the locator milestone; the content after locator is a label. This is intended for use when the documentary structure of composites is being used to edit a text which is preserved only in one exemplar (the ePSD royal inscriptions corpus edits all royal inscriptions as composites):
    
    1\. a
    @m=locator o 1

## Variants

Variants are implemented to support the ETCSL corpus but may be used in any composite.

18 Dec 2019 osc at oracc dot org

Steve Tinney

Steve Tinney, 'ATF Composites Conventions', _Oracc: The Open Richly Annotated Cuneiform Corpus_, Oracc, 2019 \[http://oracc.museum.upenn.edu/doc/help/editinginatf/composites/\]

[Oracc]: ../../../index.html
[Help]: ../../../help/index.html "Help page overview"
[Editing in ATF]: ../../../help/editinginatf/index.html "Working with ATF to edit texts"
[Oracc Qcat]: http://oracc.museum.upenn.edu/qcat "Link opens in new window"
