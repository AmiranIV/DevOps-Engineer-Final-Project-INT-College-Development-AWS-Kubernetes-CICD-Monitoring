pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh '''
                            docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
                            docker build -t jenkinspoly-prod-test:v1.0 .
                            docker tag jenkinspoly-prod-test:v1.0 amiraniv/jenkinspoly-prod-test:v1.0 
                            docker push amiraniv/jenkinspoly-prod-test:v1.0
                        '''
                    }
                }
            }
        }

        stage('Trigger Deploy') {
            steps {
                build job: 'polybot-build-prod', wait: false, parameters: [
                    string(name: 'polybot-build-prod', value: 'amiraniv/jenkinspoly-prod-test:v1.0')
                ]
            }
        }
    }
}
