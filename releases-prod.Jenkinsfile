pipeline {
    agent {
        docker {
            image 'amiraniv/jenkins-agent-docker-yq:v2.0'
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
                script {
                    // Complete this code to deploy to a real Kubernetes cluster
                    sh "echo $JENKINS_POLY_PROD_IMG_URL"
                    sh "yq e '.spec.template.spec.containers[0].image = env.JENKINS_POLY_PROD_IMG_URL' k8s/prod/polybot.yaml"
                    sh 'git add k8s/prod/polybot.yaml'
                    sh 'git commit -m "updated image $JENKINS_POLY_PROD_IMG_URL"'
                    sh 'git push origin releases'
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
