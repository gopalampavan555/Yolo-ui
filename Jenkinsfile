pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/gopalampavan555/Yolo_Task.git'
        BRANCH = 'main'
        IMAGE_NAME = 'yolo-ui'
        CONTAINER_NAME = 'yolo-container'
        DOCKER_HUB_USERNAME = 'kalyan555'  // Replace with your Docker Hub username
        DOCKER_HUB_REPO = 'yolo-ui'  // Replace with your Docker Hub repository name
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: "${BRANCH}", url: "${REPO_URL}"
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Stop & Remove Existing Container') {
            steps {
                script {
                    sh """
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                    """
                }
            }
        }

        stage('Run New Container') {
            steps {
                script {
                    sh """
                        docker run -d --name ${CONTAINER_NAME} -p 5000:5000 ${IMAGE_NAME}:latest
                    """
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                script {
                    withDockerRegistry(credentialsId: 'docker_cred') {
                        sh """
                            docker tag ${IMAGE_NAME}:latest ${DOCKER_HUB_USERNAME}/${DOCKER_HUB_REPO}:latest
                            docker push ${DOCKER_HUB_USERNAME}/${DOCKER_HUB_REPO}:latest
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Container is running successfully and image is pushed to Docker Hub!'
            sh "docker ps -a | grep ${CONTAINER_NAME}"
        }
        failure {
            echo 'Container deployment failed!'
        }
    }
}
