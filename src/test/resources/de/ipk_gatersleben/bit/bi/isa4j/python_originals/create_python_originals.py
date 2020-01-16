# This was executed with isatools installed from GitHub (https://github.com/ISA-tools/isa-api)
# in version ee60fd53e61e0ecfa92f3a0a0954f6fd3032f832
from isatools.model import *
from isatools import isatab
import shutil

investigation = Investigation(identifier="Investigation ID")
investigation.title = "Drought Stress Response in Arabidopsis thaliana"
investigation.description = "An experiment about drought stress in Arabidopsis thaliana"
investigation.submission_date = "2019-01-16"

## Comments
investigation.comments.extend([
    Comment(name="Owning Organisation URI", value="http://www.ipk-gatersleben.de/"),
    Comment(name="Investigation Keywords", value="plant phenotyping, image analysis, arabidopsis thaliana, lemnatec"),
    Comment(name="License", value="CC BY 4.0 (Creative Commons Attribution) - https://creativecommons.org/licenses/by/4.0/legalcode"),
    Comment(name="MIAPPE version", value="1.1"),
])

# Ontologies
ontologies = {}
ontologies["CRediT"] = OntologySource(name = "CRediT", file="http://purl.org/credit/ontology#", description="CASRAI Contributor Roles Taxonomy (CRediT)")
ontologies["AGRO"] = OntologySource(name = "AGRO", file="http://purl.obolibrary.org/obo/agro/releases/2018-05-14/agro.owl", description="Agronomy Ontology", version="2018-05-14")
ontologies["UO"] = OntologySource(name = "UO", file="http://data.bioontology.org/ontologies/UO", description="Units of Measurement Ontology", version="38802")
investigation.ontology_source_references.extend(ontologies.values())

# Study
study = Study(filename="s_study.txt")
study.identifier = "1745AJ"
study.title = "Drought Stress Response in Arabidopsis thaliana"
investigation.studies.append(study)

## Factors
fa_drought_stress = StudyFactor(name="drought stress", comments=[
    Comment(name="Study Factor Description", value="Which plants were subjected to drought stress and which ones were not?"),
    Comment(name="Study Factor Values", value="drought;well watered")
])
study.factors.append(fa_drought_stress)

## Comments
study.comments.extend([
    Comment(name="Study Start Date", value=""),
    Comment(name="Study Country", value="Germany"),
    Comment(name="Study Experimental Site", value="LemnaTec Facility"),
    Comment(name="Study Longitude", value="11.27778")
])

## Design
study_design = OntologyAnnotation(term="Study Design")
study_design.comments.extend([
    Comment(name="Observation Unit Level Hierarchy", value="side>lane>block>pot"),
    Comment(name="Experimental Unit Level Hierarchy", value="plant"),
])
study.design_descriptors.append(study_design)

## Contacts
contacts = [
    ### Astrid
    Person(
      last_name = "Junker",
      first_name = "Astrid",
      email = "junkera@ipk-gatersleben.de",
      address = "Corrensstrasse 3, 06466 Stadt Seeland, OT Gatersleben, Germany",
      affiliation = "Leibniz Institute of Plant Genetics and Crop Plant Research (IPK) Gatersleben",
      roles = [
        OntologyAnnotation(
          term = "project administration role",
          term_source = ontologies["CRediT"],
          term_accession = "http://purl.org/credit/ontology#CREDIT_00000007"
        ),
      ],
      comments = [
        Comment(
          name = "Person ID",
          value = "https://orcid.org/0000-0002-4656-0308"
        )
      ]
    ),
    ### Dennis
    Person(
      last_name = "Psaroudakis",
      first_name = "Dennis",
      email = "psaroudakis@ipk-gatersleben.de",
      address = "Corrensstrasse 3, 06466 Stadt Seeland, OT Gatersleben, Germany",
      affiliation = "Leibniz Institute of Plant Genetics and Crop Plant Research (IPK) Gatersleben",
      roles = [
        OntologyAnnotation(
          term = "data curation role",
          term_source = ontologies["CRediT"],
          term_accession = "http://purl.org/credit/ontology#CREDIT_00000002"
        ),
      ],
      comments = [
        Comment(
          name = "Person ID",
          value = "https://orcid.org/0000-0002-7521-798X"
        )
      ]
    )
]
investigation.contacts.extend(contacts)
study.contacts.extend(contacts)

## Protocols
prot_phenotyping = Protocol(name="Phenotyping")
prot_watering    = Protocol(name="Watering")
study.protocols.append(prot_phenotyping)
study.protocols.append(prot_watering)
prot_watering.parameters.extend([
        ProtocolParameter(parameter_name=OntologyAnnotation(term="Irrigation Type")),
        ProtocolParameter(parameter_name=OntologyAnnotation(term="Volume")),
        ProtocolParameter(parameter_name=OntologyAnnotation(term="Watering Time"))
])

## Publication
pub = Publication(doi="PUB DOI",title="A title",author_list="Psaroudakis, D",status=OntologyAnnotation(term="fictional",term_accession="access123",term_source=ontologies["CRediT"]))
investigation.publications.append(pub)


isatab.dump(investigation, ".")
shutil.copyfile("i_investigation.txt", "../../isa4J/src/test/resources/de/ipk_gatersleben/bit/bi/isa4j/python_originals/i_investigation.txt")
