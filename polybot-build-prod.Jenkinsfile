pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                script {
                withCredentials([usernamePassword(credentialsId: 'amiraniv-github-prod', passwordVariable: 'amiraniv-dh-prod-pass', usernameVariable: 'amiraniv-dh-prod')])
                    {
                         sh '''
                            docker login -u $amiraniv-github-prod -p $amiraniv-dh-prod-pass
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


