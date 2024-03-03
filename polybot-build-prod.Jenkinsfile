pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                script {
                withCredentials([string(credentialsId: 'amiraniv-DH-prod-U', variable: 'password-DH-prod')]) {
                         sh '''
                            docker login -u amiraniv -p $password-DH-prod
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
                    string(name: 'polybot-prod-test', value: 'amiraniv/jenkinspoly-prod-test:v1.0')
                ]
            }
        }
    }
}

