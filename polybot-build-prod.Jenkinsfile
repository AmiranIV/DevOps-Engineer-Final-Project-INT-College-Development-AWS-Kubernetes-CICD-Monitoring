pipeline {
    agent {
        docker {
            image 'amiraniv/jenkins-agent-docker:v1.0'
            args  '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    stages {
        stage('Build') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh '''
	                    cd AWS-PolyBot
                            docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
                            docker build -t jenkinspoly-prod-test:v1.0 .
                            docker tag jenkinspoly-prod-test:v1.0 amiraniv/jenkinspoly-prod-test:v1.0
                            docker push amiraniv/jenkinspoly-prod-test:v1.0
                        '''
                    }
                }
            }
        }

    }
}
