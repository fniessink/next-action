pipeline {
    agent any 
    stages {
        stage('Stage unit tests') {
            steps {
                docker-compose up unittest
            }
        }
    }
}
