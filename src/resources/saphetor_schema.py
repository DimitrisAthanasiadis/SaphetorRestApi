import re

from marshmallow import Schema, ValidationError, fields, validates


class SaphetorPostSchema(Schema):
    CHROM = fields.Str(required=False)
    POS = fields.Int(required=False)
    ALT = fields.Str(required=False)
    REF = fields.Str(required=False)
    ID = fields.Str(required=True)

    @validates("CHROM")
    def validate_CHROM(self, value):
        if value[:3] != "chr":
            raise ValidationError("CHROM must start with 'chr'")

        num_pattern_compiled = re.compile(r"^chr[0-9]+$")
        letter_pattern_compiled = re.compile(r"^chr[XYM]+$")

        if (
            re.match(num_pattern_compiled, value) is None
            and re.match(letter_pattern_compiled, value) is None
        ):
            raise ValidationError(
                "CHROM must be in the format 'chr' followed by numbers between1-22 or 'chr' followed by X, Y, M"
            )

    @validates("ID")
    def validates_ID(self, value):
        if value[:2] != "rs":
            raise ValidationError("ID must start with 'rs'")

    @validates("ALT")
    def validates_ALT(self, value):
        if value not in ["A", "C", "G", "T"]:
            raise ValidationError("ALT must be one of 'A', 'C', 'G', 'T'")

    @validates("REF")
    def validates_REF(self, value):
        if value not in ["A", "C", "G", "T"]:
            raise ValidationError("REF must be one of 'A', 'C', 'G', 'T'")
