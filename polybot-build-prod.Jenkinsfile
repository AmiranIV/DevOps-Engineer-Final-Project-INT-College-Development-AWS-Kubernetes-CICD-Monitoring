pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                script {
                withCredentials([string(credentialsId: 'amiraniv-DH-prod-U', variable: 'AmiranIV-DH-U'), string(credentialsId: 'amiraniv-prod-DH-Pass', variable: 'AmiranIV-DH-Pass')])
                    {
                         sh '''
                            docker login -u $AmiranIV-DH-U -p $AmiranIV-DH-Pass
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

