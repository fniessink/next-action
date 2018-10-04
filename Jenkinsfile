pipeline {
    agent any 
    stages {
        stage('Stage unit tests') {
            steps {
                sh 'docker-compose up unittest'
            }
        }
    }
}
