soapyfy - Keep your code clean from SOAP.
---
(c) 2014 Gregory Estrade and contributors.

Licensed under the [WTFPL](http://www.wtfpl.net/).

# Motivation

Because [SOAP](http://en.wikipedia.org/wiki/SOAP) is often seen as a complicated
standard to work with, plagued with implementation-dependent compatibility issues,
especially when you're dealing with different technology stacks.

Because most developers are more comfortable with
[REST](http://en.wikipedia.org/wiki/Representational_state_transfer)
architectures.

Because [JSON](http://en.wikipedia.org/wiki/JSON) is often preferred over
[XML](http://en.wikipedia.org/wiki/XML) for its better concision and human-readability.

# How

**soapyfy** is a simple Python script that runs a Web server acting as some kind of proxy.

It provides a set of endpoints generated from the
[WSDL](http://en.wikipedia.org/wiki/Web_Services_Description_Language) file
describing a **SOAP**-enabled Web service,
that accept and output **JSON** formatted data structures,
and performs the necessary conversions.

The API is browsable. **XSDs** are converted to [JSON-Schema](http://json-schema.org/), and dedicated endpoints are provided to perform validations of data structures.
