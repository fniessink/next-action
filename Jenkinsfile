pipeline {
    agent any 
    stages {
        stage('Stage unit tests') {
            steps {
                sh 'docker-compose -f docker-compose.yml -f docker-compose.jenkins.yml up unittest'
            }
        }
    }
}
