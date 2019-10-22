#
# Supporting Services
#


from .helpers import curl_healthcheck, parse_version
from .service import StackService, Service


class Logstash(StackService, Service):
    SERVICE_PORT = 5044

    def build_candidate_manifest(self):
        version = self.version
        image = self.docker_name
        if self.oss:
            image += "-oss"
        key = "{image}-{version}-docker-image.tar.gz".format(
            image=image,
            version=version,
        )
        return self.bc["projects"]["logstash-docker"]["packages"][key]

    def _content(self):
        self.es_urls = ",".join(self.options.get(
            "logstash_elasticsearch_urls") or [self.DEFAULT_ELASTICSEARCH_HOSTS])
        if self.at_least_version("7.3") \
                or self.options.get("apm_server_snapshot") \
                or (not self.options.get("apm_server_version") is None and
                    parse_version("7.3") <= parse_version(self.options.get("apm_server_version"))):
            volumes = ["./docker/logstash/pipeline/:/usr/share/logstash/pipeline/"]
        else:
            volumes = ["./docker/logstash/pipeline-6.x-compat/:/usr/share/logstash/pipeline/"]

        return dict(
            depends_on={"elasticsearch": {"condition": "service_healthy"}} if self.options.get(
                "enable_elasticsearch", True) else {},
            environment={
                "ELASTICSEARCH_URL": self.es_urls,
            },
            healthcheck=curl_healthcheck(9600, "logstash", path="/"),
            ports=[self.publish_port(self.port, self.SERVICE_PORT), "9600"],
            volumes=volumes
        )

    @classmethod
    def add_arguments(cls, parser):
        super(Logstash, cls).add_arguments(parser)
        parser.add_argument(
            "--logstash-elasticsearch-url",
            action="append",
            dest="logstash_elasticsearch_urls",
            help="logstash elasticsearch output url(s)."
        )


class Kafka(Service):
    SERVICE_PORT = 9092

    def _content(self):
        return dict(
            depends_on=["zookeeper"],
            environment={
                "KAFKA_ADVERTISED_LISTENERS": "PLAINTEXT://kafka:9092",
                "KAFKA_BROKER_ID": 1,
                "KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR": 1,
                "KAFKA_ZOOKEEPER_CONNECT": "zookeeper:2181",
            },
            image="confluentinc/cp-kafka:4.1.3",
            labels=None,
            logging=None,
            ports=[self.publish_port(self.port, self.SERVICE_PORT)],
        )


class Postgres(Service):
    SERVICE_PORT = 5432
    opbeans_side_car = True

    def _content(self):
        return dict(
            environment=["POSTGRES_DB=opbeans", "POSTGRES_PASSWORD=verysecure"],
            healthcheck={"interval": "10s", "test": ["CMD", "pg_isready", "-h", "postgres", "-U", "postgres"]},
            image="postgres:10",
            labels=None,
            ports=[self.publish_port(self.port, self.SERVICE_PORT, expose=True)],
            volumes=["./docker/opbeans/sql:/docker-entrypoint-initdb.d", "pgdata:/var/lib/postgresql/data"],
        )


class Redis(Service):
    SERVICE_PORT = 6379
    opbeans_side_car = True

    def _content(self):
        return dict(
            healthcheck={"interval": "10s", "test": ["CMD", "redis-cli", "ping"]},
            image="redis:4",
            labels=None,
            command="--save ''",  # disable persistence
            ports=[self.publish_port(self.port, self.SERVICE_PORT, expose=True)],
        )


class Zookeeper(Service):
    SERVICE_PORT = 2181

    def _content(self):
        return dict(
            environment={
                "ZOOKEEPER_CLIENT_PORT": 2181,
                "ZOOKEEPER_TICK_TIME": 2000,
            },
            image="confluentinc/cp-zookeeper:latest",
            labels=None,
            logging=None,
            ports=[self.publish_port(self.port, self.SERVICE_PORT)],
        )