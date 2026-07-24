import re
import spacy

from functools import lru_cache

from presidio_analyzer import (
    AnalyzerEngine
)

# =====================================================
# LOAD SPACY (SMALL MODEL)
# =====================================================

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise RuntimeError(
        "The spaCy model 'en_core_web_sm' is not installed. "
        "Please install it through requirements.txt."
    )

# =====================================================
# PRESIDIO
# =====================================================

analyzer = AnalyzerEngine()

# =====================================================
# FAST REGEX
# =====================================================

EMAIL_REGEX = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

PHONE_REGEX = re.compile(
    r"(?:\+91[\-\s]?)?(?:\(?\d{3,5}\)?[\-\s]?)?\d{10}\b"
)

URL_REGEX = re.compile(
    r"(https?://[^\s]+|www\.[^\s]+)"
)

IP_REGEX = re.compile(
    r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
)

DATE_REGEX = re.compile(
    r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"
)

PAN_REGEX = re.compile(
    r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"
)

CARD_REGEX = re.compile(
    r"\b(?:\d[ -]?){13,16}\b"
)

REGEX_PATTERNS = {

    "EMAIL": EMAIL_REGEX,

    "PHONE": PHONE_REGEX,

    "URL": URL_REGEX,

    "IP": IP_REGEX,

    "DATE": DATE_REGEX,

    "PAN": PAN_REGEX,

    "CREDIT_CARD": CARD_REGEX

}


# =====================================================
# DETECTOR
# =====================================================

class PIIDetector:

    def __init__(self):

        self.nlp = nlp

        self.analyzer = analyzer

        self.regex_patterns = REGEX_PATTERNS

        self.cache = {}

    # --------------------------------------------------
    # FAST REGEX
    # --------------------------------------------------

    @lru_cache(maxsize=5000)
    def detect_regex(self, text):

        entities = []

        for entity_type, pattern in self.regex_patterns.items():

            for match in pattern.finditer(text):

                entities.append({

                    "type": entity_type,

                    "text": match.group(),

                    "start": match.start(),

                    "end": match.end()

                })

        return entities
        # --------------------------------------------------
    # FAST SPACY
    # --------------------------------------------------

    def detect_spacy(self, text):

        if not text or len(text.strip()) < 3:
            return []

        doc = self.nlp(text)

        entities = []

        for ent in doc.ents:

            if ent.label_ == "PERSON":

                entities.append({

                    "type": "PERSON",

                    "text": ent.text,

                    "start": ent.start_char,

                    "end": ent.end_char

                })

            elif ent.label_ == "ORG":

                entities.append({

                    "type": "COMPANY",

                    "text": ent.text,

                    "start": ent.start_char,

                    "end": ent.end_char

                })

            elif ent.label_ in ("GPE", "LOC", "FAC"):

                entities.append({

                    "type": "ADDRESS",

                    "text": ent.text,

                    "start": ent.start_char,

                    "end": ent.end_char

                })

        return entities


    # --------------------------------------------------
    # BATCH SPACY
    # --------------------------------------------------

    def detect_spacy_batch(self, texts):

        """
        Process hundreds of paragraphs together.
        Much faster than calling self.nlp(text)
        repeatedly.
        """

        results = []

        docs = self.nlp.pipe(

            texts,

            batch_size=64,

            disable=[
                "tagger",
                "parser",
                "lemmatizer",
                "textcat"
            ]

        )

        for doc in docs:

            entities = []

            for ent in doc.ents:

                if ent.label_ == "PERSON":

                    entities.append({

                        "type": "PERSON",

                        "text": ent.text,

                        "start": ent.start_char,

                        "end": ent.end_char

                    })

                elif ent.label_ == "ORG":

                    entities.append({

                        "type": "COMPANY",

                        "text": ent.text,

                        "start": ent.start_char,

                        "end": ent.end_char

                    })

                elif ent.label_ in (

                    "GPE",

                    "LOC",

                    "FAC"

                ):

                    entities.append({

                        "type": "ADDRESS",

                        "text": ent.text,

                        "start": ent.start_char,

                        "end": ent.end_char

                    })

            results.append(entities)

        return results
        # --------------------------------------------------
    # PRESIDIO (Selective)
    # --------------------------------------------------

    @lru_cache(maxsize=5000)
    def detect_presidio(self, text):

        if not text or len(text.strip()) < 10:
            return []

        # Skip Presidio if regex already found
        # obvious PII (huge speed improvement)

        regex_entities = self.detect_regex(text)

        regex_types = {
            e["type"]
            for e in regex_entities
        }

        skip_types = {

            "EMAIL",
            "PHONE",
            "PAN",
            "CREDIT_CARD",
            "IP",
            "URL"

        }

        if regex_types.issuperset(skip_types):
            return []

        presidio_entities = []

        results = self.analyzer.analyze(

            text=text,

            language="en",

            entities=[
                "PERSON",
                "LOCATION",
                "ORGANIZATION"
            ]

        )

        mapping = {

            "PERSON": "PERSON",

            "LOCATION": "ADDRESS",

            "ORGANIZATION": "COMPANY"

        }

        for item in results:

            presidio_entities.append({

                "type": mapping[item.entity_type],

                "text": text[item.start:item.end],

                "start": item.start,

                "end": item.end

            })

        return presidio_entities


    # --------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------

    def remove_duplicates(self, entities):

        seen = set()

        output = []

        for entity in entities:

            key = (

                entity["type"],

                entity["start"],

                entity["end"]

            )

            if key in seen:
                continue

            seen.add(key)

            output.append(entity)

        return output


    # --------------------------------------------------
    # REMOVE OVERLAPS
    # --------------------------------------------------

    def remove_overlaps(self, entities):

        if not entities:
            return []

        entities.sort(

            key=lambda x: (

                x["start"],

                -(x["end"]-x["start"])

            )

        )

        final = []

        current_end = -1

        for entity in entities:

            if entity["start"] >= current_end:

                final.append(entity)

                current_end = entity["end"]

        return final
        # --------------------------------------------------
    # MAIN DETECTION
    # --------------------------------------------------

    @lru_cache(maxsize=5000)
    def detect(self, text):

        if not text:
            return []

        text = text.strip()

        if len(text) < 3:
            return []

        # -----------------------------
        # Step 1 : Regex
        # -----------------------------

        regex_entities = self.detect_regex(text)

        all_entities = list(regex_entities)

        # -----------------------------
        # Step 2 : Decide if NLP needed
        # -----------------------------

        alpha_count = sum(
            c.isalpha()
            for c in text
        )

        needs_nlp = (
            alpha_count > 15
            and len(text.split()) > 3
        )

        if needs_nlp:

            all_entities.extend(
                self.detect_spacy(text)
            )

        # -----------------------------
        # Step 3 : Presidio only when
        # person/company/address absent
        # -----------------------------

        found_types = {

            entity["type"]

            for entity in all_entities

        }

        if not (

            "PERSON" in found_types

            or "COMPANY" in found_types

            or "ADDRESS" in found_types

        ):

            all_entities.extend(

                self.detect_presidio(text)

            )

        # -----------------------------
        # Cleanup
        # -----------------------------

        all_entities = self.remove_duplicates(

            all_entities

        )

        all_entities = self.remove_overlaps(

            all_entities

        )

        all_entities.sort(

            key=lambda x: x["start"]

        )

        return all_entities

    # --------------------------------------------------
    # BATCH DETECTION
    # --------------------------------------------------

    def detect_batch(self, texts):

        """
        Detect entities for hundreds of
        paragraphs together.
        """

        results = []

        spacy_results = self.detect_spacy_batch(texts)

        for text, spacy_entities in zip(
            texts,
            spacy_results
        ):

            regex_entities = self.detect_regex(text)

            entities = regex_entities + spacy_entities

            found = {

                entity["type"]

                for entity in entities

            }

            if not (

                "PERSON" in found

                or "COMPANY" in found

                or "ADDRESS" in found

            ):

                entities.extend(

                    self.detect_presidio(text)

                )

            entities = self.remove_duplicates(

                entities

            )

            entities = self.remove_overlaps(

                entities

            )

            entities.sort(

                key=lambda x: x["start"]

            )

            results.append(

                entities

            )

        return results


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    detector = PIIDetector()

    sample = """

    Rajesh Kumar works at Infosys.

    Email:
    rajesh@gmail.com

    Phone:
    +91 9876543210

    PAN:
    ABCDE1234F

    Website:
    https://google.com

    """

    entities = detector.detect(sample)

    print()

    print("=" * 50)

    print("Detected Entities")

    print("=" * 50)

    for entity in entities:

        print(

            f"{entity['type']:15}"

            f"{entity['text']}"

        )