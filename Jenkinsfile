pipeline {
    environment {
        imageRegistry = "docker.io"
        imageRepo = "marlapativ"
        imageName = "llm-ingestor"
        pipelineImageName = "pipelines"
        registryCredential = "dockerhub"
    }
    agent any
    stages {
        stage('helm chart validations') {
            parallel {
                stage('helm lint') {
                    steps {
                        sh '''
                            helm lint charts/llm-ingestor --strict
                        '''
                    }
                }

                stage('helm template') {
                    steps {
                        sh '''
                            helm template charts/llm-ingestor
                        '''
                    }
                }
            }
        }

        stage('setup docker') {
            steps {

                sh '''
                    if [ -n "$(docker buildx ls | grep multiarch)" ]; then
                        docker buildx use multiarch
                    else
                        docker buildx create --name=multiarch --driver=docker-container --use --bootstrap 
                    fi
                '''

                script {
                    withCredentials([usernamePassword(credentialsId: registryCredential, passwordVariable: 'password', usernameVariable: 'username')]) {
                        sh('docker login -u $username -p $password')
                    }
                }
            }
        }

        stage('github release') {
            tools {
                nodejs "nodejs"
            }
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'github-app', passwordVariable: 'GITHUB_TOKEN', usernameVariable: 'GITHUB_USERNAME')]) {
                        sh '''
                            npm i -g @semantic-release/exec
                            export GITHUB_ACTION=true
                            npx semantic-release
                        '''
                    }
                }
            }
        }

        stage('build and push llm-ingestor image') {
            steps {
                    sh '''
                        export IMAGE_TAG=$(git describe --tags --abbrev=0)

                        docker buildx build \
                        --platform linux/amd64,linux/arm64 \
                        --builder multiarch \
                        -t $imageRepo/$imageName:latest \
                        -t $imageRepo/$imageName:$IMAGE_TAG \
                        -f ingestor/Dockerfile.llm-ingestor \
                        --push \
                        ingestor
                    '''
            }
        }

        stage('build and push open-webui pipelines image') {
            steps {
                    sh '''
                        export IMAGE_TAG=$(git describe --tags --abbrev=0)

                        docker buildx build \
                        --platform linux/amd64,linux/arm64 \
                        --builder multiarch \
                        -t $imageRepo/$pipelineImageName:latest \
                        -t $imageRepo/$pipelineImageName:$IMAGE_TAG \
                        -f pipelines/Dockerfile.pipelines \
                        --push \
                        pipelines
                    '''
            }
        }

        stage('helm chart release') {
            steps {
                script {
                    sh '''
                        cd charts/llm-ingestor
                        helm push *.tgz oci://$imageRegistry/$imageRepo
                    '''
                }
            }
        }
    }
}
