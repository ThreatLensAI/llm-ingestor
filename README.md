# llm-ingestor

This repository contains the following components:
1. **Helm Chart for llm-ingestor**: Located in `/charts/llm-ingestor`.
2. **Application Code for Ingestor**: Located in `/ingestor` with its Dockerfile.
3. **Application Code for LLM Pipeline**: Located in `/pipelines` with its Dockerfile (used by a chart not included in this repository).

## Helm Chart Overview

The Helm chart is designed to deploy the `llm-ingestor` application. Below are the configuration options available in the chart.

## Configuration

The following table lists the configurable parameters of the `llm-ingestor` Helm chart and their default values.

| Parameter                                      | Description                                                    | Default Value                    |
|------------------------------------------------|----------------------------------------------------------------|----------------------------------|
| `nameOverride`                                 | Name override for the deployment                               | `llm-ingestor`                   |
| `secrets.dockerhubconfigjson`                  | Docker Hub credentials secret                                  | `''`                             |
| `env.KAFKA_SERVICE`                            | Kafka service endpoint                                         | `localhost:9092`                 |
| `env.KAFKA_TOPIC`                              | Kafka topic to consume                                         | `cve`                            |
| `env.KAFKA_CONSUMER_GROUP_ID`                  | Kafka consumer group ID                                        | `llm-ingestor`                   |
| `env.KAFKA_MAX_SIZE`                           | Maximum Kafka message size                                     | `10000000`                       |
| `env.PORT`                                     | Port on which the application listens                          | `3001`                           |
| `env.LLAMAINDEX_OLLAMA_BASE_URL`               | Base URL for the LlamaIndex Ollama                             | `http://localhost:11434`         |
| `env.LLAMAINDEX_MODEL_NAME`                    | Model name for LlamaIndex                                      | `gemma:2b`                       |
| `env.EMBEDDING_DIM`                            | Embedding dimension for LlamaIndex                             | `1024`                           |
| `env.LLAMAINDEX_EMBEDDING_MODEL_NAME`          | Embedding model name for LlamaIndex                            | `mxbai-embed-large:latest`       |
| `initContainers[].name`                        | Name of the init container                                     | `db-migrate`                     |
| `initContainers[].repository`                  | Repository for the init container                              | `marlapativ/db-migration`        |
| `initContainers[].tag`                         | Tag for the init container                                     | `latest`                         |
| `initContainers[].pullPolicy`                  | Pull policy for the init container                             | `Always`                         |
| `initContainers[].command`                     | Command to run in the init container                           | `['flyway']`                     |
| `initContainers[].args`                        | Arguments for the init container command                       | `['migrate']`                    |
| `initContainers[].resources.limits.cpu`        | CPU limit for the init container                               | `100m`                           |
| `initContainers[].resources.limits.memory`     | Memory limit for the init container                            | `100Mi`                          |
| `initContainers[].resources.requests.cpu`      | CPU request for the init container                             | `10m`                            |
| `initContainers[].resources.requests.memory`   | Memory request for the init container                          | `25Mi`                           |
| `extraSecrets`                                 | Additional secrets to be provided                              | `{}`                             |
| `pod.readinessProbe.path`                      | Path for the readiness probe                                   | `/healthz`                       |
| `pod.livenessProbe.path`                       | Path for the liveness probe                                    | `/healthz`                       |
| `resources.limits.cpu`                         | CPU limit for the application pod                              | `500m`                           |
| `resources.limits.memory`                      | Memory limit for the application pod                           | `384Mi`                          |
| `resources.requests.cpu`                       | CPU request for the application pod                            | `250m`                           |
| `resources.requests.memory`                    | Memory request for the application pod                         | `256Mi`                          |
| `podLabels`                                    | Labels to be applied to the pod                                | `{}`                             |
| `podAnnotations`                               | Annotations to be applied to the pod                           | `{}`                             |
| `serviceAccount.create`                        | Whether to create a new service account                        | `true`                           |
| `serviceAccount.name`                          | Name of the service account                                    | `llm-ingestor-sa`                |
| `serviceAccount.automount`                     | Automount service account token                                | `false`                          |
| `serviceAccount.annotations`                   | Annotations for the service account                            | `{}`                             |
| `db.secrets.postgresUsername`                  | Secret for PostgreSQL username                                 | `''`                             |
| `db.secrets.postgresPassword`                  | Secret for PostgreSQL password                                 | `''`                             |
| `db.config.host`                               | Host for the PostgreSQL database                               | `''`                             |
| `db.config.port`                               | Port for the PostgreSQL database                               | `5432`                           |
| `db.config.table`                              | Table name in the PostgreSQL database                          | `embeddings`                     |
| `db.config.schema`                             | Schema name in the PostgreSQL database                         | `cve`                            |
| `kafka.secrets.username`                       | Kafka username                                                 | `''`                             |
| `kafka.secrets.password`                       | Kafka password                                                 | `''`                             |
| `replicaCount`                                 | Number of replicas for the deployment                          | `3`                              |
| `image.repository`                             | Docker image repository for the application                    | `marlapativ/llm-ingestor`        |
| `image.tag`                                    | Docker image tag for the application                           | `latest`                         |
| `image.pullPolicy`                             | Image pull policy                                              | `Always`                         |
| `affinity.enable`                              | Enable affinity for pod scheduling                             | `true`                           |
| `affinity.topologyKey`                         | Topology key for pod affinity                                  | `topology.kubernetes.io/zone`    |
| `pdb.create`                                   | Whether to create a Pod Disruption Budget                      | `true`                           |
| `pdb.minAvailable`                             | Minimum number of pods available under PDB                     | `1`                              |
| `pdb.maxUnavailable`                           | Maximum number of pods unavailable under PDB                   | `{}`                             |
| `autoscaling.hpa.enabled`                      | Enable Horizontal Pod Autoscaler                               | `true`                           |
| `autoscaling.hpa.minReplicas`                  | Minimum number of replicas under HPA                           | `1`                              |
| `autoscaling.hpa.maxReplicas`                  | Maximum number of replicas under HPA                           | `3`                              |
| `autoscaling.hpa.targetCPU`                    | Target CPU utilization percentage for HPA                      | `5`                              |
| `autoscaling.hpa.targetMemory`                 | Target memory utilization percentage for HPA                   | `80`                             |
| `autoscaling.hpa.annotations`                  | Annotations for the HPA                                        | `{}`                             |

## Usage

To deploy the `llm-ingestor` Helm chart, use the following command:

```bash
helm install llm-ingestor /charts/llm-ingestor --values /path/to/your/values.yaml
```

---

This template provides a clear overview of the configuration parameters and their default values, making it easy for users to understand and customize the deployment.
