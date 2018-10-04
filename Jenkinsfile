pipeline {
    agent any 
    stages {
        stage('Stage unit tests') {
            steps {
                sh 'pwd'
                sh 'ls'
                sh 'docker-compose up unittest-jenkins'
                sh 'docker-compose up unittest'
            }
        }
    }
}
