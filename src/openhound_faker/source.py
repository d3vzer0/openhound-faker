from openhound_faker.main import app
from openhound_faker.models.computer import FakeComputer
from faker import Faker
from faker.providers import internet
from dataclasses import dataclass

NODE_COUNT = 1000


@dataclass
class RandomContext:
    node_count: int


@app.resource(parallelized=False, columns=FakeComputer, name="fake_computer")
def computers(ctx: RandomContext):
    fake = Faker()
    fake.add_provider(internet)
    for idx in range(ctx.node_count):
        yield {
            "hostname": fake.hostname(),
            "ip_address": fake.ipv4(),
            "mac_address": fake.mac_address(),
        }


@app.source(name="random")
def source(node_count: int = NODE_COUNT):
    return computers(RandomContext(node_count=node_count))
