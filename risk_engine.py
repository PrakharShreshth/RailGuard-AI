def calculate_risk(defect):

    risk_map = {
        "crack": ("Critical", 100),
        "bolt_missing": ("High", 80),
        "clip_missing": ("Medium", 60),
        "normal_track": ("Safe", 0)
    }

    return risk_map.get(
        defect,
        ("Unknown", 0)
    )
