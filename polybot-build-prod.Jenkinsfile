pipeline {
    agent {
        docker {
            image 'amiraniv/jenkins-agent-docker-yq:v3.0'
            args '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        DH_NAME = "amiraniv"
        FULL_VER = "v.$BUILD_NUMBER"
    }

    stages {
        stage('Build') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh '''
                            cd AWS-PolyBot
                            docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
                            docker build -t k8s-poly-amiran:$FULL_VER .
                            docker tag k8s-poly-amiran:$FULL_VER $DH_NAME/k8s-poly-amiran:$FULL_VER
                            docker push $DH_NAME/k8s-poly-amiran:$FULL_VER
                            sh 'echo building polybot pipeline fix...'
                        '''
                    }
                }
            }
        }

        stage('Trigger Deploy') {
            steps {
                build job: 'releases-prod', wait: false, parameters: [
                    string(name: 'JENKINS_POLY_PROD_IMG_URL', value: "$DH_NAME/k8s-poly-amiran:$FULL_VER")
                ]
            }
        }
    }

    post {
        always {
            sh '''
                docker system prune -a -f --filter "until=24h"
                docker builder prune -a -f --filter "until=24h"
            '''
            cleanWs()
        }
    }
}
