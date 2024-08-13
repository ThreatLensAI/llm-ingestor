# CSYE7125 Helm Chart to deploy LLM Ingestor pods

This Helm chart is used to deploy LLM Ingestor pods in a Kubernetes cluster.

## Helm Installation

Please follow the installation instructions required for setting up the project [here](https://github.com/csye7125-su24-team06/helm-cluster-operations/blob/main/INSTALLATION.md).

## Chart Structure

The chart contains the following key files:

- `Chart.yaml`: Contains metadata for the chart.
- `values.yaml`: Contains default values for the chart.
- `templates/llm-ingestor-configmap.yaml`: Defines a ConfigMap for storing kafka configuration for llm-ingestor.
- `templates/llm-ingestor-secrets.yaml`: Defines a Secret for storing database and kafka credentials for llm-ingestor.
- `templates/db-secrets.yaml`: Defines a Secret for storing Flyway secrets for database migration.
- `templates/deployment.yaml`: Defines a Deployment for running database migrations & llm-ingestor.
- `templates/secrets.yaml`: Defines secrets for the dockerhub credentials.
- `templates/serviceaccount.yaml`: Defines a ServiceAccount for the llm-ingestor.

## Installation

To install the chart with default variables set in `values.yaml`, helm install requires following secrets to be provided.

Following secrets are required:

- `secrets.dockerhubconfigjson` - DockerHub credentials in base64 encoded format.
- `db.secrets.username` - Database username in base64 encoded format.
- `db.secrets.password` - Database password in base64 encoded format.
- `db.secrets.database` - Database name in base64 encoded format.
- `kafka.secrets.username` - Kafka username in base64 encoded format
- `kafka.secrets.password` - Kafka password in base64 encoded format

Following config is required:

- `db.config.host` - Database host.
- `db.config.port` - Database port.

This can be provided in following two ways:

1. Update the `values.yaml` file variable:

    ```yaml
    secrets:
        dockerhub: <base64 encoded dockerhub config/credentials>
    db:
        secrets:
            username: <base64 encoded db username>
            password: <base64 encoded db password>
            database: <base64 encoded db name>
        config:
            host: <db host>
            port: <db port>
    kafka:
        secrets:
            username: <base64 encoded kafka username>
            password: <base64 encoded kafka password>
    ```

    and then run the following command:

    ```bash
    helm install llm-ingestor .
    ```

    This will install the chart with the default values set in `values.yaml` in the `default` namespace.

## Uninstallation

To uninstall the chart, use the following command:

```bash
helm uninstall llm-ingestor
```

## Configuration

The following table lists the configurable parameters of the Helm chart and their default values.

| Parameter                     | Description                                    | Default                   |
| ----------------------------- | ---------------------------------------------- | ------------------------- |
| `nameOverride`                | Name override instead of fullname              | `llm-ingestor`            |
| `secrets.dockerhubconfigjson` | DockerHub credentials in base64 encoded format | `''`                      |
| `db.secrets.username`         | Database username in base64 encoded format     | `''`                      |
| `db.secrets.password`         | Database password in base64 encoded format     | `''`                      |
| `db.secrets.database`         | Database name in base64 encoded format         | `''`                      |
| `db.config.host`              | Database host                                  | `''`                      |
| `db.config.port`              | Database port                                  | `'5432'`                  |
| `image.repository`            | Image repository                               | `marlapativ/llm-ingestor` |
| `image.tag`                   | Image tag                                      | `latest`                  |
| `image.pullPolicy`            | Image pull policy                              | `Always`                  |
| `initContainers`              | Deployment init containers configuration       | See `values.yaml`         |
| `serviceAccount.create`       | Whether to create a service account            | `true`                    |
| `serviceAccount.name`         | Service account name                           | `llm-ingestor-sa`         |
| `serviceAccount.automount`    | Automount service account token                | `true`                    |
| `serviceAccount.annotations`  | Service account annotations                    | `{}`                      |
| `podAnnotations`              | Pod annotations                                | `{}`                      |
| `podLabels`                   | Pod labels                                     | `{}`                      |
| `resources`                   | Pod resource requests and limits               | `{}`                      |
| `pod.livenessProbe`           | Liveness probe configuration                   | See `values.yaml`         |
| `pod.readinessProbe`          | Readiness probe configuration                  | See `values.yaml`         |
| `env`                         | Environment Variables for llm-ingestor         | `{}`                      |
