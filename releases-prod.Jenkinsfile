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
    parameters {
        string(name: 'JENKINS_POLY_PROD_IMG_URL', defaultValue: '', description: '')
    }

    stages {
        stage('Deploy') {
            steps {
                // Install yq
                sh 'sudo snap install yq'

                // Display JENKINS_POLY_PROD_IMG_URL
                sh 'echo $JENKINS_POLY_PROD_IMG_URL'

                // Update image URL in polybot.yaml
                sh 'yq e \'.spec.template.spec.containers[0].image = env.JENKINS_POLY_PROD_IMG_URL\' k8s/prod/polybot.yaml'

                // Git operations
                sh 'git add k8s/prod/polybot.yaml'
                sh 'git commit -m "Updated production image: $JENKINS_POLY_PROD_IMG_URL"'
                sh 'git push origin releases'
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
