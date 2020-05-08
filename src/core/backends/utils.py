def validate_template_string(template_string, extra_map=()):

    clean_template = template_string

    replace_map = (
        ("&nbsp;}}", " }}"),
        ("{{&nbsp;", "{{ "),
        ("\r", ""),
    )

    replace_map += extra_map

    for _from, _to in replace_map:
        clean_template = clean_template.replace(_from, _to)

    return clean_template
