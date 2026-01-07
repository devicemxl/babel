[Oracc] » [Help] » [Lemmatising] » PSA

# PSA: The Person Specification Analyser

This document contains a brief explanation of the rationale and implementation of one of Oracc's three entity recognisers: the Person Specification Analyzer (PSA). It includes schemas for configuration data and output. This document is a work-in-progress; it will certainly change as they are implemented.

## Definitions

### Person-specs

Persons are a subclass of Named Entity referring, in Mesopotamian culture at least, to humans, gods and beings in between. By convention, we write PN for Personal Name, with numeric subscripts to distinguish, e.g., PN1 from PN2.

A Person Specification (person-spec) is a series of words which identify a specific individual, though the specification may be indeterminate with respect to identity. Thus, in Ur III administrative texts a transaction function such as ŋiri = "via" may be followed not only by the name of a person, but also by a professional or functional designation referring to the transactor by office. Within certain contexts, then, a person-spec may be an unadorned functional term.

### Relations

Besides names and functional designations, a person-spec may include information on the individual's relatives, most commonly in the form "PN1 son of PN2", but with the expected range of possible relational designators.

A person-spec with no relational designators is called a `simple` person-spec. A person-spec with relational designators is called a `complex` person-spec. Such complex person-specs are actually person-specs which contain person-specs; these container relationships may be recursive.

### Role and Profession

A person-spec may also include designations of the individual's profession or customary function, and/or of the individual's role in a given transaction. In such constructs as "PN1 son of PN2, the scribe" the attribution of the profession to the correct PN may be uncertain.

### Anaphora

Texts frequently contain relationship information expressed by anaphora, and these anaphoric references are themselves frequently discontinuous with respect to the person-spec itself. Examples of this include constructs such as "PN1 ... PN2, his father". Identifying such references, even if incompletely, is a desideratum.

### Context

Various kinds of discourse context contain information relevant to person-specs. These include the syntactic/sentence-frame context (person-spec's role is buyer/seller, etc.) and object context (person-spec's actions include sealing document).

## Implementation

### Requirements

The implementation must be:

-   multilingual;
-   generalizable;
-   independently layered in terms of token-classification and program operation.

The input data must be:

-   lemmatized;
-   morphologically analyzed (anaphora resolution is not attempted if morphology is not available);
-   constructed in the form of an XCL tree.

Language configuration data must be:

-   expressed as a well-formed XML file conforming to the PSA configuration data schema.

Input data which does not meet these contraints can be preprocessed appropriately.

### Concepts

Type

As explained above, there are two types of person-spec: simple and complex. A complex person-spec is one which contains further person-specs, which may themselves be simple or complex, and so on.

Head

The PN or other designator which is at the top of a person-spec container hierarchy is referred to as the `head` of the person-spec.

Properties

The information that is part of a person-spec may be thought of in terms of its `properties`. Person-spec properties include the name(s) of the person, relations such as 'son-of', daughter-of', and profession/role designations.

Operators

Relators, profession and role designations may all be viewed as operators: relators are binary operators, applicable to two person-specs (normally the preceding and following person-specs). Profession and role designations are unary operators, applicable to only one person-spec (normally the preceding one, but in the case of Ur III transaction markers like ŋiri they may apply to the following person-spec).

As a matter of discursive simplicity, this document tends to talk in terms of operators being applied to person-specs with the result that they contribute properties to the person-specs.

Direction

Unary operators have an application direction, given as `forward` or `backward`. Operators that are applied `forward` contribute properties to the following person-spec; those which are applied backward contribute properties to the preceding person-spec.

Scope

In a simple person-spec the scope is not an issue: the scope is person-spec. In complex person-specs, scope is the level at which designators are applied to a head, and we generalize those levels as `outer`, or top-level, and `inner`, or lower-level. Consider the following examples from Sumerian:

(0) Dudu dubsar
(1) Dudu dumu Dada dubsar
(2) Dudu dumu Dada dumu Didi

In these examples we have both simple and complex person-specs, with both binary and unary operators.

In example (0), the person-spec is simple, and the scope within which to apply the unary operator `dubsar`, "scribe", is clear: it applies to the head of the single person-spec.

In example (1), the person-spec is complex. Several person-specs are actually involved, which may be partially (and minimally) bracketed as:

(1') (1 Dudu dumu (2 Dada))

It is apparent that the unary operator `dubsar` could be applied either at the inner or the outer scope. Application at the inner scope yields:

(1'a) (1 Dudu dumu (2 Dada dubsar 2))

Application at the outer scope yields:

(1'b) (1 Dudu dumu (2 Dada) dubsar)

Unary Scope

Every unary operator specified in the configuration data must be given a scope. The scope may be over-ridden at the instance level by specifying either the `inner` or `outer` property on the lemmatization of the instance.

**N.B.: as of 2009-01-09 the facility to over-ride the default scope by specifying a lemma property is not yet implemented or documented in the lemmatizer.**

Binary Scope

Example (2) is provided to illustrate the effect of scope on binary operators. Like unary operators, binary operators must have a default scope defined in the configuration data. Defining the default scope of `dumu` as `inner` and `dubsar` as `outer` yields:

(2') (1 Dudu dumu (2 Dada dumu (3 Didi) 2) dubsar)

## Configuration

The configuration data for the PSA consists of a collection of property specifications keyed to lemmata and, possibly, lemma-sequences or patterns. Each language has its own configuration block. The PSA itself is language-agnostic, relying only on the information which is attached to the lemmata as a result of applying the configuration data to the input.

**N.B.:** In the present schema support for multi-word PSA tokens, such as Akkadian `māru ša` is not yet defined. It is, however, a recognized requirement and the intention is to address this requirement using the Ngram mechanism.

## psa.rnc

namespace psa     = "http://oracc.org/ns/psa/1.0"
start     = config

config    = element psa:config { lang\* }

lang      = element psa:lang   {
              attribute psa:target-lang { xsd:NMTOKEN },
              confdata\* 
	    }

confdata  = lemma | ngram

lemma     = element psa:lemma   { 
              cfgw , 
	      ((binary , prop-prev , prop-next) 
               |(unary , prop-this , direction)) ,
              scope
            }
ngram     = element psa:ngram   { text }

cfgw      = attribute psa:cfgw  { text }
binary    = attribute psa:arity { "binary" }
unary     = attribute psa:arity { "unary" }
direction = attribute psa:dir   { "backward" | "forward" }
scope     = attribute psa:scope { "inner" | " outer" }
prop-next = attribute psa:next  { text }
prop-prev = attribute psa:prev  { text }
prop-this = attribute psa:this  { text }

## Output

The results of running the PSA on an XTF text may appear in several places:

-   In the list of XFF structures attached to XCL lemma nodes.
    
    The PSA may result in the (partial) disambiguation of PN instances, resulting in elimination of unnecessary forms from ambiguity lists.
    
-   In the core attributes of individual XFF instance structures.
    
    The PSA may result in increased specificity of PN identifications, for example, a PN marked as SENSE=0, i.e., unresolved, may be able to recategorized as a specific individual.
    
-   In the properties of individual XFF instance structures.
    
    In the case of person-specs whose head is a PN, unary properties attached to person-specs by the PSA are retrofitted into the XCL tree as properties on the instance forms.
    
-   In the Linkbase belonging to the text.
    
    Relations and other structures that have more than one member are entered as linksets in the Linkbase. From there they can be harvested and integrated into the Corpus-Based Dictionaries.
    

18 Dec 2019 osc at oracc dot org

Steve Tinney

Steve Tinney, 'PSA: The Person Specification Analyser', _Oracc: The Open Richly Annotated Cuneiform Corpus_, Oracc, 2019 \[http://oracc.museum.upenn.edu/doc/help/lemmatising/psa/\]

[Oracc]: ../../../index.html
[Help]: ../../../help/index.html "Help page overview"
[Lemmatising]: ../../../help/lemmatising/index.html "Lemmatising ATF Files"
