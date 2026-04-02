from openhound.core.app import OpenHound
from openhound.core.collect import CollectContext
from .lookup import RandomLookup
from dlt.extract.source import DltSource


app = OpenHound("random", source_kind="Rand", help="OpenGraph collector generating random resources")


@app.collect()
def collect(ctx: CollectContext) -> DltSource:
    """Register a Typer CLI command that generates random resources and stores them (filtered) on disk.

    Args:
        ctx (CollectContext): Returns DLT pipeline context.
    """
    from openhound_faker.source import source as dummy_source

    return dummy_source()


@app.preproc()
def preproc(ctx: CollectContext) -> dict[str, str]:

    return {"fake_computer": "fake_computer"}


@app.convert(lookup=RandomLookup)
def convert(ctx: CollectContext) -> tuple[DltSource, dict]:
    """Register a Typer CLI command that generates OpenGraph nodes/edges based on the random resource generator.

    Args:
        ctx (CollectContext): Returns DLT pipeline context.
    """
    from openhound_faker.source import source as dummy_source

    return dummy_source(), {}
