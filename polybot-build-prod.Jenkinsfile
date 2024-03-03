pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'amiraniv-github-prod', passwordVariable: 'passworddh', usernameVariable: 'usernamedh')]) {
                        sh """
                            docker login -u $usernamedh -p $passworddh
                            docker build -t jenkinspoly-prod-test:v1.0 .
                            docker tag jenkinspoly-prod-test:v1.0 $usernamedh/jenkinspoly-prod-test:v1.0
                            docker push $usernamedh/jenkinspoly-prod-test:v1.0
                        """
                    }
                }
            }
        }

        stage('Trigger Deploy') {
            steps {
                build job: 'polybot-build-prod', wait: false, parameters: [
                    string(name: 'polybot-prod-test', value: "$usernamedh/jenkinspoly-prod-test:v1.0")
                ]
            }
        }
    }
}
