
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
        string(name: 'JENKINS_YOLO_DEV_IMG_URL', defaultValue: '', description: '')
    }

    stages {
        stage('Deploy') {
            steps {
                // Complete this code to deploy to real k8s cluster
              withCredentials([string(credentialsId: 'jenkinsclassicgithubtoken-dev', variable: 'jenkinsclassicgithubtoken')]) {
                sh 'git config --global --add safe.directory /var/lib/jenkins/workspace/dev/releases-yolo-dev'
                sh 'git config --global user.email "amiranivgi@gmail.com"'
                sh 'git config --global user.name "amiraniv"'
                sh 'git config --global credential.helper cache'
                sh "git remote set-url origin https://amiraniv:${jenkinsclassicgithubtoken}@github.com/amiraniv/CICD-Final-Project.git"
                sh 'git checkout releases'
                sh 'cd k8s/dev && ls'
                sh "sed -i \"s|image: .*|image: $JENKINS_POLY_DEV_IMG_URL|\" k8s/dev/yolo.yaml"
                sh 'git add k8s/dev/yolo.yaml'
                sh 'git commit -m "$JENKINS_YOLO_DEV_IMG_URL" '
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

