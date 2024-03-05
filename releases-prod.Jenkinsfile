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
                script {
                    // Read YAML file
                    def yamlContent = readFile('k8s/prod/polybot.yaml')

                    // Convert YAML to JSON
                    def jsonContent = readYaml text: yamlContent

                    // Update image value
                    jsonContent.spec.template.spec.containers[0].image = env.JENKINS_POLY_PROD_IMG_URL

                    // Convert JSON back to YAML
                    def updatedYaml = yamlContent = yamlBuilder.toYaml(jsonContent)

                    // Write updated YAML back to file
                    writeFile file: 'k8s/prod/polybot.yaml', text: updatedYaml

                    // Verify changes
                    sh "cat k8s/prod/polybot.yaml"
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
