[Oracc] » [Help] » [Lemmatising] » Ngrammer

# The Ngrammer

The Ngrammer is a phase of Oracc lemmatization that performs disambiguation and annotation of sequences of lemmatized forms. It is called automatically during lemmatization, often multiple times for different purposes:

-   to create entries for PSUs (Phrasal Semantic Units, such as Sumerian compound verbs)
-   to apply disambiguation rules defined using the new @collo (collocation) tag in glossaries
-   to disambiguate ambiguous forms using the lemmatizer's statistics on adjacent forms (bigrams)

In addition, several analyzers are implemented using the Ngrammer but are not (at present) widely used throughout Oracc:

-   Date Specification Analyzer (DSA): annotate sequences of forms which comprise a date
-   Person Specification Analyzer (PSA): annotate sequences of forms which comprise a personal name and related information such as genealogical and professional qualifiers
-   Number System Analyzer (NSA): annotate sequences of forms which comprise a number or quantity

Ngrammer rules share the same syntax and the various analyzers have adjunct data files giving rules for the sequences to be annotated.

## Ngrammer Rules

An ngram rule consists of two parts: an input side and an output side. When the forms on the input are matched by the Ngrammer, the rules on the output side are applied. The separator between input and output is '=>', equals followed by right-angle-bracket.

The output side is optional because when the input side results in one or more matches the matched lemmata are kept and the unmatched lemmata are dropped, meaning that the input side is often enough to effect disambiguation because of the multi-word context it gives for selecting the matched lemmata.

Each member of the sequence of terms on the input and outsides is essentially a [signature]. These signatures are usually abbreviated to the minimum amount required for successful matching on the input side, and the minimum amount for editing the match sequence on the output side.

The special signature '\*' has different meanings on the input and output sides. On the input side it is a wildcard, matching any instances that occur between the terms on either side of it. On the output side it is a placeholder, meaning that there is no action required on the output side for the corresponding term on the output side.

If an output term begins with a semi-colon, ;, the corresponding term is cleared first, and then the ouptut term is applied. Thus, if the input term is a\[arm\] and the output term is ;PN, the result of applying the output is the equivalent of 'PN'. Without this, the result would be to set the POS for a\[arm\] to 'PN', which is probably not what is intended.

## Order of Application of Rules

The Ngrammer applies the longest rules first, and applies rules of the same length in the order in which they occur in the input files.

## Example

Here is an example of an ngram with both sides:

  a\[arm\] apin\[plow\] => a\[arm//plow handle\] \*

In this case, the Ngrammer looks for matches to the sequence of terms on the left, the input side. When it finds the sequence `a[arm] apin[plow]`, it applies the rules on the right, or output, side. In this case, it forces the SENSE of a\[arm\] to be "plow handle", and then does nothing for apin\[plow\], because of the place holder term '\*'.

### Predicates

Predicates are rules that may optionally be appended to the signature part of term. They are put in angle brackets with no space between them and the end of the term's signature.

A predicate may be negated by putting an exclamation mark, !, immediately after the opening left angle-bracket, `<! ...>`.

At present only one predicate is implemented, `vpr`, which succeeds if the instance has a verbal prefix. This is used in ePSD2 in the following entry to suppress matches to `e₂ mu-na-du₃`:

  @entry\* e duʾa \[lot\] N
  @parts e\[house\]N du\[build\]V/t<!vpr>
  @sense N a built-up house lot
  @end entry

[Oracc]: ../../../index.html
[Help]: ../../../help/index.html "Help page overview"
[Lemmatising]: ../../../help/lemmatising/index.html "Lemmatising ATF Files"
[signature]: ../../../help/lemmatising/signatures/index.html "Signatures"
