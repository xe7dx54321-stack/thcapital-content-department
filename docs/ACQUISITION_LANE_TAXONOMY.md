# Acquisition Lane Taxonomy

The acquisition lane taxonomy answers what each signal type is for, how strong it is as evidence, and where it may go downstream.

Key rules:

- One source has one primary lane and may have secondary tags.
- Reddit / X / YouTube / trend heat / WeChat metadata are weak or manual lanes.
- Lane definitions live in `config/acquisition_lanes.yaml`.
- Python code loads and validates the taxonomy; it does not hard-code lane semantics.
