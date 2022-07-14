from dataclasses import dataclass, field, make_dataclass

buttons: dataclass = make_dataclass(
    "Buttons",
    fields=(
        ("play", int, field(default=0)),
        ("settings", int, field(default=2)),
        ("quit", int, field(default=4)),
        ("sound", int, field(default=3)),
        ("keybindings", int, field(default=1)),
        ("back", int, field(default=5)),
        ("save", int, field(default=6)),
        ("reset", int, field(default=7)),
    ),
    frozen=True,
)
