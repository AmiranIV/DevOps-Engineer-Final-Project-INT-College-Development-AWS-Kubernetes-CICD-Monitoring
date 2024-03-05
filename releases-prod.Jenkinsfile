pipeline {
    agent any
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

