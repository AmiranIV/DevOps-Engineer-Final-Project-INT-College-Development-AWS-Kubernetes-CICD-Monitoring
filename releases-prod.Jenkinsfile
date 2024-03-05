pipeline {
    agent {
        docker {
            image 'amiraniv/jenkins-agent-docker:v1.0'
            args '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    options {
        timestamps()
    }
    parameters { string(name: 'JENKINS_POLY_PROD_IMG_URL', defaultValue: '', description: '') }

    stages {
        stage('Deploy') {
            steps {
                // complete this code to deploy to real k8s cluster
                sh 'echo kubectl apply -f ....'
                sh 'echo $JENKINS_POLY_PROD_IMG_URL'
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}

