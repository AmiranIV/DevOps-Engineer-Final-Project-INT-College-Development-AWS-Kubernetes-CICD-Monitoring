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
        stage('Install yq') {
            steps {
                script {
                    sh 'sudo apt-get update && sudo apt-get install -y curl'
                    sh 'sudo curl -sL https://github.com/mikefarah/yq/releases/download/v4.9.6/yq_linux_amd64 -o /usr/local/bin/yq'
                    sh 'sudo chmod +x /usr/local/bin/yq'
                }
            }
        }
        
        stage('Deploy') {
            steps {
                // complete this code to deploy to real k8s cluster
                sh 'echo $JENKINS_POLY_PROD_IMG_URL'
                sh 'yq e \'.spec.template.spec.containers[0].image = env.JENKINS_POLY_PROD_IMG_URL\' k8s/prod/polybot.yaml'
                sh 'git add k8s/prod/polybot.yaml'
                sh 'git commit -m "updated prod $JENKINS_POLY_PROD_IMG_URL"'
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
