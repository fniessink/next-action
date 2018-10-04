pipeline {
    agent any 
    stages {
        stage('Stage unit tests') {
            steps {
                sh 'pwd'
                sh 'ls'
                sh 'docker-compose up -f docker-compose.yml -f docker-compose-jenkins.yml up unittest'
            }
        }
    }
}
