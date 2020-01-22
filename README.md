## Welcome
isa4J is a comprehensive and scalable Java Library for the programmatic generation of experimental metadata descriptions using the ISATab container format.
Every experiment or rather investigation is described using the hierarchical ISA (Investigation, Study, Assay) structure (for details see: [ISA Model and Serialization Specifications](https://isa-specs.readthedocs.io/en/latest/isatab.html)).
We're assuming you're familiar with the ISATab framework in the remainder of the manual so if you're not, please [read up about it first](https://isa-specs.readthedocs.io/en/latest/).

## 1. License and Citation
The software provided as-is and made available under the terms of the GNU GPLv3 license (https://www.gnu.org/licenses/gpl-3.0.en.html), granting you the freedom to run, use, study, share, and modify the software in any way you want as long as any derivative work is distributed under the same or equivalent terms ([details](https://en.wikipedia.org/wiki/GNU_General_Public_License#Terms_and_conditions)).
If you're referring to isa4J in a scientific publication, please cite our paper:

> Citation forthcoming

## 2. Installation
TODO

## 3. Usage

### 3.1 Creating the Investigation File
With only a few exceptions, isa4J classes and variables are named in keeping with the [ISA model schemas](https://github.com/ISA-tools/isa-api/tree/master/isatools/resources/schemas/isa_model_version_1_0_schemas/core) and all ISA classes are available in the `de.ipk_gatersleben.bit.bi.isa4j.components` package.
If you're new to ISATab and the following code is confusing you, it may be helpful to look at the TestInvestigation.writeToStream Unit test and read the Investigation File generated by it in parallel, so you can see what ends up where(TODO LINK).

#### 3.1.1 Investigations
Each investigation needs an identifier, anything else is optional.

```java
Investigation investigation = new Investigation("InvestigationID");
	investigation.setTitle("Investigation Title");
	investigation.setDescription("Investigation Description");
	investigation.setSubmissionDate(LocalDate.of(2019, 12, 22));
	investigation.setPublicReleaseDate(LocalDate.of(2020, 1, 16));
```

#### 3.1.2 Ontologies
If you want to refer to Ontologies lateron, define them here and add them to your investigation.

```java
Ontology creditOntology = new Ontology(
	"CRediT", // Name
	new URL("http://purl.org/credit/ontology"), // File/URL
	null, // Version
	"CASRAI Contributor Roles Taxonomy (CRediT)"	// Description
);
investigation.addOntology(creditOntology);
```

#### 3.1.3 OntologyAnnotations
Many fields and attributes take an OntologyAnnotation instead of a simple String.
Every OntologyAnnotation needs a `term` (the actual content), a `term accession` and `term source` are optional.

```java
OntologyAnnotation paperPublished = new OntologyAnnotation(
	"Published",	// Term
	"<TermAccessionNumber>",	// Term Accession Number
	creditOntology	// Ontology (as defined before)
);
```

#### 3.1.4 Publications
If you want to link any publications to the investigation, you can do so similarly to ontologies

```java
Publication statsStories = new Publication("Five Things I wish my Mother had told me, about Statistics that is", "Philip M. Dixon");
statsStories.setDOI("https://doi.org/10.4148/2475-7772.1013");
statsStories.setStatus(paperPublished); // as defined before
investigation.addPublication(statsStories);
```

#### 3.1.5 Contacts
Contacts can be added as Objects of the type `Person`:

```java
Person schlomo = new Person(
	"Schlomo", // First Name
	"Hootkins", // Last Name
	"schlomoHootkins@miofsiwa.foo", // Email
	"Ministry of Silly Walks", // Affiliation
	"4 Hanover House, 14 Hanover Square, London W1S 1HP" // Address
);
Person agatha  = new Person("Agatha", "Stroganoff", null, "Stroganoff Essential Eels", null);
// Agatha doesn't have an email or a postal address, but she has a fax number
agatha.setFax("+49 3553N714L 33l2");
// Add them as investigation contacts
investigation.addContact(schlomo);
investigation.addContact(agatha);
```

#### 3.1.6 Comments
Many objects can take comments. Their `CommentCollection` as accessible through the `.comments()` method.

```java
schlomo.comments().add(new Comment("Smell", "Very bad"));
schlomo.comments().add(new Comment("Hair", "Fabolous"));
schlomo.comments().getAll() // Returns a List<Comment>
schlomo.comments().findByName("Smell") // Returns an Optional<Comment>
investigation.comments().add(new Comment("Usability", "None"));
```

#### 3.1.7 Studies
At some point you will want to create one or more Study objects and attach them to your investigation.
Each study needs an identifier and a filename, if no filename is given it will be automatically constructed from the identifier.
If you want to save your study files someplace else than the current working directory (more on writing the files later), you can also pass a valid path.

```java
Study study1 = new Study("Study1ID", "s_study1.txt");
Study study2 = new Study("Study2ID"); // now the filename will be automatically set to "s_Study2ID.txt"
investigation.addStudy(study1);
investigation.addStudy(study2);
```

Like the Investigation, studies also can have a Title and Description, Contacts and Publications.
You can populate them just like you did the investigation.

Don't forget to define Study Factors and Protocols

```java
Factor soilCoverage = new Factor("soil coverage", new OntologyAnnotation("Factor Type"));
study1.addFactor(soilCoverage);
Protocol plantTalking = new Protocol("Plant Talking");
plantTalking.addComponent(new ProtocolComponent("Component Name", new OntologyAnnotation("Component Type")));
ProtocolParameter toneOfVoice = new ProtocolParameter("Tone of Voice");
plantTalking.addParameter(toneOfVoice);
```

#### 3.1.8 Assays
Finally you can link assays with each of your studies.
They only need a filename/path and no identifier.

```java
Assay assay1 = new Assay("a_assay.txt");
study1.addAssay(assay1);
```

#### 3.1.9 Writing the File
When you have added everything, you can simply write the investigation file to a location you specify:

```java
investigation.writeToFile("./i_investigation.txt");
```

Instead of writing to a file, you can also write to an open outputstream (e.g. if you're using isa4J in a REST server application)

```java
OutputStream os = new ByteArrayOutputStream(); // of course you would already have a stream
investigation.writeToStream(os);
```

Please note that unlike the `isatab.dump` method from the [python API](https://github.com/ISA-tools/isa-api), this only writes the investigation file and no study or assay files.
They have to be written separately.

### 3.2 Writing Study and Assay files
isa4J is designed to also work with study and assay files that are too large to fit in memory, so instead of populating a study object with all sources and samples and then writing everything in one go, you build and flush out the file iteratively.
After you have taken care of all information that's needed for the investigation file and have attached your study object to the investigation, you tell the study to open it's corresponding file for writing:

```java
study1.openFile(); // study1 is defined above
```

This will use the path or filename that you passed when you created the study or that you set with `.setFilename`, so no argument is needed here (this is done to ensure the filename mentioned in the investigation file matches the one you actually write to).

You then create Source and Sample Objects, connect them via a Process and flush them out into the file before creating the next set of objects:

```java
// Instead of looping through meaningless numbers, you would loop through your database entries,
// CSV entries, or whatever things you have that you want to describe with ISATab.
for(int i = 0; i < 5; i++) {
	Source source = new Source("Source Name");
	Sample sample = new Sample("Sample Name");
	Process talkingProcess = new Process(plantTalking); // plantTalking is a Protocol defined above
	talkingProcess.setInput(source);
	talkingProcess.setOutput(sample);

	// WRITE TO FILE HERE (see below)
}
```

The method to write a line to the study file is `writeLine(initiator)`, `initiator` being the first object in the line that is then connected via a chain of processes and samples/materials etc. to the last.
In our case that would be `source`.
But if you call `study1.writeLine(source)` at the marked space above, you will be met with an error:

```
Exception in thread "main" java.lang.IllegalStateException: Headers were not written yet
```

The reason is that, as explained before, isa4J doesn't know anything about the structure of any rows before or after the current one.
So if, for example, a Source in a later line has a Characteristic attached to it, that needs to be accounted for by having a corresponding entry in the file header and keeping an empty column for all the Sources that do not have this Characteristic.
That is why you have to explicitly tell isa4J what headers you need by passing an examplary initiator (e.g. Source) connected to a process/sample/material/datafile chain *that contains every field any of your future rows will need*:

```java
study1.writeHeadersFromExample(source);
```

In our case, where all lines are of homogenous structure, you can simply include it in the loop:

```java
for(int i = 0; i < 5; i++) {
	Source source = new Source("Source Name");
	Sample sample = new Sample("Sample Name");
	Process talkingProcess = new Process(plantTalking); // plantTalking is a Protocol defined above
	talkingProcess.setInput(source);
	talkingProcess.setOutput(sample);

	if(!study1.hasWrittenHeaders())
		study1.writeHeadersFromExample(source);
	study1.writeLine(source);
}
```

After you have written everything you want to write, you can close the file with

```java
study1.closeFile();
```

#### 3.2.1 Attributes for Sources, Samples, Processes etc.
In the ISA specification, Sources and Samples can have more than just a name.
You can attach, depending on the type of object, ParameterValues (for Processes), FactorValues (for Samples), and Characteristics (Sources, Samples, and Materials).
Many objects can also be annotated with Comments.
The way you do this is very similar to how you populate the Investigation file above:

```java
Source source = new Source("Source Name");
source.addCharacteristic(new Characteristic("Characteristic 1", new OntologyAnnotation("Characteristic1Value","Char1Acc",creditOntology))); // creditOntology defined above

Sample sample = new Sample("Sample Name");
sample.addFactorValue(new FactorValue(
	soilCoverage, // Factor devined above
	34.12, // Value (can also be a String or an OntologyAnnotation)
	new OntologyAnnotation("%") // Unit
));

Process process = new Process(plantTalking);
process.addParameterValue(
	new ProtocolParameter(toneOfVoice, "soft") // similar to FactorValue: can have double/string/OntologyAnnotation values and an optional unit
); 

// Comments work the same way as before
source.comments().add(new Comment("Comment Name", "Comment Value"));
```

Of course it makes sense to define Objects that you are going to use multiple times outside of your loop, so a more complete example could look like this:

```java
Characteristic species = new Characteristic("Organism", new OntologyAnnotation("Arabidopsis thaliana","http://purl.obolibrary.org/obo/NCBITaxon_3702",ncbiTaxonomy)); // ontology not defined here
ParameterValue softSpeaking = new ParameterValue(toneOfVoice, "Very softly");
study1.openFile();
for(int i = 0; i < 5; i++) {
	Source source = new Source("Source Name");
	source.addCharacteristic(species);
	Sample sample = new Sample("Sample Name");
	sample.addFactorValue(new FactorValue(soilCoverage, i*10, new OntologyAnnotation("%")));
	Process talkingProcess = new Process(plantTalking); // plantTalking is a Protocol defined above
	talkingProcess.addParameterValue(softSpeaking);
	talkingProcess.setInput(source);
	talkingProcess.setOutput(sample);

	if(!study1.hasWrittenHeaders())
		study1.writeHeadersFromExample(source);
	study1.writeLine(source);
}
study1.closeFile();
```

#### 3.2.2 Writing to Streams
Like the investigation file, you can also write study files to a stream instead of a file.

```java
study1.directToStream(os); // os = some OutputStream
// Write your lines here
study1.releaseStream();
```

The stream will not be closed by these methods so you can keep using it if you want to send anything after the study file content.

#### 3.3.3 What about Assays?
Assays work in the exact same way that studies do, they also have `openFile, writeHeadersFromExample, writeLine, closeFile` as well as `directToStream` and `releaseStream` methods.
In addition to Sources and Samples, you may want to make use of the `Material` and `DataFile` classes when writing assay files.

```java
Material material = new Material("Extract Name", "Extract No. 232");
extractionProcess.setInput(sample);
extractionProcess.setOutput(material);

DataFile sequenceFile = new DataFile("Raw Data File", "seq-232.fasta");
sequencingProcess.setInput(material);
sequencingProcess.setOutput(sequenceFile);
```

#### 3.3.4 Even more Speed
If you have multiple study or assay files and want to create them even faster, you can also parallelize the creation process for each of them into a separate thread or process.
Just make sure you're not writing to the same file from multiple threads/processes at the same time, that will create chaos.


### 3.4 Things to Look Out For

- All Strings passed to isa4J will be sanitized to make sure they don't break the format. Specifically that means all TABs and ENTERs will be converted to spaces. Watch out for that if you're passing data from somewhere into isa4J and then parsing the files somewhere else back into a database: The result will not be the same as the initial input.

## ISA JSON
isa4J does not provide export functions to the ISA JSON format.
If you need ISA JSON files, you can create ISATab files with isa4J and then [convert them with the python API](https://isatools.readthedocs.io/en/latest/conversions.html).
The conversion is very straightforward and should be doable even for people with no experience working in python.