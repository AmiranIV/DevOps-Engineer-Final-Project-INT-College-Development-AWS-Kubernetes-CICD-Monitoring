pipeline {
    agent {
        docker {
            image 'amiraniv/jenkins-agent-docker-yq:v3.0'
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
                // Complete this code to deploy to real k8s cluster
                sh 'echo kubectl apply -f ....'
                sh 'echo $JENKINS_POLY_PROD_IMG_URL'
                sh 'cd k8s/prod && ls'
                sh "sed -i \"s|image: .*|image: $JENKINS_POLY_PROD_IMG_URL|\" k8s/prod/polybot.yaml"
                sh 'git config --global --add safe.directory /var/lib/jenkins/workspace/prod/releases-prod'
                sh 'git config --global user.email "amiranivgi@gmail.com"'
                sh 'git config --global user.name "amiraniv"'
                sh 'git config --global credential.helper cache'

                // Adding secret text credentials to Git remote URL
                withCredentials([string(credentialsId: 'githubsecretpass', variable: 'password')]) {
                    sh "git remote set-url origin https://amiraniv:${password}@github.com/amiraniv/CICD-Final-Project.git"
                    sh 'git checkout releases'
                    sh 'git branch'
                    sh 'git add k8s/prod/polybot.yaml'
                    sh 'git commit -m "$JENKINS_POLY_PROD_IMG_URL" '
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
