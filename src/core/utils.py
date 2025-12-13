def validate_non_empty(value, field_name="Field"):
    if not value or str(value).strip() == "":
        raise ValueError(f"{field_name} cannot be empty.")
